from .otros import MAE, DEP, SDE, PRO
from .apu import APU
from .asi import Asiento
from .iva import IVS, IVR
from .sal import SAL, AutoAcumulador
from ...entorno import EntornoSOL
import logging

log = logging.getLogger('importasol.db.contasol')


class ContadorAsientos(object):
    def __init__(self, entorno, initial):
        self.entorno = entorno
        self.actual = initial
        entorno.on_pre_bind += self.handle_bind

    def next(self):
        self.actual += 1
        return self.actual

    def handle_bind(self, entorno, tipo, obj):
        if tipo != 'APU':
            return
        apu = obj
        if apu.asiento and apu.asiento > self.actual:
            self.actual = apu.asiento

    def recalcular(self):
        apus = self.entorno.get_tabla_elemento('APU')
        num = 0
        for apu in apus:
            if apu.asiento and apu.asiento > num:
                num = apu.asiento
        self.actual = num
        return num


class ContaSOL(EntornoSOL):
    def __init__(self, primer_asiento=1):
        super(ContaSOL, self).__init__()
        self.asinum = ContadorAsientos(self, initial=primer_asiento-1)

    def auto_cierre(self, saldo, fecha, contrapartida, texto, acumula=False, selector=None):
        """ Asiento de cierre automatico.

        ``saldo`` ha de ser un numero de mes, o ape, reg, cie. Indica
                  la columna de saldos a usar para el asiento.
        ``fecha`` es la fecha del asiento que haremos.
        ``contrapartida`` es la cuenta a la que enviamos el saldo resultante.
        ``texto`` texto de los apuntes
        ``selector`` puede ser un callable al que le pasamos el SAL y nos da True
                     o False segun si hay o no que incluirlo en el asiento.

        OJO, el Asiento no se vincula. Es cosa de uno mismo llamar a vincular()
        """
        diarios = {}
        meses = []
        if isinstance(saldo, list):
            pass
        elif saldo not in ['reg', 'cie']:
            if acumula:
                mes = int(saldo)
                meses += ['ape', ]
                meses += [str(m) for m in range(1, mes+1)]
            else:
                meses = [saldo, ]
        else:
            meses = ['ape', ]
            meses = meses + [str(m) for m in range(1, 13)]
            if saldo == 'cie':
                meses = meses + ['reg', ]
        log.debug("""ContaSOL.autocierre(%s, %s, %s, '%s', %s) meses=(%s), selector=(%s)""" %
                  (saldo, fecha, contrapartida, texto, acumula, meses, selector))
        for s in self.get_tabla_elemento('SAL'):
            if len(s.cuenta) != self.nivel_pgc:
                continue
            if selector is not None:
                if callable(selector):
                    if not selector(self, s):
                        continue
                elif isinstance(selector, list):
                    if s.cuenta not in selector:
                        continue
                else:
                    raise ValueError("No se trabajar con un selector de tipo %s" % type(selector))
            for m in meses:
                d = int(s.diario)
                if d not in diarios:
                    diarios[d] = {'suma': 0, 'asiento': Asiento(), 'cuentas': {}}
                cuentas = diarios[d]['cuentas']
                suma = diarios[d]['suma']
                asi = diarios[d]['asiento']
                if s.cuenta not in cuentas:
                    cuentas[s.cuenta] = 0
                field = s._meta.fields.get('euros_%s' % m)
                saldo = field.get_valor(s)
                cuentas[s.cuenta] += saldo
                suma += saldo
                diarios[d]['suma'] = suma
        for k, v in diarios.iteritems():
            suma = v['suma']
            asi = v['asiento']
            for cuenta, saldo in v['cuentas'].iteritems():
                if saldo == 0:
                    continue
                apu = APU()
                apu.fecha = fecha
                apu.diario = s.diario
                apu.concepto = texto
                apu.cuenta = cuenta
                apu.euros = saldo * -1
                asi.add(apu)
            if suma:
                apu = APU()
                apu.fecha = fecha
                apu.diario = k
                apu.concepto = texto
                apu.cuenta = contrapartida
                apu.euros = suma
                asi.add(apu)
        return [v['asiento'] for v in diarios.values()]


__all__ = [APU, MAE, Asiento, DEP, SDE, IVS, IVR, PRO, SAL, AutoAcumulador, ContaSOL]
