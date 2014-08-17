from string import join

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
        raise ValueError, "%s, La cuenta es mas larga (%s) del maximo permitido (%s)" % (cuenta, len(cuenta), nivel)
    if cuenta in ['', u'', None]:
        raise ValueError, "No me diste ningun numero de cuenta..."
    if cuenta.find('.') == -1:
        raise ValueError, "%s, La cuenta es mas corta del nivel, y no tiene separador (.)" % cuenta
    parts = cuenta.split('.')
    miss = nivel - (len(cuenta) - 1)
    val = parts[0] + join(['0' for i in range(0, miss)], '') + parts[1]
    return unicode(val)

