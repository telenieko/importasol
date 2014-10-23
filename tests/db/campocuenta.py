import unittest
from decimal import Decimal
from importasol.db import fields
from importasol.db.base import SOLFile
from importasol import exceptions
from importasol.entorno import EntornoSOL


class CCFile(SOLFile):
    cA = fields.CampoCuenta("Cuenta", size=15)

    class Meta:
        tabla = 'TST'
        aliases = (('cuenta', 'cA'), )

    def __unicode__(self):
        return u"TestCampoCuenta(%s)" % (self.cA)

    __str__ = __unicode__


class TestCampoCuenta(unittest.TestCase):
    def test_campocuenta(self):
        e = EntornoSOL()
        e.nivel_pgc = 8
        c = CCFile()
        c.cuenta = '43.0'
        f = c._meta.fields['cA']

        self.assertRaises(exceptions.ProgrammingError, f.get_valor, c)

        e.bind(c)
        val = f.get_valor(c)
        self.assertEqual('43000000', val)

        e.unbind(c)
        self.assertRaises(exceptions.ProgrammingError, f.get_valor, c)



