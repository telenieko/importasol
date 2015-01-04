""" setup.py file. """
import os
from setuptools import setup

def read(fname):
    """ Utility function to read the README file.
    Used for the long_description.  It's nice, because now 1) we have a top level
    README file and 2) it's easier to type in the README file than to put a raw
    string in below ...
    """
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="importasol",
    version="0.0.1",
    author="Marc Fargas",
    author_email="marc@marcfargas.com",
    description=("Libreria para generar archivos XLS importables "
                 "en las apliaciones *SOL (ContaSOL, ...)."),
    license = "BSD",
    keywords = "accounting contasol etl",
    url = "http://packages.python.org/importasol",
    packages=['importasol', 'tests'],
    long_description=read('README.rst'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
    install_requires=[
        "xlwt==0.7.5",
    ]
)
