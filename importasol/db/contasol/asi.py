class Asiento():
    apuntes = None
    _numero = 0

    def __str__(self):
        return unicode(self)

    def __unicode__(self):
        s = u'Asiento(\n'
        for apu in self.apuntes:
            s += u'\t%s\n' % unicode(apu)
        s += '\t)'
        return s

    def _get_numero(self):
        return self._numero

    def _set_numero(self, val):
        for a in self.apuntes:
            a.asiento = val
        self._numero = val
    numero = property(_get_numero, _set_numero)

    def __init__(self, numero=None, apuntes=None):
        self._numero = numero
        self.apuntes = []
        if apuntes:
            for apu in apuntes:
                self.apuntes.append(apu)

    def _get_descuadre(self):
        valor = 0
        for apu in self.apuntes:
            valor += apu.euros
        return valor
    descuadre = property(_get_descuadre)

    def cuadra(self):
        if self.descuadre != 0:
            return False
        return True

    def add(self, apunte):
        if apunte in self.apuntes:
            raise ValueError("Apunte duplicado en el asiento")
        self.apuntes.append(apunte)
        apunte.asi = self
        apunte.asiento = self.numero

    def rm(self, apunte):
        self.apuntes.remove(apunte)
        apunte.asi = None
        apunte.asiento = 0

    def reordena(self):
        """ Ordenar la lista de apuntes segun el campo Orden de cada uno. """
        self.apuntes = sorted(self.apuntes, key=lambda apu: apu.orden)

    def renumera(self):
        """ Pone el Orden de cada apunte segun donde esta ahora de la lista. """
        i = 1
        for apu in self.apuntes:
            apu.orden = i
            i += 1

    def vincular(self, entorno, autonum=False):
        if autonum:
            self._set_numero(entorno.asinum.next())
        for apu in self.apuntes:
            entorno.bind(apu)

    def desvincular(self):
        for apu in self.apuntes:
            apu.entorno.unbind(apu)

    def copy(self, invertido=False):
        nuevo = self.__class__()
        for apu in self.apuntes:
            ap = apu.copy()
            if invertido:
                ap.euros = ap.euros * -1
            nuevo.add(ap)
        return nuevo
