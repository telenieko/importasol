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
            if selector and not selector(s):
                continue
            for m in meses:
                d = int(s.diario)
                if d not in diarios:
                    diarios[d] = {'suma': 0, 'asiento': Asiento()}
                suma = diarios[d]['suma']
                asi = diarios[d]['asiento']
                field = s._meta.fields.get('euros_%s' % m)
                debe = field.campo_debe.get_valor(s)
                haber = field.campo_haber.get_valor(s)
                if debe:
                    apu = APU()
                    apu.fecha = fecha
                    apu.diario = s.diario
                    apu.concepto = texto
                    apu.cuenta = s.cuenta
                    apu.haber = debe
                    asi.add(apu)
                    suma += debe
                if haber:
                    apu = APU()
                    apu.fecha = fecha
                    apu.diario = s.diario
                    apu.concepto = texto
                    apu.cuenta = s.cuenta
                    apu.debe = haber
                    suma -= haber
                    asi.add(apu)
                diarios[d]['suma'] = suma
                diarios[d]['asiento'] = asi
        for k, v in diarios.iteritems():
            suma = v['suma']
            asi = v['asiento']
            apu = APU()
            apu.fecha = fecha
            apu.diario = k
            apu.concepto = texto
            apu.cuenta = contrapartida
            apu.euros = suma
            asi.add(apu)
        return [v['asiento'] for v in diarios.values()]


__all__ = [APU, MAE, Asiento, DEP, SDE, IVS, IVR, PRO, SAL, AutoAcumulador, ContaSOL]
