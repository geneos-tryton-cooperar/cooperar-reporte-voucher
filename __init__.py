from trytond.pool import Pool
from .reporte import VoucherReport

def register():
    Pool.register(
        VoucherReport,
        module='cooperar-reporte-voucher', type_='report')

