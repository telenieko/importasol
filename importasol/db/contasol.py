from decimal import Decimal
from .base import SOLFile
from .fields import CampoA, CampoT, CampoN, CampoF, CampoND, CampoV


class MAE(SOLFile):
    cA = CampoA("Cuenta", size=10, required=True)
    cB = CampoA("Descripcion", size=40, required=True)
    cC = CampoT("Descripcion Extendida")
    cD = CampoT("Mensaje Emergente")
    cE = CampoN("Departamento", size=4)
    cF = CampoN("Subdepartamento", size=4)

    class Meta:
        tabla = 'MAE'
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
        tabla = 'APU'
        aliases = (('cuenta', 'E'), ('asiento', 'C'), ('orden', 'D'),
                   ('concepto', 'G'), ('documento', 'H'), ('fecha', 'B'),
                   ('debe', 'I'), ('haber', 'J'), ('dpto', 'O'), ('subdpto', 'P'))

    def __unicode__(self):
        con = self.concepto and self.concepto[:10] or None
        return u"APU(%s: %s:%10s %s > %s" % \
                (self.asiento, self.orden, self.cuenta, self.euros, con)

    __str__ = __unicode__
    __repr__ = __unicode__
        

class Asiento():
    apuntes = None
    numero = None

    def __init__(self, numero=None, apuntes=None):
        self.numero = numero
        self.apuntes = []
        if apuntes:
            for apu in apuntes:
                self.apuntes.append(apu)

    def _get_descuadre(self):
        valor = 0
        for apu in self.apuntes:
            valor += apu.euros
        return valor
    descuadre = property(_get_descuadre)

    def cuadra(self):
        if self.descuadre != 0:
            return False
        return True

    def add(self, apunte):
        if apunte in self.apuntes:
            raise ValueError("Apunte duplicado en el asiento")
        self.apuntes.append(apunte)

    def rm(self, apunte):
        self.apuntes.remove(apunte)

    def reordena(self):
        """ Ordenar la lista de apuntes segun el campo Orden de cada uno. """
        self.apuntes = sorted(self.apuntes, key=lambda apu: apu.orden)

    def renumera(self):
        """ Pone el Orden de cada apunte segun donde esta ahora de la lista. """
        i = 1
        for apu in self.apuntes:
            apu.orden = i
            i += 1

    def vincular(self, entorno):
        for apu in self.apuntes:
            entorno.bind(apu)

    def desvincular(self):
        for apu in self.apuntes:
            apu.entorno.unbind(apu)

