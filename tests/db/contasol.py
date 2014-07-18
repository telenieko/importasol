import unittest
from decimal import Decimal
from importasol.db import fields
from importasol.db.base import SOLFile
from importasol.db import contasol
from importasol.db.contasol import APU, Asiento
from importasol.exceptions import ValidationError


class TestAsiento(unittest.TestCase):
    def test_add_rm(self):
        ap1 = APU()
        ap1.euros = 1000
        ap2 = APU()
        ap2.euros = -500
        ap3 = APU()
        ap3.euros = -500
        asi = Asiento(apuntes=[ap1, ap2, ap3])
        asi.rm(ap3)
        self.assertRaises(ValueError, asi.rm, ap3)
        asi.add(ap3)
        self.assertRaises(ValueError, asi.add, ap3)

    def test_descuadre(self):
        ap1 = APU()
        ap1.euros = 1000
        ap2 = APU()
        ap2.euros = -500
        ap3 = APU()
        ap3.euros = -500
        asi = Asiento(apuntes=[ap1, ap2, ap3])
        self.assertEqual(0, asi.descuadre)
        ap3.euros = -300
        self.assertEqual(200, asi.descuadre)

    def test_cuadra(self):
        ap1 = APU()
        ap1.euros = 1000
        ap2 = APU()
        ap2.euros = -500
        ap3 = APU()
        ap3.euros = -500
        asi = Asiento(apuntes=[ap1, ap2, ap3])
        self.assertEqual(True, asi.cuadra())
        ap3.euros = -300
        self.assertEqual(False, asi.cuadra())

    def test_renumera(self):
        ap1 = APU()
        ap1.euros = 1000
        ap2 = APU()
        ap2.euros = -500
        ap3 = APU()
        ap3.euros = -300
        asi = Asiento(apuntes=[ap1, ap2, ap3])
        asi.renumera()
        self.assertEquals([1, 2, 3],
                [ap.orden for ap in asi.apuntes])
        asi2 = Asiento(apuntes=[ap2, ap3, ap1])
        asi2.renumera()
        self.assertEquals([1, 2, 3],
                [ap.orden for ap in asi2.apuntes])
        self.assertEquals([3, 1, 2],
                [ap.orden for ap in asi.apuntes])

    def test_reordena(self):
        ap1 = APU()
        ap1.euros = 1000
        ap2 = APU()
        ap2.euros = -500
        ap3 = APU()
        ap3.euros = -300
        asi = Asiento(apuntes=[ap1, ap2, ap3])
        asi.renumera()
        ap2.orden = 100
        asi.reordena()
        self.assertEquals([1000, -300, -500],
                [ap.euros for ap in asi.apuntes])
        ap1.orden = 50
        asi.reordena()
        self.assertEquals([-300, 1000, -500],
                [ap.euros for ap in asi.apuntes])


