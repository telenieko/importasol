from ..base import SOLFile
from ..fields import CampoA, CampoT, CampoN, CampoCuenta


class MAE(SOLFile):
    cA = CampoCuenta("Cuenta", size=10, required=True)
    cB = CampoA("Descripcion", size=40, required=True)
    cC = CampoT("Descripcion Extendida")
    cD = CampoT("Mensaje Emergente")
    cE = CampoN("Departamento", size=4)
    cF = CampoN("Subdepartamento", size=4)

    class Meta:
        tabla = 'MAE'
        aliases = (('dpto', 'E'), ('subdpto', 'F'))

    def __unicode__(self):
        t = u"MAE("
        if self.dpto:
            t += '%s' % self.dpto
        if self.subdpto:
            t += '|%s' % self.subdpto
        t += ') %s: %s' % (self.cA, self.cB)
        return t

    __str__ = __unicode__
    __repr__ = __unicode__


class DEP(SOLFile):
    cA = CampoN("Codigo", size=3, required=True)
    cB = CampoA("Denominacion", size=50)
    cC = CampoA("Observaciones", size=255)

    class Meta:
        tabla = 'DEP'

    def __unicode__(self):
        t = u"DEP(%s: %s)" % (self.cA, self.cB)
        return t

    __str__ = __unicode__
    __repr__ = __unicode__


class SDE(SOLFile):
    cA = CampoN("Departamento", size=3, required=True)
    cB = CampoN("Codigo", size=3, required=3)
    cC = CampoA("Denominacion", size=50)
    cD = CampoA("Observaciones", size=255)

    class Meta:
        tabla = 'SDE'

    def __unicode__(self):
        t = u"SDE(%s.%s: %s)" % (self.cA, self.cB, self.cC)
        return t

    __str__ = __unicode__
    __repr__ = __unicode__
