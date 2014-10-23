import unittest
from importasol.entorno import EntornoSOL
from importasol.db.contasol import APU, AutoAcumulador, MAE
from datetime import date


def crea_apu(**kwargs):
    apu = APU()
    for k, v in kwargs.iteritems():
        setattr(apu, k, v)
    return apu


def entorno_con_acumulador():
    e = EntornoSOL()
    ac = AutoAcumulador(e)
    for c in ['430', '43001234', '100', '47', '477', '47700001']:
        m = MAE()
        m.cuenta = c
        m.cB = "Test Account"
        e.bind(m)
    return e, ac


class TestEntorno(unittest.TestCase):
    def test_eventos(self):
        e, ac = entorno_con_acumulador()
        self.assertEqual(6, len(ac.saldos.keys()))
        m = MAE()
        m.cuenta = '4301'
        m.descripcion = "reprueba"
        e.bind(m)
        self.assertEqual(7, len(ac.saldos.keys()))
        e.unbind(m)
        self.assertEqual(6, len(ac.saldos.keys()))
        self.assertNotIn(m, e.get_tabla_elemento('MAE'))

    def test_afectador(self):
        e, ac = entorno_con_acumulador()
        self.assertEqual(0, len(ac.detectar_afectadas('43')))
        self.assertEqual(1, len(ac.detectar_afectadas('430')))
        self.assertEqual(2, len(ac.detectar_afectadas('43001234')))
        self.assertEqual(2, len(ac.detectar_afectadas('47700')))

    def test_acumulador(self):
        e, ac = entorno_con_acumulador()
        ap1 = crea_apu(debe=1000, fecha=date(2010, 1, 1), cuenta='20000000')
        e.bind(ap1)
        ap2 = crea_apu(debe=1000, fecha=date(2010, 2, 1), cuenta='10000000')
        e.bind(ap2)
        self.assertEqual(1000, ac.saldos.get('100').euros_2)
        e.unbind(ap2)
        self.assertEqual(0, ac.saldos.get('100').euros_2)
        ap3 = crea_apu(haber=1200, fecha=date(2010, 3, 5), cuenta='47700001')
        e.bind(ap3)
        self.assertEqual(-1200, ac.saldos.get('477').euros_3)
        ap4 = crea_apu(debe=300, fecha=date(2010, 3, 15), cuenta='47700001')
        e.bind(ap4)
        self.assertEqual(-900, ac.saldos.get('477').euros_3)
        e.unbind(ap3)
        self.assertEqual(300, ac.saldos.get('477').euros_3)
        self.assertEqual(300, ac.saldos.get('47700001').euros_3)

        sal = ac.saldos.get('477')
        c = sal._meta.fields.get('euros_3')
        debe = c.campo_debe.get_valor(sal)
        haber = c.campo_haber.get_valor(sal)
        self.assertEqual(0, haber)
        self.assertEqual(300, debe)
