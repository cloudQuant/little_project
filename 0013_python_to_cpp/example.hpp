// example.hpp

// 导入必要的头文件
#include <iostream>
#include <cmath>

// 实现接收 NumPy 数组的 C++ 函数
double process_arr(double* arr, int rows, int cols) {
    // 在这里直接使用 NumPy 数组的数据，无需复制
    double sum = 0;
    for (int i = 0; i < rows; ++i) {
        std::cout << "[ ";
        for (int j = 0; j < cols; ++j)
            {
                int index = i * cols + j;
                double v = arr[index];
                sum+=v;
                std::cout << v << " ";
            }
        std::cout << "] " << std::endl;
    }
    double avg = sum/(cols*rows);
        std::cout << "avg = " << avg << std::endl;
    return avg;
}