from decimal import Decimal
from .db.base import SOLFile
from .db.fields import CampoA, CampoT, CampoN, CampoF, CampoND, CampoV


class MAE(SOLFile):
    cA = CampoA("Cuenta", size=10, required=True)
    cB = CampoA("Descripcion", size=40, required=True)
    cC = CampoT("Descripcion Extendida")
    cD = CampoT("Mensaje Emergente")
    cE = CampoN("Departamento", size=4)
    cF = CampoN("Subdepartamento", size=4)

    class Meta:
        aliases = (('cuenta', 'A'), ('descripcion', 'B'),
                ('dpto', 'E'), ('subdpto', 'F'))

    def __unicode__(self):
        return u"MAE(%s: %s)" % (self.A, self.B)


def get_en_pesetas(obj, col_valor):
    val = getattr(obj, col_valor)
    return val * Decimal('166.386')

def set_euros(obj, value, col_debe, col_haber):
    if value < 0:
        debe = None
        haber = abs(value)
    elif value > 0:
        debe = abs(value)
        haber = None
    else:
        debe = haber = None
    setattr(obj, col_debe, debe)
    setattr(obj, col_haber, haber)

def get_euros(obj, col_debe, col_haber):
    d = getattr(obj, col_debe) or 0
    h = getattr(obj, col_haber) or 0
    importe = d - h
    return importe


class APU(SOLFile):
    cA = CampoN("Diario", size=3, default=1, required=True)
    cB = CampoF("Fecha", required=True)
    cC = CampoN("Asiento", size=5, default=0, required=True)
    cD = CampoN("Orden", size=6, required=True)
    cE = CampoA("Cuenta", size=10, required=True)
    cF = CampoV("Pesetas", size=15, getter=get_en_pesetas, parametros=('cI', 'cJ'))
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
    euros = CampoV("Euros", getter=get_euros, setter=set_euros, parametros=('cI', 'cJ'))

    class Meta:
        aliases = (('cuenta', 'E'), ('asiento', 'C'), ('orden', 'D'),
                   ('concepto', 'G'), ('documento', 'H'), ('fecha', 'B'),
                   ('debe', 'I'), ('haber', 'J'), ('dpto', 'O'), ('subdpto', 'P'))

    def __unicode__(self):
        return u"APU(%s: %d:%10s %s > %s" % \
                (self.asiento, self.orden, self.cuenta, self.euros, self.concepto[:10])
        

