from string import join, ascii_letters


def nivelar_cuenta(cuenta, nivel):
    """ Nivelar una cuenta en formato XX.Y segun nivel
        >>> nivelar_cuenta('41.3', 8)
        u'41000003'
        >>> nivelar_cuenta('41.0003', 5)
        Traceback (most recent call last):
        ...
        ValueError: 41.0003, La cuenta es mas larga (7) del maximo permitido (5)
        >>> nivelar_cuenta('410003', 8)
        Traceback (most recent call last):
        ...
        ValueError: 410003, La cuenta es mas corta del nivel, y no tiene separador (.)
    """
    if cuenta.find('.') == -1 and len(cuenta) == nivel:
        return unicode(cuenta)
    if len(cuenta) > nivel:
        raise ValueError(
            "%s, La cuenta es mas larga (%s) del maximo permitido (%s)"
            % (cuenta, len(cuenta), nivel))
    if cuenta in ['', u'', None]:
        raise ValueError("No me diste ningun numero de cuenta...")
    if cuenta.find('.') == -1:
        raise ValueError(
            "%s, La cuenta es mas corta del nivel, y no tiene separador (.)"
            % cuenta)
    parts = cuenta.split('.')
    miss = nivel - (len(cuenta) - 1)
    val = parts[0] + join(['0' for i in range(0, miss)], '') + parts[1]
    return unicode(val)


def col2num(col):
    # http://stackoverflow.com/questions/7261936/convert-an-excel-or-spreadsheet-column-letter-to-its-number-in-pythonic-fashion
    num = 0
    for c in col:
        if c in ascii_letters:
            num = num * 26 + (ord(c.upper()) - ord('A')) + 1
    return num


def num_to_col_letters(num):
    # http://stackoverflow.com/questions/23861680/convert-spreadsheet-number-to-column-letter?rq=1
    div = num
    string = ""
    while div > 0:
        module = (div-1) % 26
        string = chr(65 + module) + string
        div = int((div - module)/26)
    return string


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class Event:
    # http://stackoverflow.com/a/1096614/1819160
    def __init__(self):
        self.handlers = set()

    def handle(self, handler):
        self.handlers.add(handler)
        return self

    def unhandle(self, handler):
        try:
            self.handlers.remove(handler)
        except:
            raise ValueError("Handler is not handling this event, so cannot unhandle it.")
        return self

    def fire(self, *args, **kargs):
        for handler in self.handlers:
            handler(*args, **kargs)

    def getHandlerCount(self):
        return len(self.handlers)

    __iadd__ = handle
    __isub__ = unhandle
    __call__ = fire
    __len__  = getHandlerCount
