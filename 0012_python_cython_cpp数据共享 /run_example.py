import numpy as np
import example
import example_2
import time
from pyecharts import options as opts
from pyecharts.charts import Bar

# 创建示例 NumPy 数组
numpy_array = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
# 调用 Cython 函数处理 NumPy 数组
example.process_numpy_data(numpy_array, 5)
example_2.process_numpy_data(numpy_array, 5)

def test_time_consume():
    time_result = []
    for n in [10000, 100000, 1000000]:
        # np.random.seed(n)
        arr = np.random.randn(n)

        # print("---------------这是原来cython的算法原型---------------------")
        total_time = 0
        r = 0
        for i in range(100):
            a = time.perf_counter()
            r = example.process_numpy_data(arr, n)
            b = time.perf_counter()
            total_time += (b - a)
            # print(f"cython耗费时间为:{b - a}")
        avg_time_1 = round(total_time / 100, 6)
        print("内存指针计算结果：", r)

        total_time = 0
        r = 0
        for i in range(100):
            a = time.perf_counter()
            r = example_2.process_numpy_data(arr, n)
            b = time.perf_counter()
            total_time += (b - a)
            # print(f"cython耗费时间为:{b - a}")
        avg_time_2 = round(total_time / 100, 6)
        print("转化成vector计算结果：", r)
        time_result.append([avg_time_1, avg_time_2])
    return time_result


if __name__ == '__main__':
    result = test_time_consume()
    print(result)
    c = (
        Bar()
        .add_xaxis(["1万行", "10万行", "100万行"])
        .add_yaxis("内存指针", [i[0] for i in result])
        .add_yaxis("转化vector", [i[1] for i in result])
        .reversal_axis()
        .set_series_opts(label_opts=opts.LabelOpts(position="right"))
        .set_global_opts(title_opts=opts.TitleOpts(title="耗费时间对比"))
        # .render("d:/result/夏普率耗费时间对比.html")
        .render("./绩效指标耗费时间对比.html")
    )