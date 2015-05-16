from trytond.pool import Pool
from trytond.report import Report
import report_creator
from z3c.rml import rml2pdf
import template_orden_pago, template_recibo

class VoucherReport(Report):
    __name__ = 'account.voucher'

    @classmethod
    def crear_reporte(cls, voucher):

        #import pudb;pu.db
        
        if voucher.voucher_type == 'payment': #Orden de Pago
            datos = report_creator.crear_data_orden(voucher)
            rml_text = template_orden_pago.get(*datos)
            out = rml2pdf.parseString(rml_text)
            return out.read()
        elif voucher.voucher_type == 'receipt':  #Recibo
            datos = report_creator.crear_data_recibo(voucher)
            rml_text = template_recibo.get(*datos)
            out = rml2pdf.parseString(rml_text)
            return out.read()
        
    @classmethod
    def parse(cls, report, records, data, localcontext):
        """
        Armamos los datos que vamos a mostrar en la factura.
        LLamamos a llenar el template.
        Transformamos el template en un pdf y lo retornamos.
        """
        voucher = records[0]
        repo = cls.crear_reporte(voucher)
        #Voucher = Pool().get('account.voucher')
        #Voucher.write([Voucher(voucher.id)], {
        #    'voucher_report_cache': repo})
        return ('pdf', repo)

