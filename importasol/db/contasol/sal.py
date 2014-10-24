from ..base import SOLFile
from ..fields import CampoCuenta, CampoDebeHaber, Campo, CampoN
from ...utiles import num_to_col_letters, col2num
from decimal import Decimal


class CreadorSaldos(Campo):

    """ CreadorSaldos: Utilidad para crear los campos de Saldos.

    Este "campo" simplemente crea de golpe los campos de saldos de
    todos los meses de forma mas rapida que escribirlos todos a mano...
    """
    def __init__(self, nombre, inicial, **kwargs):
        self.inicial = inicial
        self.columnas_euro = {}
        super(CreadorSaldos, self).__init__(nombre, size=None, **kwargs)

    def crea_campo(self, cls, nombre, cd, ch, field_name):
        cd = num_to_col_letters(cd)
        ch = num_to_col_letters(ch)
        c = CampoDebeHaber(nombre, cd, ch, default=Decimal(0), auto_alias=False)
        c.contribute_to_class(cls, field_name)
        return c

    def contribute_to_class(self, cls, field_name):
        columna = col2num(self.inicial)
        ad = self.crea_campo(cls, "Saldo de apertura %s" % self.nombre,
                             columna, columna+1,
                             '%s_ape' % field_name)
        columna += 2
        for i in range(0, 12):
            mes = i + 1
            cd = columna + i*2
            ch = columna + i*2 + 1
            col = self.crea_campo(cls, "Saldo %d" % mes, cd, ch, "%s_%d" % (field_name, mes))
            self.columnas_euro.update({mes: col})
        columna += 24
        reg = self.crea_campo(cls, "Regularizacion %s" % self.nombre,
                              columna, columna+1, '%s_reg' % field_name)
        columna += 2
        cie = self.crea_campo(cls, "Cierre %s" % self.nombre,
                              columna, columna+1, '%s_reg' % field_name)
        self.columnas_euro.update({'ape': ad, 'reg': reg, 'cie': cie})


class AutoAcumulador(object):

    """ AutoAcumulador mantiene la tabla SAL sincronizada con la APU de un EntornoSOL.

    Si vinculamos un AutoAcumulador a un EntornoSOL este estara atentos a los (un)bind()
    manteniendo los saldos mensuales actualizados en todo momento.
    """

    def __init__(self, entorno):
        self.entorno = entorno
        self.cuentas = {}
        entorno.on_post_bind += self.handle_bind
        entorno.on_post_unbind += self.handle_unbind

    def handle_bind(self, entorno, tipo, obj):
        if tipo == 'APU':
            return self.handle_bind_apu(obj)
        elif tipo == 'MAE':
            return self.handle_bind_mae(obj)
        else:
            return None

    def handle_unbind(self, entorno, tipo, obj):
        if tipo == 'APU':
            return self.handle_unbind_apu(obj)
        elif tipo == 'MAE':
            return self.handle_unbind_mae(obj)
        else:
            return None

    def detectar_afectadas(self, cuenta):
        afectadas = []
        for i in range(0, len(cuenta)+1):
            c = cuenta[:i]
            if c in self.cuentas.keys():
                afectadas.append(c)
        return afectadas

    def sumar(self, sal, apu, valor=1):
        debe = (apu.debe or 0) * valor
        haber = (apu.haber or 0) * valor
        mes = apu.fecha.month
        campo = 'euros_%d' % mes
        field = SAL._meta.fields.get(campo)
        cd = field.campo_debe
        ch = field.campo_haber
        debe_ahora = cd.get_valor(sal) or 0
        haber_ahora = ch.get_valor(sal) or 0
        cd.from_valor(sal, debe_ahora + debe)
        ch.from_valor(sal, haber_ahora + haber)

    def handle_bind_apu(self, apu):
        afectadas = self.detectar_afectadas(apu.cuenta)
        for a in afectadas:
            diario = apu._meta.fields['cA'].get_valor(apu)
            s = self.get_sal(diario, a)
            self.sumar(s, apu)

    def handle_unbind_apu(self, apu):
        afectadas = self.detectar_afectadas(apu.cuenta)
        for a in afectadas:
            diario = apu._meta.fields['cA'].get_valor(apu)
            s = self.get_sal(diario, a)
            self.sumar(s, apu, -1)

    def get_sal(self, diario, cuenta):
        if cuenta not in self.cuentas:
            return None
        v = self.cuentas[cuenta]
        if diario not in v.keys():
            s = SAL()
            s.cA = cuenta
            s.diario = diario
            self.entorno.bind(s)
            v[diario] = s
        return v[diario]

    def handle_bind_mae(self, mae):
        self.cuentas[mae.cuenta] = {}

    def handle_unbind_mae(self, mae):
        s = self.cuentas.pop(mae.cuenta)
        for sal in s.values():
            self.entorno.unbind(sal)


class SAL(SOLFile):
    cA = CampoCuenta("Cuenta", size=10)
    euros = CreadorSaldos("euros", 'AF')
    cBJ = CampoN("Diario", size=3)

    def __str__(self):
        return unicode(self)

    def __unicode__(self):
        return u'SAL(%s)' % self.cuenta

    __repr__ = __str__

    class Meta:
        tabla = 'SAL'

