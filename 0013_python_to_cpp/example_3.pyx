#cython: language_level=3
#distutils: language=c++
#cython: c_string_type=unicode, c_string_encoding=utf8
import cython
import numpy as np
cimport numpy as np
# import pandas as pd
from libcpp.vector cimport vector

# 声明 C++ 函数
cdef extern from "example.hpp":
    double process_arr(double* arr, int rows, int cols)

# 定义 Cython 函数
cpdef process_numpy_data(np.ndarray[double, ndim=2] arr, rows, cols):
    cdef double* arr_ptr = &arr[0, 0]
    return process_arr(arr_ptr, rows, cols)