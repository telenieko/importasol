from ..base import SOLFile
from ..fields import CampoCuenta, CampoDebeHaber, Campo, CampoN
from ...utiles import num_to_col_letters, col2num


class CreadorSaldos(Campo):

    """ CreadorSaldos: Utilidad para crear los campos de Saldos.

    Este "campo" simplemente crea de golpe los campos de saldos de
    todos los meses de forma mas rapida que escribirlos todos a mano...
    """
    columnas = {}

    def __init__(self, nombre, inicial, **kwargs):
        self.inicial = inicial
        self.columnas = {}
        super(CreadorSaldos, self).__init__(nombre, size=None, **kwargs)

    def crea_campo(self, cls, nombre, cd, ch, field_name):
        cd = num_to_col_letters(cd)
        ch = num_to_col_letters(ch)
        c = CampoDebeHaber(nombre, cd, ch, auto_alias=False)
        c.contribute_to_class(cls, field_name)
        return c

    def contribute_to_class(self, cls, field_name):
        columna = col2num(self.inicial)
        ad = self.crea_campo(cls, "Saldo de apertura %s" % self.nombre,
                             columna, columna+1,
                             '%s_ape' % field_name)
        columna += 2
        for i in range(0, 12):
            mes = i + 1
            cd = columna + i*2
            ch = columna + i*2 + 1
            col = self.crea_campo(cls, "Saldo %d" % mes, cd, ch, "%s_%d" % (field_name, mes))
            self.columnas.update({mes: col})
        columna += 24
        reg = self.crea_campo(cls, "Regularizacion %s" % self.nombre,
                              columna, columna+1, '%s_reg' % field_name)
        columna += 2
        cie = self.crea_campo(cls, "Cierre %s" % self.nombre,
                              columna, columna+1, '%s_reg' % field_name)
        self.columnas.update({'ape': ad, 'reg': reg, 'cie': cie})


class SAL(SOLFile):
    cA = CampoCuenta("Cuenta", size=10)
    euros = CreadorSaldos("euros", 'AF')
    cBJ = CampoN("Diario", size=3)
