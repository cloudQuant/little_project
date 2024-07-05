import akshare as ak
import pandas as pd
from datetime import datetime, timedelta

# 获取商品期权合约代码
content = {
    "白糖期权": "2017-04-19",
    "棉花期权": "2019-01-28",
    "PTA期权": "2019-12-16",
    "甲醇期权": "2019-12-16",
    "菜籽粕期权": "2020-01-16",
    "动力煤期权": "2020-06-30",
    "菜籽油期权": "2022-08-26",
    "花生期权": "2022-08-26",
    "短纤期权": "2023-10-20",
    "纯碱期权": "2023-10-20",
    "锰硅期权": "2023-10-20",
    "硅铁期权": "2023-10-20",
    "尿素期权": "2023-10-20",
    "苹果期权": "2023-10-20"
}
current_date = datetime.now().strftime('%Y-%m-%d')
for symbol in content:
    data = pd.DataFrame()
    begin_date = content[symbol]
    while begin_date < current_date:
        df1 = ak.option_czce_daily(symbol=symbol, trade_date=begin_date)
        if df1 is not None:
            df1['date'] = begin_date
            data = pd.concat([data, df1], ignore_index=True)
        # 转换为 datetime 对象
        date_obj = datetime.strptime(begin_date, "%Y-%m-%d")
        # 获取下一个日期
        next_date_obj = date_obj + timedelta(days=1)
        # 转换回字符串
        begin_date = next_date_obj.strftime("%Y-%m-%d")
    data.to_csv(f"{symbol}.csv")
    print(f"{symbol}期权数据下载成功")
