import unittest
from decimal import Decimal
from importasol.db import fields
from importasol.db.base import SOLFile
from importasol.db import contasol
from importasol.db.contasol import APU, Asiento, ContaSOL, AutoAcumulador, MAE
from importasol.exceptions import ValidationError
from importasol.utiles import print_diario
from datetime import date


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


def auto_crea_cuentas(entorno, tipo, obj):
    if tipo == 'APU':
        apu = obj
        c = apu.cuenta
        for cue in entorno.get_tabla_elemento('MAE'):
            if cue.cuenta == c:
                return
        cue = MAE()
        cue.cuenta = c
        cue.descripcion = "cuenta magica"
        entorno.bind(cue)


def solo_pyg(entorno, sal):
    if sal.cuenta[0] not in ['6', '7']:
        return False
    return True


class TestContaSOL(unittest.TestCase):
    def test_autocierre(self):
        e = ContaSOL()
        e.on_pre_bind += auto_crea_cuentas
        AutoAcumulador(e)
        for c, importe in (('43000000', 1000), ('70000000', -1000)):
            apu = APU(euros=importe, cuenta=c, fecha=date(2010, 2, 1), concepto="Apu a")
            e.bind(apu)
        for c, importe in (('41000000', -500), ('60000000', 500)):
            apu = APU(euros=importe, cuenta=c, fecha=date(2010, 2, 2), concepto="Apu b")
            e.bind(apu)
        for c, importe in (('43000000', -1000), ('57000000', 1000)):
            apu = APU(euros=importe, cuenta=c, fecha=date(2010, 3, 2), concepto="Apu c")
            e.bind(apu)
        for c, importe in (('41000000', 500), ('57000000', -500)):
            apu = APU(euros=importe, cuenta=c, fecha=date(2010, 4, 2), concepto="Apu d")
            e.bind(apu)
        print_diario(e.get_tabla_elemento('APU'))
        reg = e.auto_cierre('reg', date(2010, 12, 31), '12900001', 'Regularizar', selector=solo_pyg)
        asi = reg[0]
        self.assertEqual(-500, asi.apuntes[-1].euros)
        asi.vincular(e)
        cie = e.auto_cierre('cie', date(2010, 12, 31), '90000001', 'Cierre')
        self.assertEqual(2, len(cie[0].apuntes))
        cie[0].vincular(e)
        print_diario(e.get_tabla_elemento('APU'))
