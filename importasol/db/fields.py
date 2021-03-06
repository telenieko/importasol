import types
from decimal import Decimal
from datetime import date
from ..exceptions import ValidationError, ProgrammingError
from ..utiles import nivelar_cuenta
import datetime


class Campo(object):
    field_name = None
    size = None
    required = None
    base_type = None
    default = None
    binding_required = None
    auto_alias = None

    def __init__(self, nombre, size, default=None, required=False,
                 binding_required=False, auto_alias=True):
        self.nombre = nombre
        self.size = size
        self.required = required
        self.default = default
        self.binding_required = binding_required
        self.auto_alias = auto_alias

    def is_valid(self, obj, value):
        raise ProgrammingError("Hay que implementar is_valid!!")

    def get_valor(self, obj):
        """ Devolver el valor que debe almacenarse en la Salida """
        if self.binding_required and not obj.is_bound:
            raise ProgrammingError(
                "%s tiene que estar enlazado a un entorno" % obj)
        val = getattr(obj, self.field_name)
        return val

    def from_valor(self, obj, value):
        """ De un valor que viene de un archivo o BBDD ponerlo en el objeto. """
        if self.binding_required and not obj.is_bound:
            raise ProgrammingError(
                "%s tiene que estar enlazado a un entorno" % obj)
        return setattr(obj, self.field_name, value)

    def contribute_to_class(self, cls, field_name):
        self.field_name = field_name
        setattr(cls, field_name, None)
        cls._meta.add_field(field_name, self)
        if self.auto_alias is not False:
            if self.auto_alias is True:
                alias_name = self.nombre.lower()
                for a, b in ((' ', '_'), ('-', '_'), ('.', '')):
                    alias_name = alias_name.replace(a, b)
                self.crear_alias(cls, alias_name)
            else:
                self.crear_alias(cls, self.auto_alias)

    def crear_alias(self, cls, alias_name):
        ca = CampoAlias(self.field_name)
        ca.contribute_to_class(cls, alias_name)

    def bind(self, obj, entorno):
        pass

    def unbind(self, obj, entorno):
        pass


class CampoA(Campo):
    base_type = types.UnicodeType
    truncate = None

    def __init__(self, nombre, truncate=True, **kwargs):
        self.truncate = truncate
        return super(CampoA, self).__init__(nombre, **kwargs)

    def is_valid(self, obj):
        val = self.get_valor(obj)
        if len(val) > self.size:
            raise ValidationError(
                "El texto es mayor de lo permitido y truncate=False")
        return True

    def get_valor(self, obj):
        val = super(CampoA, self).get_valor(obj)
        if val and type(val) not in types.StringTypes:
            val = str(val)
        if self.truncate and val:
            return val[:self.size]
        else:
            return val


class CampoT(CampoA):
    def __init__(self, nombre, **kwargs):
        if 'size' in kwargs:
            raise ValueError("El CampoT siempre tiene un largo de 255!")
        kwargs.update({'size': 255})
        return super(CampoT, self).__init__(nombre, **kwargs)


class CampoND(Campo):
    base_type = Decimal
    pass


class CampoN(CampoND):
    base_type = types.IntType

    def is_valid(self, obj):
        val = self.get_valor(obj)
        if len(str(val)) > self.size:
            raise ValidationError(
                "El numero es mas largo que el limite")
        return True


class CampoB(CampoN):
    base_type = types.BooleanType

    def __init__(self, nombre, **kwargs):
        if 'size' in kwargs:
            raise ValueError("El CampoB siempre tiene un largo de 1")
        kwargs.update({'size': 1})
        return super(CampoB, self).__init__(nombre, **kwargs)

    def get_valor(self, obj):
        val = super(CampoB, self).get_valor(obj)
        if val is False:
            return 0
        elif val is True:
            return 1
        else:
            return val


class CampoF(Campo):
    base_type = date

    def __init__(self, *args, **kwargs):
        kwargs.update({'size': 0})
        super(CampoF, self).__init__(*args, **kwargs)

    def from_valor(self, obj, value):
        date = datetime.datetime(1899, 12, 30)
        get_ = datetime.timedelta(int(value))
        get_col2 = str(date + get_)[:10]
        d = datetime.datetime.strptime(get_col2, '%Y-%m-%d')
        fecha = d
        setattr(obj, self.field_name, fecha)


