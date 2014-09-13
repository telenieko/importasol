from ..base import SOLFile
from ..fields import CampoA, CampoN, CampoF, CampoND, CampoB


class FAC(SOLFile):
    cA = CampoA("Tipo", size=1, truncate=False)
    cB = CampoN("Numero", size=6)
    cC = CampoA("Referencia", size=50, truncate=False)
    cD = CampoF("Fecha")
    cE = CampoN("Estado", size=1)
    cF = CampoN("Agente", size=5)
    cG = CampoA("Proveedor", size=10)
    cH = CampoN("Cliente", size=5)
    cI = CampoA("Nombre del Cliente", size=50)
    cJ = CampoA("Domicilio del cliente", size=100)
    cK = CampoA("Poblacion", size=30)
    cL = CampoA("Codigo postal", size=10)
    cM = CampoA("Provincia", size=40)
    cN = CampoA("NIF", size=18)
    cO = CampoA("Tipo de IVA", size=1)
    cP = CampoN("Recargo de Equivalencia", size=1, default=0)
    cQ = CampoA("Telefono del cliente", size=20)
    cR = CampoND("Importe neto 1", size=12)
    cS = CampoND("Importe neto 2", size=12)
    cT = CampoND("Importe neto 3", size=12)

    cAS = CampoND("Base Imponible 1", size=12)
    cAT = CampoND("Base Imponible 2", size=12)
    cAU = CampoND("Base Imponible 3", size=12)
    cAV = CampoND("Porcentaje de IVA 1", size=2)
    cAW = CampoND("Porcentaje de IVA 2", size=2)
    cAX = CampoND("Porcentaje de IVA 3", size=2)
    cAY = CampoND("Importe de IVA 1", size=12)
    cAZ = CampoND("Importe de IVA 2", size=12)
    cBA = CampoND("Importe de IVA 3", size=12)
    cBJ = CampoND("Total", size=12)
    cBK = CampoA("Forma de pago", size=3, truncate=False)
    cBN = CampoA("Observaciones 1", size=100)
    cBO = CampoA("Observaciones 2", size=100)
    cBW = CampoB("Recibo Girado")
    cBZ = CampoB("Traspasada")
    cCA = CampoA("Anotaciones privadas", size=65000)
    cCC = CampoB("Impresa")
    cCW = CampoA("Banco", size=40)
    cCX = CampoA("Entidad", size=4)
    cCY = CampoA("Oficina", size=4)
    cCZ = CampoA("DC", size=4)
    cDA = CampoA("Cuenta", size=10)
    cDB = CampoND("Suplidos", size=12)

    def copiar_datos_cliente(self, cli, banco=True):
        """ Copiar datos del cliente que hay que meter en factura. """
        self.cliente = cli.codigo
        self.cI = cli.nombre
        self.cJ = cli.domicilio
        for campo in ('poblacion', 'codigo_postal', 'provincia', 'nif',
                      'tipo_de_iva', 'agente'):
            setattr(self, campo, getattr(cli, campo))
        if banco:
            for campo in ('banco', 'entidad', 'oficina', 'dc', 'cuenta'):
                setattr(self, campo, getattr(cli, campo))
        self.telefono_del_cliente = cli.telefono
        return True

    class Meta:
        tabla = 'FAC'

    def __unicode__(self):
        t = u"FAC(%s/%s, %s)" % (self.cA, self.cB, self.cC)
        return t

    __str__ = __unicode__
    __repr__ = __unicode__


class LFA(SOLFile):
    cA = CampoA("Tipo", size=1, truncate=False)
    cB = CampoN("Numero", size=6)
    cC = CampoA("Posicion", size=5, truncate=False)
    cD = CampoA("Articulo", size=13, truncate=False)
    cE = CampoA("Servicio", size=13, truncate=False)
    cF = CampoA("Descripcion", size=65000)
    cG = CampoND("Cantidad", size=12)
    cH = CampoND("Descuento1", size=2)
    cK = CampoND("Precio", size=12)
    cL = CampoND("Total", size=12)
    cM = CampoN("Tipo de IVA", size=1)
    cT = CampoB("IVA incluido")
    cU = CampoND("Precio IVA incluido", size=5)
    cV = CampoND("Total IVA incluido", size=5)

    class Meta:
        tabla = 'LFA'

    def __unicode__(self):
        t = u"LFA(%s/%s: %s, %s)" % (self.cA, self.cB, self.cC, self.cF)
        return t

    __str__ = __unicode__
    __repr__ = __unicode__


class LCO(SOLFile):
    cA = CampoA("Tipo", size=1, truncate=False)
    cB = CampoN("Numero", size=6)
    cC = CampoA("Posicion", size=5, truncate=False)
    cD = CampoF("Fecha")
    cE = CampoND("Importe", size=12)
    cF = CampoA("Concepto", size=40)
    cG = CampoN("Contrapartida", size=1)
    cH = CampoB("Traspasado")
    cI = CampoN("Anticipo", size=5)
    cJ = CampoN("Devolucion", size=1)
    cK = CampoA("Forma de pago", size=3, truncate=False)
    cL = CampoA("Observaciones", size=65000)

    class Meta:
        tabla = 'LCO'

    def __unicode__(self):
        t = u"LCA(%s/%s: %s, %s, %s)" % (self.cA, self.cB, self.cC, self.cD, self.cE)
        return t

    __str__ = __unicode__
    __repr__ = __unicode__
