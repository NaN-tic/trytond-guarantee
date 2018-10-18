# The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.
from trytond.model import ModelView, ModelSQL, ModelSingleton, fields
from trytond.pool import Pool
from trytond.pyson import Eval
from trytond.modules.company.model import (
    CompanyMultiValueMixin, CompanyValueMixin)

__all__ = ['Configuration', 'ConfigurationSequence']


class Configuration(
        ModelSingleton, ModelSQL, ModelView, CompanyMultiValueMixin):
    'Guarantee Configuration'
    __name__ = 'guarantee.configuration'
    guarantee_sequence = fields.MultiValue(fields.Many2One(
            'ir.sequence', "Guarante Sequence", required=True,
            domain=[
                ('company', 'in',
                    [Eval('context', {}).get('company', -1), None]),
                ('code', '=', 'guarantee.guarantee'),
                ]))

    @classmethod
    def multivalue_model(cls, field):
        pool = Pool()
        if field == 'guarantee_sequence':
            return pool.get('guarantee.configuration.sequence')
        return super(Configuration, cls).multivalue_model(field)


class ConfigurationSequence(ModelSQL, CompanyValueMixin):
    "Guarantee Configuration Sequence"
    __name__ = 'guarantee.configuration.sequence'
    guarantee_sequence = fields.Many2One(
        'ir.sequence', "Guarante Sequence", required=True,
        domain=[
            ('company', 'in', [Eval('company', -1), None]),
            ('code', '=', 'guarantee.guarantee'),
            ],
        depends=['company'])

    @classmethod
    def default_guarantee_sequence(cls):
        pool = Pool()
        ModelData = pool.get('ir.model.data')
        try:
            return ModelData.get_id('guarantee', 'sequence_guarantee')
        except KeyError:
            return None
