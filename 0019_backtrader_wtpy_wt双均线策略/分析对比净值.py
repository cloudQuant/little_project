import pandas as pd
import matplotlib.pyplot as plt
df = pd.read_csv("./total_value.csv", index_col=0)
df.index = pd.to_datetime(df.index)
df.index = [i.date() for i in df.index]
df.columns = ['value']
df['value'] = df['value'] - 1000000
# 识别重复的索引
duplicate_index = df.index.duplicated(keep='first')
# 删除重复的行
df = df[~duplicate_index]

# df.plot()

df2 = pd.read_csv(r"D:\source_code\wtpy_demos\monitor\bt_deploy\0002_cta_arbitrage_bt\outputs_bt\t1_rb_i\funds.csv", index_col=0)
df2.index = pd.to_datetime(df2.index, format="%Y%m%d")
df2.index = [i.date() for i in df2.index]
# df2[['dynbalance']].plot()
print(df)
print(df2)
data = pd.concat([df, df2[['dynbalance']]], axis=1)
# print(df2)
data.plot()
plt.show()
