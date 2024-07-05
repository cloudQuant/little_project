import akshare as ak
import pandas as pd
from datetime import datetime, timedelta

# 获取商品期权合约代码
content = {
    "铜期权": "2018-09-21",
    "天胶期权": "2019-01-28",
    "黄金期权": "2019-12-20",
    "铝期权": "2020-08-10",
    "锌期权": "2020-08-10",
    "原油期权": "2021-06-21"
}

current_date = datetime.now().strftime('%Y-%m-%d')
for symbol in content:
    data1 = pd.DataFrame()
    data2 = pd.DataFrame()
    begin_date = content[symbol]
    while begin_date < current_date:
        try:
            result = ak.option_shfe_daily(symbol=symbol, trade_date=begin_date)
            # print(result)
            if result is None:
                df1 = None
                df2 = None
            else:
                df1, df2 = result
        except Exception as e:
            print(e)
            df1 = df2 = None

        if df1 is not None:
            df1['date'] = begin_date
            data1 = pd.concat([data1, df1], ignore_index=True)
        if df2 is not None:
            df2['date'] = begin_date
            data2 = pd.concat([data2, df2], ignore_index=True)
        # print("df1 = ", df1)
        # print("df2 = ", df2)
        # 转换为 datetime 对象
        date_obj = datetime.strptime(begin_date, "%Y-%m-%d")
        # 获取下一个日期
        next_date_obj = date_obj + timedelta(days=1)
        # 转换回字符串
        begin_date = next_date_obj.strftime("%Y-%m-%d")
    data1.to_csv(f"{symbol}.csv")
    data2.to_csv(f"{symbol}_隐含波动率.csv")
    print(f"{symbol}期权数据下载成功")
