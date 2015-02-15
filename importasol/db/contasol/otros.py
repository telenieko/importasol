from ..base import SOLFile
from ..fields import CampoA, CampoT, CampoN, CampoCuenta, CampoND


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


class PRO(SOLFile):
    cA = CampoN("Codigo", size=5, required=True)
    cB = CampoA("Nombre", size=100)
    cC = CampoA("NIF", truncate=False, size=12)
    cD = CampoA("Sigla del Domicilio", size=2)
    cE = CampoA("Domicilio", size=100)
    cF = CampoA("Numero de la calle", size=6)
    cG = CampoN("Codigo Postal", size=5)
    cH = CampoA("Poblacion", size=30)
    cI = CampoA("Provincia", size=20)
    cJ = CampoA("Telefono", truncate=False, size=15)
    cK = CampoA("Fax", size=15, truncate=False)
    cL = CampoA("Movil", size=15, truncate=False)
    cM = CampoA("Concepto Debe", size=40)
    cN = CampoN("Tipo de operaciones", size=1)
    cO = CampoA("Pais", size=3)
    cP = CampoA("Persona de Contacto", size=50)
    cQ = CampoA("Email", size=50)
    cR = CampoND("Porcen IVA", size=5)
    cR = CampoND("Porcen Recargo", size=5)
    cT = CampoCuenta("Cuenta Contrapartida 1", size=10)
    cU = CampoCuenta("Cuenta Contrapartida 2", size=10)
    cV = CampoCuenta("Cuenta Contrapartida 3", size=10)
    cW = CampoA("Banco", size=50, truncate=False)
    cX = CampoA("Entidad", size=4, truncate=False)
    cY = CampoA("Oficina", size=4, truncate=False)
    cZ = CampoA("DC", size=2, truncate=False)
    cAA = CampoA("Cuenta", size=10, truncate=False)
    cAB = CampoA("Mensaje Emergente", size=50)
    cAF = CampoN("Tipo de retenciones", size=1)
    cAG = CampoND("Porcen Retencion", size=5)
    cAH = CampoN("Tipo de deduccion", size=1)
    cAI = CampoA("IBAN", size=30)
    cAK = CampoN("Identificacion Fiscal", size=1)
    cAL = CampoN("Tipo de Impuesto", size=1)
    cAM = CampoN("Clave de operacion habitual", size=2)
    cAO = CampoN("Tipo de IVA predefinido", size=1)

    class Meta:
        tabla = 'PRO'

    def __unicode__(self):
        t = u"PRO(%s, %s)" % (self.cA, self.cB)
        return t

    __str__ = __unicode__
    __repr__ = __unicode__


class CLI(SOLFile):
    cA = CampoN("Codigo", size=5, required=True)
    cB = CampoA("Nombre", size=100)
    cC = CampoA("NIF", truncate=False, size=12)
    cD = CampoA("Sigla del Domicilio", size=2)
    cE = CampoA("Domicilio", size=100)
    cF = CampoA("Numero de la calle", size=6)
    cG = CampoN("Codigo Postal", size=5)
    cH = CampoA("Poblacion", size=30)
    cI = CampoA("Provincia", size=20)
    cJ = CampoA("Telefono", truncate=False, size=15)
    cK = CampoA("Fax", size=15, truncate=False)
    cL = CampoA("Movil", size=15, truncate=False)
    cM = CampoA("Banco", size=40, truncate=False)
    cN = CampoA("Entidad", size=4, truncate=False)
    cO = CampoA("Oficina", size=4, truncate=False)
    cP = CampoA("DC", size=2, truncate=False)
    cQ = CampoA("Cuenta", size=2, truncate=False)
    cR = CampoA("Concepto Debe", size=40)
    cS = CampoN("Tipo de operaciones", size=1)
    cR = CampoA("Pais", size=3)
    cU = CampoA("Persona de Contacto", size=50)
    cV = CampoA("Email", size=50)
    cW = CampoND("Porcen IVA", size=5)
    cX = CampoND("Porcen Recargo", size=5)
    cY = CampoCuenta("Cuenta Contrapartida 1", size=10)
    cZ = CampoCuenta("Cuenta Contrapartida 2", size=10)
    cAA = CampoCuenta("Cuenta Contrapartida 3", size=10)
    cAB = CampoA("Mensaje Emergente", size=50)
    cAF = CampoN("Tipo de retenciones", size=1)
    cAG = CampoND("Porcen Retencion", size=5)
    cAI = CampoA("IBAN", size=30)
    cAK = CampoN("Identificacion Fiscal", size=1)
    cAL = CampoN("Tipo de Impuesto", size=1)
    cAM = CampoN("Clave de operacion habitual", size=2)
    cAO = CampoN("Tipo de IVA predefinido", size=1)

    class Meta:
        tabla = 'CLI'

    def __unicode__(self):
        t = u"CLI(%s, %s)" % (self.cA, self.cB)
        return t

    __str__ = __unicode__
    __repr__ = __unicode__