class CampoAlias(object):
    alias_de = None
    field_name = None

    def __init__(self, alias_de):
        self.alias_de = alias_de

    def contribute_to_class(self, cls, field_name):
        self.field_name = field_name
        p = property(self.getvalue, self.setvalue)
        setattr(cls, field_name, p)
        pass

    def getvalue(self, obj):
        return getattr(obj, self.alias_de)

    def setvalue(self, obj, value):
        return setattr(obj, self.alias_de, value)


class CampoV(Campo):

    """ CampoV, un campo virtual que obtiene su valor a partir de un metodo.

    El campo acepta un metodo ``getter`` y un ``setter`` parecidos a los de
    property(). El parametro ``parametros`` permite pasar parametros fijos
    al getter y el setter cuando se usen.

    Ejemplo:
        from importasol.contasol.apu import get_euros, set_euros
        euros = fields.CampoV('Euros', getter=get_euros, setter=set_euros,
                              parametros=('cA', 'cB'))

    Cuando leemos ``euros`` nos devuelve la suma de debe + haber (columnas A y B,
    de ahi los parametros). Cuando cambiamos su valor se guarda en A o B segun el
    signo.
    """

    getter = None
    setter = None
    parametros = None

    def __init__(self, nombre, getter=None, setter=None,
                 parametros=tuple(), **kwargs):
        self.getter = getter
        self.setter = setter
        self.parametros = parametros
        if 'size' not in kwargs:
            kwargs.update({'size': 0})
        return super(CampoV, self).__init__(nombre, **kwargs)

    def getvalue(self, obj):
        if self.getter is not None:
            val = self.getter(obj, *self.parametros)
            return val
        else:
            return None

    def setvalue(self, obj, value):
        if self.setter is not None:
            return self.setter(obj, value, *self.parametros)
        else:
            return None

    def contribute_to_class(self, cls, field_name):
        self.field_name = field_name
        p = property(self.getvalue, self.setvalue)
        setattr(cls, field_name, p)


class CampoCuenta(CampoA):
    def __init__(self, nombre, *args, **kwargs):
        if not 'binding_required' in kwargs.keys():
            kwargs.update({'binding_required': True})
        return super(CampoCuenta, self).__init__(nombre, *args, **kwargs)

    def get_valor(self, obj):
        val = super(CampoCuenta, self).get_valor(obj)
        if val is None:
            return None
        return nivelar_cuenta(val, obj.entorno.nivel_pgc)


class CampoDebeHaber(CampoV):

    """ CampoDebeHaber, un campo que saber que es el debe y el haber!. """

    def __init__(self, nombre, col_debe, col_haber, editable=True, **kwargs):
        self.col_debe = col_debe
        self.col_haber = col_haber
        if 'size' not in kwargs:
            kwargs.update({'size': 15})
        if editable:
            kwargs.update({'setter': self.set_saldo})
        super(CampoDebeHaber, self).__init__(nombre, getter=self.get_saldo, **kwargs)

    def get_saldo(self, obj):
        debe = self.campo_debe.get_valor(obj) or 0
        haber = self.campo_haber.get_valor(obj) or 0
        return (debe - haber)

    def set_saldo(self, obj, value):
        if value < 0:
            debe = None
            haber = abs(value)
        elif value > 0:
            debe = abs(value)
            haber = None
        else:
            debe = haber = None
        self.campo_debe.from_valor(obj, debe)
        self.campo_haber.from_valor(obj, haber)

    def contribute_to_class(self, cls, field_name):
        super(CampoDebeHaber, self).contribute_to_class(cls, field_name)
        campo_debe = CampoND("c%s" % self.col_debe, self.size, auto_alias=False)
        campo_haber = CampoND("c%s" % self.col_haber, self.size, auto_alias=False)
        cls._meta.add_field(field_name, self)
        campo_debe.contribute_to_class(cls, campo_debe.nombre)
        campo_haber.contribute_to_class(cls, campo_haber.nombre)

        if self.auto_alias:
            campo_debe.crear_alias(cls, '%s_debe' % field_name)
            campo_haber.crear_alias(cls, '%s_haber' % field_name)

        self.campo_debe = campo_debe
        self.campo_haber = campo_haber
