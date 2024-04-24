import numpy as np

# 创建一个示例数组
arr_row_major = np.arange(12).reshape((3, 4))  # 行主顺序
arr_col_major = np.arange(12).reshape((3, 4), order='F')  # 列主顺序

# 判断数组内存布局
flags_row_major = arr_row_major.flags
flags_col_major = arr_col_major.flags

print("Array with Row-major order ('C'):")
print(arr_row_major)
print("\nArray flags (Row-major order):")
print(flags_row_major)

print("\nArray with Column-major order ('F'):")
print(arr_col_major)
print("\nArray flags (Column-major order):")
print(flags_col_major)

# 检查数组的内存布局
if flags_row_major['C_CONTIGUOUS']:
    print("\nArray is stored in Row-major order ('C').")
elif flags_row_major['F_CONTIGUOUS']:
    print("\nArray is stored in Column-major order ('F').")

if flags_col_major['C_CONTIGUOUS']:
    print("\nArray is stored in Row-major order ('C').")
elif flags_col_major['F_CONTIGUOUS']:
    print("\nArray is stored in Column-major order ('F').")
