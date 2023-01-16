import os
import sys
from distutils.core import setup
from distutils.extension import Extension
from pathlib import Path

from Cython.Build import build_ext

setup(
    name = 'Sample Program',
    cmdclass = {'build_ext': build_ext},                     
    ext_modules = [Extension("secrets", ["secrets.py"])]
)