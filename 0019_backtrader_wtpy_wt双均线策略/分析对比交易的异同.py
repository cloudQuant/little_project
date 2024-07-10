import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df1 = pd.read_csv("./transactions.csv")
df1.index = pd.to_datetime(df1['date'], format='%Y-%m-%d %H:%M:%S+00:00')
print(df1)

df2 = pd.read_csv(r"D:\source_code\wtpy_demos\monitor\bt_deploy\0002_cta_arbitrage_bt\outputs_bt\t1_rb_i\trades.csv")
df2['datetime'] = df2['time'].astype("str")
df2.index = pd.to_datetime(df2['datetime'], format="%Y%m%d%H%M")


print(df2)

lost_index = set(df1.index) - set(df2.index)

print(sorted(lost_index))