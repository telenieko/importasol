from ..base import SOLFile
from ..fields import CampoA, CampoN, CampoB, CampoND


class FPA(SOLFile):

    """ Formas de pago/cobro. """

    cA = CampoA("Codigo", size=3, truncate=False)
    cB = CampoA("Descripcion", size=100)
    cC = CampoN("Numero Vencimientos", size=1)
    cD = CampoB("Pagos proporcionales", default=False)
    cE = CampoN("Dias vto 1", size=3)
    cK = CampoND("Proporcion vto 1", size=4)
    cQ = CampoB("Efectivo")
    cR = CampoN("Meses o Dias", size=1, default=1)
    cS = CampoA("Codigo en Factura-e", size=5, truncate=False)

    class Meta:
        tabla = 'FPA'

    def __unicode__(self):
        t = u"FPA(%s: %s)" % (self.cA, self.cB)
        return t

    __str__ = __unicode__
    __repr__ = __unicode__
