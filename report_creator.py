from trytond.pool import Pool
import datetime
from decimal import Decimal, ROUND_DOWN, ROUND_HALF_DOWN
from .scripts import numeros_a_letras

def header_orden(voucher):   

    ret = dict(
        fecha = voucher.date,
        nro_orden_de_pago = voucher.number,
        apellidoNombre = voucher.party.name,
        cuil = Decimal(voucher.amount).quantize(Decimal(".01"), rounding=ROUND_DOWN),
    )
    return ret

def header_recibo(voucher):   

    address = voucher.party.address_get()
    montoenletras = numeros_a_letras.to_word(voucher.amount,'ARS')

    ret = dict(
        fecha = voucher.date,
        nrofactura = voucher.number,
        apellidoynombre = voucher.party.name + ' ' + address.street + ' ' + address.city,
        legajo7 = montoenletras,
    )
    return ret


def comprobante_orden(voucher):   
    
    def get_lineas(voucher):
        
        ret = []
        for line in voucher.lines:
            #Tipo Comprobante (Ver A o B), Nro Comprobante, Fecha, Importe            
            
            ret.append(('Factura ', line.name, str(line.date), str(Decimal(line.amount).quantize(Decimal(".01"), rounding=ROUND_DOWN))))
        return ret

    def get_linea_vacia():
        ret = []    
        ret.append((' ',' ',' ',' '))
        return ret

    
    if voucher.lines:
        lineas = get_lineas(voucher)
    else:
        lineas = get_linea_vacia()
    
    return {
        "tablaComprobante": lineas,
    }
  
def formas_de_pago_orden(voucher):   
    '''
    pago_cheque
    pago_banco                        ??????
    pago_importe
    pago_cheque_9   (tranferencia)    NADA
    pago_banco_7    (banco)           ??????
    pago_importe_8  (importe)
    pago_entidad                      ??????
    '''

    tranferencia = ''
    transferencia_banco = ''
    transferencia_importe = ''
    
    for payline in voucher.pay_lines:
        #import pudb;pu.db
        if payline.pay_mode.name == 'Transferencia':
            transferencia =  ''
            transferencia_banco = '' #Ver como lo obtengo
            transferencia_importe = str(payline.pay_amount)

    cheque = ''
    cheque_banco = ''
    cheque_importe = ''

    for check in voucher.issued_check:
        if check:
            cheque = check.name
            cheque_banco = ''
            cheque_importe = check.amount

    if cheque_importe != '':
        pago_importe = Decimal(cheque_importe).quantize(Decimal(".01"), rounding=ROUND_DOWN)


    if transferencia_importe != '':
        transferencia_importe = Decimal(transferencia_importe).quantize(Decimal(".01"), rounding=ROUND_DOWN)

    ret = dict(
        pago_cheque = cheque,
        pago_banco = cheque_banco,
        pago_importe = cheque_importe,
        pago_cheque_9 = tranferencia,
        pago_banco_7 = transferencia_banco,
        pago_importe_8 = transferencia_importe,
        pago_entidad = '',
    )
    return ret


def formas_de_pago_recibo(voucher):   

    def get_formas_de_pago(voucher):
        
        ret = []
        for payline in voucher.pay_lines:         
            ret.append((payline.pay_mode.name, str(Decimal(payline.pay_amount).quantize(Decimal(".01"), rounding=ROUND_DOWN))))
        
        for check in voucher.third_check:
            ret.append((check.name + ' ' + check.bank.name, str(Decimal(check.amount).quantize(Decimal(".01"), rounding=ROUND_DOWN))))
        
        return ret

    
    lineas = get_formas_de_pago(voucher)
    
    return {
        "formas_de_pago": lineas,
    }



def totales_orden(voucher):
    
    subtotal = voucher.amount
    retencion_gs = 0

    for retencion in voucher.retenciones_efectuadas:
        if retencion:
            retencion_gs += retencion.amount

    total = subtotal + retencion_gs

    total_formas_pago = 0
    
    for payline in voucher.pay_lines:
        if payline.pay_mode.name == 'Transferencia':
            total_formas_pago += float(payline.pay_amount)

    for check in voucher.issued_check:
        if check:
            total_formas_pago += float(check.amount)


    ret = dict(
        comp_subtotal = Decimal(subtotal).quantize(Decimal(".01"), rounding=ROUND_DOWN),
        comp_ret_imp = Decimal(retencion_gs).quantize(Decimal(".01"), rounding=ROUND_DOWN),
        comp_total = Decimal(total).quantize(Decimal(".01"), rounding=ROUND_DOWN),
        comp_total_6 = Decimal(total_formas_pago).quantize(Decimal(".01"), rounding=ROUND_DOWN),
    )
    return ret

def conceptos_orden(voucher):   
    #Por ahora que lo ingresen a mano en el comentario, despues deberia traer
    #los productos de las facturas
    conceptos = voucher.comment

    ret = dict(
        tablaConceptos = conceptos,
    )
    return ret

def conceptos_recibo(voucher):   

    def get_conceptos(voucher):
        
        ret = []
        Invoice = Pool().get('account.invoice')
        nombre_comprobante = ''
        for line in voucher.lines:  
            
            if int(line.amount) > 0:          
                if line.move_line:
                    invoices = Invoice.search(
                        [('move', '=', line.move_line.move.id)])
                    if invoices:
                        if str(invoices[0].invoice_type.id) == '12':
                            nombre_comprobante = 'Nota de Debito B'
                        elif str(invoices[0].invoice_type.id) == '11':
                            nombre_comprobante = 'Nota de Debito A'
                        elif str(invoices[0].invoice_type.id) == '7':
                            nombre_comprobante = 'Factura A'
                        elif str(invoices[0].invoice_type.id) == '8':
                            nombre_comprobante = 'Factura B'                        
                    
                    if int(line.amount) > 0:   
                        ret.append((nombre_comprobante + ' : ' + line.name))
                else:
                    ret.append((line.name))
        
        return ret
 
    conceptos = get_conceptos(voucher)

    if len(conceptos)==0:
        conceptos = [' ']
    
    return {
        "conceptos": conceptos,
    }

 
def totales_recibo(voucher):   

    total = voucher.amount

    ret = dict(
        total = Decimal(total).quantize(Decimal(".01"), rounding=ROUND_DOWN),
    )
    return ret


def imputacion_recibo(voucher):   
    #Ver si tengo que buscar alguna cuenta contable
    imputacion = ''

    ret = dict(
        total3 = imputacion,
    )
    return ret

def footer_orden(voucher):   
    #Control, Confeccion, Autorizacion: van vacios

    total_abonado = voucher.amount

    ret = dict(
        total_abonar = Decimal(total_abonado).quantize(Decimal(".01"), rounding=ROUND_DOWN),
    )
    return ret


SECCIONES_ORDEN = [
        header_orden,
        comprobante_orden,
        formas_de_pago_orden,
        totales_orden,
        conceptos_orden,
        footer_orden
]

SECCIONES_RECIBO = [
        header_recibo,
        formas_de_pago_recibo,
        conceptos_recibo,
        totales_recibo,
        imputacion_recibo
]


def crear_data_orden(voucher):
    data = []
    for seccion in SECCIONES_ORDEN:
        data.append(seccion(voucher))
    return data

def crear_data_recibo(voucher):
    data = []
    for seccion in SECCIONES_RECIBO:
        data.append(seccion(voucher))
    return data