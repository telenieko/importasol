#!/usr/bin/env python
# -*- coding: UTF-8 -*-

""" EntornoSOL

    El objeto de Entorno provee un marco común desde el que "coordinar" todas
    las tablas de una misma base de datos (ie: APU y MAE de una misma
    contabilidad).

    En el Entorno se encuentran los datos comunes como el nivel del plan de
    cuentas y es desde donde se lanza la generación de los archivos de salida.

    Los objetos derivados de SOLFile quedan "vinculados" a un entorno mediante
    "bind".
"""


class EntornoSOL(object):
    nivel_pgc = 8
    tablas = {}

    def __init__(self):
        self.tablas = dict()

    def get_tabla_elemento(self, elemento):
        """ Obtener la tabla que corresponde a este elemento. """
        tablas = self.tablas
        nom = elemento._meta.tabla
        if nom not in tablas.keys():
            tablas[nom] = []
        return tablas.get(nom)

    def bind(self, elemento):
        """ Vincular un elemento a este entorno. """
        if elemento.is_bound:
            if elemento.entorno == self:
                raise ValueError("El elemento ya esta vinculado a este entorno")
            elemento.entorno.unbind(elemento)
        elemento.bind(self)
        tabla = self.get_tabla_elemento(elemento)
        tabla.append(elemento)

    def unbind(self, elemento):
        """ Desvincular un elemento de este entorno. """
        tabla = self.get_tabla_elemento(elemento)
        if elemento not in tabla:
            raise ValueError(
                "No puedo desvincular un elemento que no esta vinculado a mi!")
        elemento.unbind()
        tabla = self.get_tabla_elemento(elemento)
        tabla.remove(elemento)
