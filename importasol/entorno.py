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
from .utiles import Event


class EntornoSOL(object):
    nivel_pgc = 8
    tablas = {}

    def __init__(self):
        self.tablas = dict()
        self.on_pre_bind = Event()
        self.on_pre_unbind = Event()
        self.on_post_bind = Event()
        self.on_post_unbind = Event()

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

    def find(self, tabla, **filtro):
        """ Busca dentro de la tabla.

        el elemento que coincida con lo indicado en ``filtro``.
        """
        t = self.get_tabla_elemento(tabla)
        if len(filtro) > 1:
            raise ValueError("Por ahora solo se buscar con una sola opcion")
        attr = filtro.keys()[0]
        val = filtro[attr]
        for it in t:
            if getattr(it, attr) == val:
                return it
        return None

    def bind(self, elemento):
        """ Vincular un elemento a este entorno. """
        if elemento.is_bound:
            if elemento.entorno == self:
                raise ValueError("El elemento ya esta vinculado a este entorno")
            elemento.entorno.unbind(elemento)
        self.on_pre_bind.fire(entorno=self, tipo=elemento._meta.tabla, obj=elemento)
        elemento.bind(self)
        tabla = self.get_tabla_elemento(elemento)
        tabla.append(elemento)
        self.on_post_bind.fire(entorno=self, tipo=elemento._meta.tabla, obj=elemento)

    def unbind(self, elemento):
        """ Desvincular un elemento de este entorno. """
        tabla = self.get_tabla_elemento(elemento)
        if elemento not in tabla:
            raise ValueError("No puedo desvincular un elemento que no esta vinculado a mi!")
        self.on_pre_unbind.fire(entorno=self, tipo=elemento._meta.tabla, obj=elemento)
        elemento.unbind()
        tabla = self.get_tabla_elemento(elemento)
        tabla.remove(elemento)
        self.on_post_unbind.fire(entorno=self, tipo=elemento._meta.tabla, obj=elemento)

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
            rowno = 0
            for row in rows:
                # if rowno == 0:
                    # row.__class__.to_xls_header(0, ws)
                    # rowno = 1
                try:
                    row.to_xls(rowno, ws)
                except:
                    logging.error("Error procesando tabla %s" % name)
                    raise
                rowno += 1
            wb.save(fname)
            logging.info("Tabla %s exportada" % name)
