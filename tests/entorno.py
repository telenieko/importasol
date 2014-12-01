import unittest
from decimal import Decimal
from importasol.entorno import EntornoSOL
from .fields import TestFile
from importasol.db.contasol import APU, Asiento
from StringIO import StringIO


class TestEntorno(unittest.TestCase):
    def test_entorno(self):
        e = EntornoSOL()
        f1 = TestFile()
        e.bind(f1)
        self.assertEqual(e, f1.entorno)
        e.unbind(f1)
        self.assertEqual(None, f1.entorno)

    def test_asiento(self):
        e = EntornoSOL()
        ap1 = APU()
        ap1.euros = 1000
        ap2 = APU()
        ap2.euros = -500
        ap3 = APU()
        ap3.euros = -500
        asi = Asiento(apuntes=[ap1, ap2, ap3])
        asi.vincular(e)
        self.assertListEqual([e, e, e],
                [ap1.entorno, ap2.entorno, ap3.entorno])
        asi.desvincular()
        self.assertListEqual([None, None, None],
                [ap1.entorno, ap2.entorno, ap3.entorno])

    def test_eventos(self):
        def on_bind(tipo, entorno, obj):
            obj.manipulated = 1

        def on_unbind(tipo, entorno, obj):
            obj.manipulated = 2

        e = EntornoSOL()
        e.on_pre_bind += on_bind
        e.on_pre_unbind += on_unbind
        ap1 = APU()
        ap1.manipulated = 0
        ap1.euros = 1000
        e.bind(ap1)
        self.assertEqual(1, ap1.manipulated)
        e.unbind(ap1)
        self.assertEqual(ap1.manipulated, 2)

    def test_generacion_xls(self):
        e = EntornoSOL()
        ap1 = APU()
        ap1.euros = 1000
        ap2 = APU()
        ap2.euros = -500
        ap3 = APU()
        ap3.euros = -500
        asi = Asiento(apuntes=[ap1, ap2, ap3])
        asi.vincular(e)
        f = StringIO()
        e.generar_xls_table('APU', f)

