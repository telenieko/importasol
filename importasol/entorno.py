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

import logging
import xlwt
import os


class EntornoSOL(object):
    nivel_pgc = 8
    tablas = {}

    def __init__(self):
        self.tablas = dict()

    def get_tabla_elemento(self, elemento):
        """ Obtener la tabla que corresponde a este elemento. """
        tablas = self.tablas
        if isinstance(elemento, type('')):
            nom = elemento
        else:
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
            raise ValueError("No puedo desvincular un elemento que no esta vinculado a mi!")
        elemento.unbind()
        tabla = self.get_tabla_elemento(elemento)
        tabla.remove(elemento)

    def create_xls(self, name):
        wb = xlwt.Workbook()
        ws = wb.add_sheet(name)
        return wb, ws

    def generar_xls(self, outdir):
        """ Generar los archivos XLS de cada tabla dentro de la carpeta ``outdir``. """
        for name, rows in self.tablas.iteritems():
            logging.info("Voy a procesar la tabla %s" % name)
            wb, ws = self.create_xls(name)
            fname = os.path.join(outdir, '%s.xls' % name)
            rowno = 1
            for row in rows:
                row.to_xls(rowno, ws)
                rowno += 1
            wb.save(fname)
            logging.info("Tabla %s exportada" % name)
