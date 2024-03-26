import Cython.Compiler.Options as Cco
import numpy as np
from Cython.Build import cythonize
from setuptools import setup, Extension

from backtrader.core.utils import (set_extra_link_args,
                                   set_cpp_version,
                                   set_optimize_option)

Cco.annotate = True

# -O3 -march=native
ext = Extension(
    "example", sources=["example.pyx"],
    include_dirs=[np.get_include()],
    language='c++',
    extra_compile_args=[
                set_optimize_option(2),
                # set_compile_args('openmp'),
                # set_compile_args('lpthread'),
                set_cpp_version('c++11'),
                # "-march=native"
    ],
    extra_link_args=[
        set_extra_link_args('lgomp'),
    ]
)

setup(name="example", ext_modules=cythonize([ext]))