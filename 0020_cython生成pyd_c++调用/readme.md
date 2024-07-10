### 实现

1. 编写my_adf.pyx, setup.py，实现需要的函数
2. 编写my_adf.h，把python函数转化成c++函数
3. 编写main.cpp, 调用my_adf函数

### 运行

```angular2html
// 编译出来pyd文件
python setup.py build_ext --inplace
// 编译main.cpp
g++ main.cpp -Ic:/anaconda3/include  -Lc:/anaconda3/libs -lpython312 -o main
// 运行main
./main
```
