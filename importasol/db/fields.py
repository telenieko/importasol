import types
from decimal import Decimal
from datetime import date
from ..exceptions import ValidationError, ProgrammingError
from ..utiles import nivelar_cuenta


class Campo(object):
    field_name = None
    size = None
    required = None
    base_type = None
    default = None
    binding_required = None

    def __init__(self, nombre, size, default=None, required=False,
                 binding_required=False):
        self.nombre = nombre
        self.size = size
        self.required = required
        self.default = default
        self.binding_required = binding_required

    def is_valid(self, obj, value):
        raise ProgrammingError("Hay que implementar is_valid!!")

    def get_valor(self, obj):
        """ Devolver el valor que debe almacenarse en la Salida """
        if self.binding_required and not obj.is_bound:
            raise ProgrammingError(
                "%s tiene que estar enlazado a un entorno" % obj)
        return getattr(obj, self.field_name)

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
    pass


class CampoF(Campo):
    base_type = date

    def __init__(self, *args, **kwargs):
        kwargs.update({'size': 0})
        super(CampoF, self).__init__(*args, **kwargs)


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
    getter = None
    setter = None
    parametros = None

    def __init__(self, nombre, getter=None, setter=None,
                 parametros=tuple(), **kwargs):
        self.getter = getter
        self.setter = setter
        self.parametros = parametros
        if not 'size' in kwargs:
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
        return nivelar_cuenta(val, obj.entorno.nivel_pgc)
