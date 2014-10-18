from ..base import SOLFile
from ..fields import CampoA, CampoN, CampoF, CampoND, CampoCuenta, CampoB


class IVS(SOLFile):
    cA = CampoN("Codigo", size=5, required=True)
    cB = CampoN("Libro de IVA", size=1)
    cC = CampoF("Fecha")
    cD = CampoCuenta("Cuenta", size=10)
    cE = CampoA("Factura", size=12)
    cF = CampoA("Nombre", size=100)
    cG = CampoA("CIF", size=12)
    cH = CampoN("Tipo de operacion", size=1)
    cI = CampoN("Deducible", size=1)
    cJ = CampoND("Base 1", size=15)
    cK = CampoND("Base 2", size=15)
    cL = CampoND("Base 3", size=15)
    cM = CampoND("Porcen IVA 1", size=5)
    cN = CampoND("Porcen IVA 2", size=5)
    cO = CampoND("Porcen IVA 3", size=5)
    cP = CampoND("Porcen Recargo 1", size=5)
    cQ = CampoND("Porcen Recargo 2", size=5)
    cR = CampoND("Porcen Recargo 3", size=5)
    cS = CampoND("IVA 1", size=15)
    cT = CampoND("IVA 2", size=15)
    cU = CampoND("IVA 3", size=15)
    cV = CampoND("Recargo 1", size=15)
    cW = CampoND("Recargo 2", size=15)
    cX = CampoND("Recargo 3", size=15)
    cY = CampoND("Total", size=15)
    cZ = CampoB("Bienes soportados")
    cAS = CampoB("Incluir en 347")
    cAT = CampoND("Porcen Retencion", size=5)
    cAU = CampoND("Importe retencion", size=15)
    cAV = CampoN("Tipo de retencion", size=1)
    cAY = CampoND("Base Exenta", size=15)
    cBB = CampoN("Clave de Operacion", size=2)
    cBC = CampoN("Identificacion Fiscal", size=1)
    cBD = CampoN("Tipo de Impuesto", size=1)

    class Meta:
        tabla = 'IVS'
        aliases = (('libro', 'cB'), )

    def __unicode__(self):
        return u"IVS(%s.%s: %s %s)" % \
               (self.cB, self.cA, self.cE, self.cF)

    __str__ = __unicode__
    __repr__ = __unicode__


class IVR(SOLFile):
    cA = CampoN("Codigo", size=5, required=True)
    cB = CampoN("Libro de IVA", size=1, default=1)
    cC = CampoF("Fecha")
    cD = CampoCuenta("Cuenta", size=10)
    cE = CampoA("Factura", size=12)
    cF = CampoA("Nombre", size=100)
    cG = CampoA("CIF", size=12)
    cH = CampoN("Tipo de operacion", size=1)

    cI = CampoND("Base 1", size=15)
    cJ = CampoND("Base 2", size=15)
    cK = CampoND("Base 3", size=15)
    cL = CampoND("Porcen IVA 1", size=5)
    cM = CampoND("Porcen IVA 2", size=5)
    cN = CampoND("Porcen IVA 3", size=5)
    cO = CampoND("Porcen Recargo 1", size=5)
    cP = CampoND("Porcen Recargo 2", size=5)
    cQ = CampoND("Porcen Recargo 3", size=5)
    cR = CampoND("IVA 1", size=15)
    cS = CampoND("IVA 2", size=15)
    cT = CampoND("IVA 3", size=15)
    cU = CampoND("Recargo 1", size=15)
    cV = CampoND("Recargo 2", size=15)
    cW = CampoND("Recargo 3", size=15)
    cX = CampoND("Total", size=15)

    cAQ = CampoB("Incluir en 347")
    cAR = CampoND("Porcen Retencion", size=5)
    cAS = CampoND("Importe retencion", size=15)
    cAT = CampoN("Tipo de retencion", size=1)

    cAX = CampoN("Clave de Operacion", size=2)
    cAY = CampoN("Identificacion Fiscal", size=1)
    cAZ = CampoN("Tipo de Impuesto", size=1)
    cBF = CampoN("Tipo de Operacion", size=1)
    cBQ = CampoA("Documento FactuSOL", size=1)
    cBR = CampoA("Serie FactuSOL", size=1)
    cBS = CampoN("Codigo FactuSOL", size=6)

    class Meta:
        tabla = 'IVR'
        aliases = (('libro', 'cB'), )

    def __unicode__(self):
        return u"IVR(%s.%s: %s %s)" % \
               (self.cB, self.cA, self.cE, self.cF)

    __str__ = __unicode__
    __repr__ = __unicode__
