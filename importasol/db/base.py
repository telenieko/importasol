import inspect
from .fields import CampoAlias, Campo

class Options(object):
    aliases = None
    model = None
    app_label = None
    table_name = None
    object_name = None
    model_name = None
    fields = None

    def __init__(self, meta, app_label=None, table_name=None):
        self.model = None
        self.app_label = app_label
        self.table_name = table_name
        self.meta = meta
        self.fields = {}

    def contribute_to_class(self, cls, name):
        cls._meta = self
        self.model = cls

        self.object_name = cls.__name__
        self.model_name = self.object_name.lower()
        self.original_attrs = {}

        if self.meta:
            meta_attrs = self.meta.__dict__.copy()
            for name in self.meta.__dict__.keys():
                if name.startswith('_'):
                    del meta_attrs[name]
            for attr_name in meta_attrs.keys():
                setattr(self, attr_name, meta_attrs.pop(attr_name))
                self.original_attrs[attr_name] = getattr(self, attr_name)
        del self.meta

    def add_field(self, field_name, field):
        self.fields.update({field_name: field})



class SOLFileBase(type):
    def __new__(cls, name, bases, attrs):
        super_new = super(SOLFileBase, cls).__new__
        
        # Comprobar que somos hijos de SOLFileBase
        parents = [b for b in bases if isinstance(b, SOLFileBase)]
        if not parents:
            return super_new(cls, name, bases, attrs)

        # Crear la clase
        module = attrs.pop('__module__')
        new_class = super_new(cls, name, bases, {'__module__': module})
        attr_meta = attrs.pop('Meta', None)

        if not attr_meta:
            meta = getattr(new_class, 'Meta', None)
        else:
            meta = attr_meta
        base_meta = getattr(new_class, '_meta', None)

        kwargs = {'app_label': module, 'table_name': name}
        new_class.add_to_class('_meta', Options(meta, **kwargs))

        for obj_name, obj in attrs.items():
            new_class.add_to_class(obj_name, obj)
        if new_class._meta.aliases:
            for de, a in new_class._meta.aliases:
                if len(a) == 1:
                    ca = "c%s" % a
                else:
                    ca = a
                campo = CampoAlias(ca)
                new_class.add_to_class(de,campo)

        return new_class

    def add_to_class(cls, name, value):
        # We should call the contribute_to_class method only if it's bound
        if not inspect.isclass(value) and hasattr(value, 'contribute_to_class'):
            value.contribute_to_class(cls, name)
        else:
            setattr(cls, name, value)


class SOLFile(object):
    __metaclass__ = SOLFileBase
    is_bound = False
    entorno = None

    class Meta:
        pass

    def bind(self, entorno):
        self.is_bound = True
        self.entorno = entorno
        for name, field in self._meta.fields.iteritems():
            field.bind(self, entorno)

    def unbind(self):
        for name, field in self._meta.fields.iteritems():
            field.unbind(self, self.entorno)
        self.is_bound = False
        self.entorno = None
        

