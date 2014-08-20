from ..base import SOLFile
from ..fields import CampoA, CampoN, CampoF, CampoB


def get_cD(obj):
    return obj.cD


class CLI(SOLFile):
    cA = CampoN("Codigo", size=5, required=True)
    cB = CampoN("Codigo Contabilidad", size=5)
    cC = CampoA("NIF", truncate=False, size=18)
    cD = CampoA("Nombre Fiscal", size=50)
    cE = CampoA("Nombre Comercial", size=50, default=get_cD)
    cF = CampoA("Domicilio", size=50)
    cG = CampoA("Poblacion", size=30)
    cH = CampoN("Codigo Postal", size=10)
    cI = CampoA("Provincia", size=40)
    cJ = CampoA("Pais", size=50)
    cK = CampoA("Telefono", truncate=False, size=50)
    cL = CampoA("Fax", size=25, truncate=False)
    cM = CampoA("Movil", size=50, truncate=False)
    cN = CampoA("Persona de Contacto", size=50)
    cO = CampoN("Agente", size=5)
    cP = CampoA("Banco", size=40, truncate=False)
    cQ = CampoA("Entidad", size=4, truncate=False)
    cR = CampoA("Oficina", size=4, truncate=False)
    cS = CampoA("DC", size=2, truncate=False)
    cT = CampoA("Cuenta", size=2, truncate=False)
    cU = CampoA("Forma de pago", size=3, truncate=False)
    cV = CampoA("Tipo de Cliente", size=3, truncate=False)
    cW = CampoA("Codigo Proveedor", size=10, truncate=False)
    cX = CampoA("Actividad", size=3, truncate=False)
    cY = CampoN("Aplicar IVA", size=1)
    cZ = CampoN("Tipo de IVA", size=1)
    cAB = CampoF("Fecha de Alta")
    cAC = CampoF("Fecha de nacimiento")
    cAD = CampoA("E-mail", size=60, truncate=False)
    cAE = CampoA("Direccion Web", size=60)
    cAF = CampoA("Cuenta Skype", size=60)
    cAG = CampoA("Mensaje Emergente", size=50)
    cAH = CampoA("Observaciones", size=255)
    cAI = CampoA("Horario", size=30)
    cAJ = CampoA("Vacaciones Desde", size=5)
    cAK = CampoA("Vacaciones Hasta", size=5)
    cAL = CampoB("Crear recibos al facturar", default=False)
    cAM = CampoB("No Vender", default=False)
    cAN = CampoB("No Facturar", default=False)
    cAO = CampoB("No imprimir", default=False)
    cAP = CampoA("Domicilio del Banco", size=100)
    cAQ = CampoA("Poblacion del banco", size=50)
    cAR = CampoA("IBAN del banco", size=50)
    cAS = CampoA("SWIFT del banco", size=11)

    cDK = CampoN("Tipo de impuesto", default=0, size=1)
    cDM = CampoA("Cuenta PGC", size=3, truncate=False)
    cDS = CampoN("Estado", size=1, default=0)
    cDV = CampoN("Dia de pago", size=2)

    class Meta:
        tabla = 'CLI'

    def __unicode__(self):
        t = u"CLI(%s, %s)" % (self.cA, self.cD)
        return t

    __str__ = __unicode__
    __repr__ = __unicode__
