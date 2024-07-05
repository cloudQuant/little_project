import akshare as ak
import pandas as pd

# 获取商品期权合约代码
year_list = ["2021", "2022", "2023", "2024"]
czce_list = ["SR", "CF", "TA", "MA", "RM", "ZC"]
for symbol in czce_list:
    data = pd.DataFrame()
    for year in year_list:
        df = ak.option_czce_hist(symbol=symbol, year=year)
        data = pd.concat([data, df], ignore_index=True)
    data.to_csv(f"{symbol}.csv")
    print(f"{symbol}期权日线数据下载成功")
