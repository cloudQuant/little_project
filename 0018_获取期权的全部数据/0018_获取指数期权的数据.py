# -*- coding: utf-8 -*-
import os
import pandas as pd
import numpy as np
import akshare as ak

info_df = pd.read_csv("./所有品种合约的数据.csv", index_col=0, encoding="gbk")
info_df = info_df[info_df['type'] == "Option"]
symbol_list = [i for i in info_df['order_book_id'].tolist() if i.isnumeric()]
symbol_name_dict = dict(zip(info_df['order_book_id'].tolist(), info_df['symbol'].tolist()))
file_list = [i[:-4] for i in os.listdir('./指数期权/')]
for file in file_list:
    os.rename("./指数期权/" + file + ".csv", "./指数期权/" + file+"___"+symbol_name_dict[file] + ".csv")
assert 0
lost_symbol_list = []
data = pd.DataFrame()
for symbol in symbol_list:
    if symbol+"___"+symbol_name_dict[symbol] in file_list:
        continue
    try:
        df = ak.option_sse_daily_sina(symbol=symbol)
        df['code'] = symbol
        # data = pd.concat([data, df])
        df.to_csv("./指数期权/" + symbol+"___"+symbol_name_dict[symbol] + ".csv", encoding="utf-8")
        print(symbol, "下载成功")
    except Exception as e:
        print(symbol, e, "--------下载失败--------")
        lost_symbol_list.append(symbol)
print("lost_symbol_list", lost_symbol_list)

