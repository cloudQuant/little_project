// example.hpp

// 导入必要的头文件
#include <iostream>
#include <cmath>

double process_arr(double* arr, int rows, int cols) {
    double sum = 0;
    for (int i = 0; i < rows; ++i) {
        for (int j = 0; j < cols; ++j) {
            double v = arr[i * cols + j];
            sum += v;
        }
    }
    double avg = sum / (cols * rows);
    return avg;
}