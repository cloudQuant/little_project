#cython: language_level=3
#distutils: language=c++
#cython: c_string_type=unicode, c_string_encoding=utf8
import cython
import numpy as np
cimport numpy as np
# import pandas as pd
from libcpp.vector cimport vector

cdef extern from "example_2.hpp":
    double process_numpy_array(const vector[double] & numpy_array, int size)

cpdef vector[double] arr_to_cppvector(np.ndarray[double, ndim=1] arr):
    cdef int i = 0;
    cdef int n = arr.shape[0];
    cdef double item;
    cdef vector[double] vec
    vec.reserve(n)  # 预先分配内存以避免重新分配
    for i in range(n):
        item = arr[i];
        vec.push_back(item)
    return vec



def process_numpy_data(np.ndarray[double, ndim=1] numpy_array, int size):
    # 获取 NumPy 数组,并转化成vector传递给c++函数
    return process_numpy_array(arr_to_cppvector(numpy_array), size)