import numpy as np
import pandas as pd
import example
import time

# 创建示例 NumPy 数组
numpy_array = np.array([
    [1.0, 2.0, 3.0, 4.0, 5.0],
    [1.1, 2.0, 3.0, 4.0, 5.0],
    [1.2, 2.0, 3.0, 4.0, 5.0],
    [1.3, 2.0, 3.0, 4.0, 5.0]
    ])

df = pd.DataFrame(numpy_array)
print(df)

# # 调用 Cython 函数处理 NumPy 数组
example.process_numpy_data(df.to_numpy(), 4, 5)