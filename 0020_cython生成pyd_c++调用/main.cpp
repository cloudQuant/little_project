// main.cpp
#include <iostream>
#include "my_adf.h"

int main() {
    std::vector<double> p = {0.1, 0.2, 0.4, 0.3, 0.2, 0.25, 0.1};
    auto r = my_c_function(p);
    std::cout << "ADF Statistic =  " << r[0] << std::endl;
    std::cout << "p-value =  " << r[1] << std::endl;
    std::cout << "Lags Used =  " << r[2] << std::endl;
    std::cout << "Number of Observations Used =  " << r[3] << std::endl;
    return 0;
}