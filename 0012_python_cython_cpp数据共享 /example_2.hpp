#include <iostream>
#include <cmath>
#include <vector>
// 实现接收 NumPy 数组的 C++ 函数
double process_numpy_array(const std::vector<double> & numpy_array, int size) {
    // 在这里直接使用 NumPy 数组的数据，无需复制
    double sum = 0;
    for (int i = 0; i < size; ++i) {
        sum+=numpy_array[i];
    }
    double avg = sum/size;
    // std::cout << "avg = " << avg << std::endl;
    return avg;
}