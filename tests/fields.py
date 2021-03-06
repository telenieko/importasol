import unittest
from decimal import Decimal
from importasol.db import fields
from importasol.db.base import SOLFile
from importasol.db.contasol.apu import get_en_pesetas
from importasol.exceptions import ValidationError


class TestFile(SOLFile):
    cA = fields.CampoND("Debe", size=15)
    cB = fields.CampoND("Haber", size=15)
    cC = fields.CampoV("Pesetas", size=15, getter=get_en_pesetas, parametros=('euros', ))
    cD = fields.CampoA("Texto", size=5, truncate=True)
    cE = fields.CampoA("Text2", size=5, truncate=False)
    saldo = fields.CampoDebeHaber("apertura", 'F', 'G')
    euros = fields.CampoDebeHaber('Euros', 'A', 'B', editable=True)

    class Meta:
        tabla = 'TST'
        aliases = (('pesetas', 'cC'), )

    def __unicode__(self):
        return u"TestFile(%s : %s)" % (self.cA, self.cB)

    __str__ = __unicode__


class TestCampoA(unittest.TestCase):
    def test_truncamiento(self):
        tf = TestFile()
        cD = tf._meta.fields.get('cD')
        cE = tf._meta.fields.get('cE')
        tf.cD = '1234567890'
        self.assertEqual(True, cD.is_valid(tf))
        self.assertEqual('12345', cD.get_valor(tf))
        tf.cE = '1234567890'
        self.assertRaises(ValidationError, cE.is_valid, tf)
        self.assertEqual('1234567890', cE.get_valor(tf))


class TestCampoVirtual(unittest.TestCase):
    def test_campo_pesetas(self):
        tf = TestFile()
        self.assertEqual(0, tf.cC)
        tf.cA = 1000
        self.assertEqual(Decimal('166386'), tf.cC)
        tf.cA = ''
        tf.cB = 100
        self.assertEqual(Decimal('-16638.6'), tf.cC)

    def test_dos_no_son_lo_mismo(self):
        tf1 = TestFile()
        tf2 = TestFile()
        tf1.euros = 1000
        tf2.euros = -100
        self.assertEqual(1000, tf1.cA)
        self.assertEqual(100, tf2.cB)
        self.assertEqual(1000, tf1.euros)
        self.assertEqual(-100, tf2.euros)


class TestCampoAlias(unittest.TestCase):
    def test_campo_alias(self):
        tf = TestFile()
        tf.euros = 1000
        self.assertEqual(166386, tf.pesetas)

    def test_auto_alias(self):
        tf = TestFile()
        tf.texto = "Hola"
        self.assertEqual("Hola", tf.cD)


class TestCampoDebeHaber(unittest.TestCase):
    def test_campo_debe_haber(self):
        tf = TestFile()
        attrs = dir(tf)
        for a in ['saldo_debe', 'cF', 'saldo_haber', 'cG']:
            self.assertIn(a, attrs)
        tf.saldo_debe = 100
        tf.saldo_haber = 150
        self.assertEqual(tf.saldo, -50)

    def test_campo_euro(self):
        tf = TestFile()
        self.assertEqual(0, tf.euros)
        tf.euros = 1000
        self.assertEqual(1000, tf.cA)
        self.assertEqual(None, tf.cB)
        tf.euros = -100
        self.assertEqual(None, tf.cA)
        self.assertEqual(100, tf.cB)
        tf.euros = 0
        self.assertEqual(None, tf.cA)
        self.assertEqual(None, tf.cB)
