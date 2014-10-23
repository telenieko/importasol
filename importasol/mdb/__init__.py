import pypyodbc
import logging
from ..utiles import dict_factory
log = logging.getLogger('importasol.mdb')


class EntornoMDB(object):
    rutamdb = None
    _connection = None

    def __init__(self, rutamdb):
        self.rutamdb = rutamdb

    def _get_connection(self):
        if self._connection:
            return self._connection
        connection_string = 'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=%s' % \
                            self.rutamdb
        self._connection = pypyodbc.connect(connection_string)
        return self._connection
    connection = property(_get_connection)

    def connect(self):
        info = self.getBasicInfo()
        log.info("Conectado a MDB: %s (%s) %s" % (info['codemp'], info['denemp'], info['ejeemp']))

    def close(self):
        self.connection.close()

    def getBasicInfo(self):
        cursor = self.connection.cursor()
        cursor.execute('SELECT CODEMP, DENEMP, EJEEMP, IVAEMP FROM F_EMP')
        row = cursor.fetchone()
        info = dict_factory(cursor, row)
        return info

    def getSeriesLast(self, serie):
        """ Devuelve el ultimo numero usado de una serie. """
        cursor = self.connection.cursor()
        cursor.execute('SELECT MAX(CODFAC) FROM F_FAC WHERE TIPFAC = ?', (serie, ))
        row = cursor.fetchone()
        if row[0] is None:
            return 0
        return int(row[0])

    def getServicios(self):
        cursor = self.connection.cursor()
        cursor.execute('''SELECT * FROM F_SER''')
        res = []
        for row in cursor:
            res.append(dict_factory(cursor, row))
        return res

    def getFPA(self, codfpa):
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM F_FPA WHERE CODFPA = ?', (codfpa, ))
        row = cursor.fetchone()
        if row is None:
            return None
        return dict_factory(cursor, row)

    def getClientes(self):
        cursor = self.connection.cursor()
        cursor.execute('''SELECT * FROM F_CLI''')
        res = []
        for row in cursor:
            res.append(dict_factory(cursor, row))
        return res

    def getCliente(self, codcli):
        """ Devuelve los datos de un cliente por codigo. """
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM F_CLI WHERE CODCLI = ?', (codcli, ))
        row = cursor.fetchone()
        if not row:
            return None
        return dict_factory(cursor, row)

    def getClienteByNIF(self, nifcli):
        """ Devuelve los datos de un cliente por nif. """
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM F_CLI WHERE NIFCLI = ?', (nifcli, ))
        row = cursor.fetchone()
        if not row:
            return None
        return dict_factory(cursor, row)

    def getTiposIVA(self):
        cursor = self.connection.cursor()
        cursor.execute('SELECT IVA1AUT, IVA2AUT, IVA3AUT FROM F_AUT WHERE CODAUT = 1')
        row = cursor.fetchone()
        return row
