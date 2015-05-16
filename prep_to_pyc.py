from z3c.rml import rml2pdf
import preppy

template_recibo = preppy.getModule('template_recibo.prep')


#Traer cada modulo de datos
#rmlText = template.get("Martin Di Lisio", "Canada 1248 (7000) Tandil", ['uno', 'dos'])
#rmlText = template.get("Martin Di Lisio","Martin Di Lisio","Martin Di Lisio","Martin Di Lisio", "Canada 1248 (7000) Tandil", 'Exento', '20-28232105-0', '1111111','2222')

"""
#Convertimos el xml a pdf. parseString nos retorna un StringIO
out = rml2pdf.parseString(rmlText)
pdf = open("elpdf.pdf", "wb")
pdf.write(out.read())
"""
