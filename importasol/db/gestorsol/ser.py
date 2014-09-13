from ..base import SOLFile
from ..fields import CampoA, CampoN, CampoB, CampoND, CampoCuenta, CampoF


class SER(SOLFile):

    """ Servicios. """

    cA = CampoA("Codigo", size=13, truncate=False)
    cB = CampoA("Familia", size=3, truncate=False)
    cC = CampoA("Descripcion", size=50)
    cD = CampoN("Tipo de IVA", size=1, default=0)
    cE = CampoND("Precio de costo", size=12)
    cF = CampoND("Margen PVP", size=3)
    cG = CampoND("PVP", size=12)
    cH = CampoF("Fecha de alta")
    cI = CampoA("Mensaje Emergente", size=255)
    cJ = CampoA("Observaciones", size=255)
    cK = CampoB("No utilizar", default=False)
    cL = CampoB("No imprimir", default=False)
    cM = CampoA("Programable 1", size=25)
    cN = CampoA("Programable 2", size=25)
    cO = CampoA("Programable 3", size=25)
    cP = CampoCuenta("Cuenta Ventas", size=10)
    cQ = CampoCuenta("Cuenta Compras", size=10)
    cR = CampoF("Ultima modificacion")

    class Meta:
        tabla = 'SER'

    def __unicode__(self):
        t = u"SER(%s: %s)" % (self.cA, self.cC)
        return t

    __str__ = __unicode__
    __repr__ = __unicode__
