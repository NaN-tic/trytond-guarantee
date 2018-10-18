# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool
from . import configuration
from . import guarantee


def register():
    Pool.register(
        configuration.Configuration,
        configuration.ConfigurationSequence,
        guarantee.GuaranteeType,
        guarantee.Product,
        guarantee.Guarantee,
        guarantee.GuaranteeSaleLine,
        guarantee.GuaranteeInvoiceLine,
        guarantee.SaleLine,
        guarantee.InvoiceLine,
        module='guarantee', type_='model')
