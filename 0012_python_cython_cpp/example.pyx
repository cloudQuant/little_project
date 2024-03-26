# example.pyx
# 导入必要的库
import numpy as np
cimport numpy as np

# 定义 Cython 接口函数，接收 NumPy 数组并传递给 C++ 函数
# 定义 Cython 接口函数，接收 NumPy 数组并传递给 C++ 函数
cdef extern from "example.hpp":
    double process_numpy_array(double* numpy_array, int size)

def process_numpy_data(np.ndarray[double, ndim=1] numpy_array, int size):
    # 获取 NumPy 数组的数据指针并传递给 C++ 函数
    cdef double* data_pointer = <double*> numpy_array.data
    return process_numpy_array(data_pointer, size)