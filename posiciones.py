from xml.dom import minidom
import sys

#Se le pasa el SVG como parametro y devuelve el listado de frames a colocar en el 
#template.prep

PX_CM = 35.43844578313252
CM_PX = 1 / PX_CM

def px_to_cm(px):
    return float(px) * CM_PX

def desde_abajo(cm, altura):
    return (29.7 - cm) - altura

def redondear(nro):
    return round(nro, 4)

xmldoc = minidom.parse(sys.argv[1])
rectangulos = xmldoc.getElementsByTagName("rect")
for r in rectangulos:
    #print r.getAttribute("style")
    if "#1a1a1a" in r.getAttribute("style"):
        _id = r.getAttribute("id")
        ancho = px_to_cm(r.getAttribute("width"))
        alto = px_to_cm(r.getAttribute("height"))
        x = px_to_cm(r.getAttribute("x"))
        y = desde_abajo(px_to_cm(r.getAttribute("y")), alto)
        print "<frame id=\"{}\" x1=\"{}cm\" y1=\"{}cm\" width=\"{}cm\" height=\"{}cm\" />".format(_id, redondear(x), redondear(y), redondear(ancho), redondear(alto))

