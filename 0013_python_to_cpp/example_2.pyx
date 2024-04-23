#cython: language_level=3
#distutils: language=c++
#cython: c_string_type=unicode, c_string_encoding=utf8
import cython
import numpy as np
cimport numpy as np
# import pandas as pd
from libcpp.vector cimport vector

cdef extern from "example_2.hpp":
    double process_arr(const vector[vector[double]] & numpy_array,  int rows, int cols)


cdef vector[vector[double]] numpy_arrays_to_dataframe(np.ndarray[double, ndim=2] arr, int rows, int cols):
    cdef int i, j
    cdef vector[vector[double]] result
    cdef vector[double] row_arr
    row_arr.resize(cols)
    result.resize(rows,row_arr)
    # 使用内存视图访问NumPy数组数据
    cdef double[:, :] view = arr
    # 复制数据
    for i in range(rows):
        for j in range(cols):
            result[i][j] = view[i, j]

    return result

cpdef process_numpy_data(np.ndarray[double, ndim=2] numpy_array, int rows, int cols):
    # 转化numpy二维数组形成vector形式
    return process_arr(numpy_arrays_to_dataframe(numpy_array, rows, cols), rows, cols)