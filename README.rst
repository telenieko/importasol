ImportaSOL, Importa cualquier cosa en *SOL
******************************************

ImportaSOL es una pequeña libreria programada en Python para
facilitar la importación de datos en las aplicaciones de Sistemas
Multimedia (GestorSOL, ContaSOL, FacturaSOL, ...).

La librería facilita enormemente la generación de los archivos .XLS
adaptados a las notas técnicas proporcionadas con el software.

Pequeño ejemplo
===============

.. code-block:: python

    >>> from importasol.db.contasol import APU, Asiento, ContaSOL, AutoAcumulador, MAE
    >>> ap1 = APU()
    >>> ap1.cuenta = '430.231'
    >>> ap1.euros = 1000
    >>> ap2 = APU()
    >>> ap2.cuenta = '700.5'
    >>> ap2.euros = -500
    >>> ap3 = APU()
    >>> ap3.euros = -300
    >>> ap3.cuenta = '700.3'
    >>> asi = Asiento(apuntes=[ap1, ap2, ap3])
    >>> asi.renumera()

    >>> c = MAE()
    >>> c.codigo = '430.231'
    >>> c.descripcion = 'Cliente'

    >>> e = ContaSOL()
    >>> asi.vincular(e) # ídem de [e.bind(apu) for apu in [ap1, ap2, ap3]]
    >>> e.bind(c)
    >>> e.generar_xls('.')

Otros Ficheros
==============

No todos los ficheros / programas están soportados aún pero la base
está de modo que añadir nuevos ficheros es algo senzillísimo:

.. code-block:: python

    >>> from importasol.db.base import SOLFile
    >>> class Archivo(SOLFile)
    >>> from importasol.db.fields import CampoA, CampoT, CampoN, CampoF, CampoND, CampoV
    >>> from importasol.db.fields import CampoCuenta, CampoDebeHaber

    >>> class APU(SOLFile):
    >>>     cA = CampoN("Diario", size=3, default=1, required=True)
    >>>     cB = CampoF("Fecha", required=True)
    >>>     cC = CampoN("Asiento", size=5, default=0, required=True)
    >>>     cD = CampoN("Orden", size=6, required=True)
    >>>     cE = CampoCuenta("Cuenta", size=10, required=True)
    >>>     euros = CampoDebeHaber("Euros", 'I', 'J', editable=True)
    ...
    >>>
    >>>     class Meta:
    >>>         tabla = 'APU'
    >>>         aliases = (('dpto', 'O'), ('subdpto', 'P'))
