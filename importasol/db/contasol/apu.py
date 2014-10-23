""" apu.py Tabla APU y Asiento. """
from decimal import Decimal
from ..base import SOLFile
from ..fields import CampoA, CampoT, CampoN, CampoF, CampoND, CampoV
from ..fields import CampoCuenta, CampoDebeHaber


def get_en_pesetas(obj, col_valor):
    val = getattr(obj, col_valor)
    return val * Decimal('166.386')


class APU(SOLFile):
    cA = CampoN("Diario", size=3, default=1, required=True)
    cB = CampoF("Fecha", required=True)
    cC = CampoN("Asiento", size=5, default=0, required=True)
    cD = CampoN("Orden", size=6, required=True)
    cE = CampoCuenta("Cuenta", size=10, required=True)
    cF = CampoV("Pesetas", size=15, getter=get_en_pesetas,
                parametros=('euros'))
    cG = CampoA("Concepto", size=60)
    cH = CampoA("Documento", size=5)
    cI = CampoND("Debe", size=15)
    cJ = CampoND("Haber", size=15)
    cK = CampoA("Moneda", size=1, default='E')
    cL = CampoN("Punteo", size=1, default=0)
    cM = CampoA("Tipo IVA", size=1)
    cN = CampoN("Codigo de IVA", size=5)
    cO = CampoN("Departamento", size=3)
    cP = CampoN("Subdepartamento", size=3)
    cQ = CampoT("Ruta Imagen")
    euros = CampoDebeHaber("Euros", 'I', 'J', editable=True)

    asi = None

    class Meta:
        tabla = 'APU'
        aliases = (('dpto', 'O'), ('subdpto', 'P'))

    def __unicode__(self):
        con = self.concepto and self.concepto[:40] or None
        return u"APU(%s: %s:%10s %s > %s)" % \
               (self.asiento, self.orden, self.cuenta, self.euros, con)

    __str__ = __unicode__
    __repr__ = __unicode__
