from datetime import date
import unittest
from decimal import Decimal
from importasol.entorno import EntornoSOL
from fields import TestFile
from importasol.db.contasol import APU, Asiento
from StringIO import StringIO

class TestSortBy(unittest.TestCase):
    def apuntes(self):
        apus = [
            (date(2014, 1, 4), 2, 1, 'El sexto apunte'),
            (date(2014, 1, 4), 2, 1, 'El septimo apunte'),
            (date(2014, 1, 2), 3, 1, 'El cuarto apunte'),
            (date(2014, 1, 2), 3, 2, 'El quinto apunte'),
            (date(2014, 1, 1), 1, 1, 'El primer apunte'),
            (date(2014, 1, 1), 1, 2, 'El segundo apunte'),
            (date(2014, 1, 1), 1, 3, 'El tercer apunte'),
        ]
        apus2 = []
        for ap in apus:
            apu = APU()
            apu.fecha = ap[0]
            apu.asiento = ap[1]
            apu.orden = ap[2]
            apu.concepto = ap[3]
            apus2.append(apu)
        return apus2

    def test_unsorted(self):
        apus = self.apuntes()
        orig_sort = APU._meta.sort_by
        APU._meta.sort_by = None
        s = APU.sort_table(apus)
        orden_esperado = ('sexto', 'septimo', 'cuarto', 'quinto',
                          'primer', 'segundo', 'tercer')
        for ap, q in zip(apus, orden_esperado):
            t = 'El %s apunte' % q
            self.assertEqual(ap.concepto, t)
        APU._meta.sort_by = orig_sort

    def test_sorted(self):
        apus = self.apuntes()
        s = APU.sort_table(apus)
        orden_esperado = ('primer', 'segundo', 'tercer',
                          'cuarto', 'quinto', 'sexto', 'septimo')
        for ap, q in zip(apus, orden_esperado):
            t = 'El %s apunte' % q
            self.assertEqual(ap.concepto, t)
