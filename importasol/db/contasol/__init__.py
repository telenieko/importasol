from .otros import MAE, DEP, SDE, PRO
from .apu import APU
from .asi import Asiento
from .iva import IVS, IVR
from .sal import SAL, AutoAcumulador
from ...entorno import EntornoSOL


class ContaSOL(EntornoSOL):
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
        for s in self.get_tabla_elemento('SAL'):
            if len(s.cuenta) != self.nivel_pgc:
                continue
            if selector:
                if callable(selector) and not selector(self, s):
                    continue
                elif isinstance(selector, list) and s.cuenta not in selector:
                    continue
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
