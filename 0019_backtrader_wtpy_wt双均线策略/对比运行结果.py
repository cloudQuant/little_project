import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

bt_df = pd.read_csv("total_value.csv", index_col=0)
bt_df.columns = ['bt_value']
bt_df['datetime'] = pd.to_datetime(bt_df.index)
bt_df['date'] = bt_df['datetime'].dt.date
bt_df = bt_df.drop_duplicates("date")
bt_df.index = pd.to_datetime(bt_df['date'])
bt_df = bt_df[['bt_value']]
print(bt_df)

wt_df = pd.read_csv("wt_funds.csv")
wt_df['wt_value'] = wt_df['dynbalance'] + 1000000
wt_df.index = pd.to_datetime([str(i) for i in wt_df['date']])
print(wt_df)
result_df = pd.concat([bt_df, wt_df[['wt_value']]], axis=1, join="outer")

df = pd.read_csv("funds.csv")
df['wtpy_value'] = df['dynbalance'] + 1000000
df.index = pd.to_datetime([str(i) for i in wt_df['date']])
print(df)
result_df = pd.concat([bt_df, wt_df[['wt_value']], df[['wtpy_value']]], axis=1, join="outer")
print(result_df)

print(result_df.corr())

result_df.plot()
plt.show()


