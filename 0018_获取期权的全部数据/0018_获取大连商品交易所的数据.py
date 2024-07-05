import akshare as ak
import pandas as pd
from datetime import datetime, timedelta

# 获取商品期权合约代码
content = {
    "豆粕期权": "2017-03-31",
    "玉米期权": "2019-01-28",
    "铁矿石期权": "2019-12-09",
    "液化石油气期权": "2020-03-30",
    "聚乙烯期权": "2020-07-06",
    "聚氯乙烯期权": "2020-07-06",
    "聚丙烯期权": "2020-07-06",
    "棕榈油期权": "2021-06-18",
    "黄大豆1号期权": "2022-08-08",
    "黄大豆2号期权": "2022-08-08",
    "豆油期权": "2022-08-08",
    "乙二醇期权": "2023-05-15",
    "苯乙烯期权": "2023-05-15"
}
current_date = datetime.now().strftime('%Y-%m-%d')
for symbol in content:
    data1 = pd.DataFrame()
    data2 = pd.DataFrame()
    begin_date = content[symbol]
    while begin_date < current_date:
        try:
            result = ak.option_dce_daily(symbol=symbol, trade_date=begin_date)
        except Exception as e:
            result = None
            print(e)
        df1 = None
        df2 = None
        if result is not None:
            df1, df2 = result
        if df1 is not None:
            df1['date'] = begin_date
            data1 = pd.concat([data1, df1], ignore_index=True)
        if df2 is not None:
            df2['date'] = begin_date
            data2 = pd.concat([data2, df2], ignore_index=True)
        # 转换为 datetime 对象
        date_obj = datetime.strptime(begin_date, "%Y-%m-%d")
        # 获取下一个日期
        next_date_obj = date_obj + timedelta(days=1)
        # 转换回字符串
        begin_date = next_date_obj.strftime("%Y-%m-%d")
    data1.to_csv(f"{symbol}.csv")
    data2.to_csv(f"{symbol}_隐含波动率.csv")
    print(f"{symbol}期权数据下载成功")
