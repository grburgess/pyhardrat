import os


from numpy.distutils.core import setup
from numpy.distutils.core import Extension


setup(

    name="pyhardrat",

    packages=['pyhardrat'],
    version='v0.1',
    description='GBM hardness ratio calculator',
    author='J. Michael Burgess',
    author_email='jmichaelburgess@gmail.com',

    requires=[
        'numpy',
        'astropy',
        'scipy',
        'threeML',
    ],
)

