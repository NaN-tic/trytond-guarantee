# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from decimal import Decimal
import datetime
from dateutil.relativedelta import relativedelta
import doctest
import unittest
from trytond.pool import Pool
import trytond.tests.test_tryton
from trytond.tests.test_tryton import ModuleTestCase, with_transaction

from trytond.modules.company.tests import create_company, set_company


class TestCase(ModuleTestCase):
    'Test module'
    module = 'guarantee'

    @with_transaction()
    def test0010_in_guarante(self):
        'Test in_guarante'
        pool = Pool()
        Guarantee = pool.get('guarantee.guarantee')
        GuaranteeConfiguration = pool.get('guarantee.configuration')
        GuaranteeType = pool.get('guarantee.type')
        Product = pool.get('product.product')
        Sequence = pool.get('ir.sequence')
        Template = pool.get('product.template')
        Uom = pool.get('product.uom')

        company = create_company()
        with set_company(company):
            sequence, = Sequence.search([
                    ('code', '=', 'guarantee.guarantee')
                    ])
            GuaranteeConfiguration.create([{
                        'guarantee_sequence': sequence.id,
                        }])

            today = datetime.date.today()
            tomorrow = today + relativedelta(days=1)
            next_month = today + relativedelta(months=1)
            next_two_month = today + relativedelta(months=2)
            u, = Uom.search([('name', '=', 'Unit')])
            good, service, consumable = Template.create([{
                        'name': 'Test Guarantee Good',
                        'type': 'goods',
                        'list_price': Decimal(1),
                        'cost_price': Decimal(0),
                        'cost_price_method': 'fixed',
                        'default_uom': u.id,
                        }, {
                        'name': 'Test Guarantee Service',
                        'type': 'service',
                        'list_price': Decimal(1),
                        'cost_price': Decimal(0),
                        'cost_price_method': 'fixed',
                        'default_uom': u.id,
                        }, {
                        'name': 'Test Guarantee Consumable',
                        'type': 'goods',
                        'consumable': True,
                        'list_price': Decimal(1),
                        'cost_price': Decimal(0),
                        'cost_price_method': 'fixed',
                        'default_uom': u.id,
                        }])
            products = Product.create([{
                        'template': good.id,
                        }, {
                        'template': service.id,
                        }, {
                        'template': consumable.id,
                        }])
            good_product, service_product, consumable_product = products

            types = GuaranteeType.create([{
                        'name': 'Goods',
                        'includes_goods': True,
                        }, {
                        'name': 'Services',
                        'includes_services': True,
                        }, {
                        'name': 'Consumables',
                        'includes_consumables': True,
                        }])
            goods_guarantee, service_guarantee, consumable_guarantee = types
            tests = [{
                    'product': good_product,
                    'guarantee_type': goods_guarantee,
                    'start_date': today,
                    'end_date': next_month,
                    'test_date': today,
                    'result': True,
                    }, {
                    'product': good_product,
                    'guarantee_type': goods_guarantee,
                    'start_date': today,
                    'end_date': next_month,
                    'test_date': tomorrow,
                    'result': True,
                    }, {
                    'product': good_product,
                    'guarantee_type': goods_guarantee,
                    'start_date': today,
                    'end_date': next_month,
                    'test_date': next_month,
                    'result': True,
                    }, {
                    'product': good_product,
                    'guarantee_type': goods_guarantee,
                    'start_date': today,
                    'end_date': next_month,
                    'test_date': next_two_month,
                    'result': False,
                    }, {
                    'product': good_product,
                    'guarantee_type': service_guarantee,
                    'start_date': today,
                    'end_date': next_month,
                    'test_date': tomorrow,
                    'result': False,
                    }, {
                    'product': service_product,
                    'guarantee_type': service_guarantee,
                    'start_date': today,
                    'end_date': next_month,
                    'test_date': tomorrow,
                    'result': True,
                    }, {
                    'product': good_product,
                    'guarantee_type': consumable_guarantee,
                    'start_date': today,
                    'end_date': next_month,
                    'test_date': tomorrow,
                    'result': False,
                    }, {
                    'product': consumable_product,
                    'guarantee_type': consumable_guarantee,
                    'start_date': today,
                    'end_date': next_month,
                    'test_date': tomorrow,
                    'result': True,
                    }]
            for data in tests:
                guarantee, = Guarantee.create([{
                            'party': company.party.id,
                            'document': str(data['product']),
                            'type': data['guarantee_type'],
                            'start_date': data['start_date'],
                            'end_date': data['end_date'],
                            }])
                self.assertEqual(guarantee.applies_for_product(data['product'],
                        data['test_date']), data['result'])


def suite():
    suite = trytond.tests.test_tryton.suite()
    from trytond.modules.company.tests import test_company
    for test in test_company.suite():
        if test not in suite and not isinstance(test, doctest.DocTestCase):
            suite.addTest(test)
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestCase))
    return suite
