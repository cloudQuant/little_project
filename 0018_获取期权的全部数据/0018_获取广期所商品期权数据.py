import akshare as ak
import pandas as pd
from datetime import datetime, timedelta

# 获取商品期权合约代码
content = {
    "工业硅": "2022-12-23",
    "碳酸锂": "2023-07-24"
}
current_date = datetime.now().strftime('%Y-%m-%d')
for symbol in content:
    data = pd.DataFrame()
    begin_date = content[symbol]
    while begin_date < current_date:
        df1 = ak.option_gfex_daily(symbol=symbol, trade_date=begin_date)
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


