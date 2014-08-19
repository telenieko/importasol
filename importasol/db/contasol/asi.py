class Asiento():
    apuntes = None
    numero = None

    def __init__(self, numero=None, apuntes=None):
        self.numero = numero
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

    def rm(self, apunte):
        self.apuntes.remove(apunte)

    def reordena(self):
        """ Ordenar la lista de apuntes segun el campo Orden de cada uno. """
        self.apuntes = sorted(self.apuntes, key=lambda apu: apu.orden)

    def renumera(self):
        """ Pone el Orden de cada apunte segun donde esta ahora de la lista. """
        i = 1
        for apu in self.apuntes:
            apu.orden = i
            i += 1

    def vincular(self, entorno):
        for apu in self.apuntes:
            entorno.bind(apu)

    def desvincular(self):
        for apu in self.apuntes:
            apu.entorno.unbind(apu)
