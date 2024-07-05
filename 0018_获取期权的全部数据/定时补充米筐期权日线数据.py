import os
import re
import rqdatac
import pandas as pd
from datetime import datetime


def get_contract_number(contract_string):
    # 使用正则表达式提取数字部分
    match = re.search(r'\d+', contract_string)
    if match:
        contract_number = match.group(0)
    else:
        contract_number = None
    return contract_number


# 获取当前所有的文件
data_root = "E:\\data\\option\\ricequant\\day\\"
file_list = list(os.listdir(data_root))
print(file_list)
# 获取所有的期货合约信息
info_df = pd.read_csv("./所有品种合约的数据.csv", index_col=0, encoding="gbk")
info_df = info_df[info_df['type'] == "Option"]

# 循环所有的合约,并进行下载
rqdatac.init('13383713859', '123456')
print(rqdatac.user.get_quota())

for index, row in info_df.iterrows():
    name = row['order_book_id']
    number = get_contract_number(name)
    try:
        begin_date = row['listed_date']
        end_date = row['de_listed_date']
        if begin_date == "0000-00-00":
            begin_date = "2010-01-01"
        # 获取当前日期并格式化为字符串
        current_date = datetime.now().strftime('%Y-%m-%d')
        if end_date == "0000-00-00":
            end_date = current_date
        if name + ".csv" not in file_list:
            df = rqdatac.get_price(name, start_date=begin_date, end_date=end_date, frequency='1d')
            if df is not None:
                df.to_csv(data_root + name + ".csv")
                print(f"{name}合约下载成功，数据长度为{len(df)}")
            else:
                print(f"{name}合约下载失败")
        else:
            pre_df = pd.read_csv(data_root + name + ".csv", index_col=0)
            datetime_list = list(pre_df['datetime'])
            first_time = datetime_list[0]
            last_time = datetime_list[-1]
            begin_date = pd.to_datetime(end_date, format="%d/%m/%Y").date()
            d1 = pd.to_datetime(end_date, format="%d/%m/%Y").date()
            d2 = pd.to_datetime(last_time).date()
            # print(f"name = {name}, d1 = {d1}, d2 = {d2}")
            if d1 > d2:
                # print(pre_df)
                df = rqdatac.get_price(name, start_date=d2.strftime("%Y-%m-%d"), end_date=d1.strftime("%Y-%m-%d"), frequency='1d')
                df = df.reset_index()
                df = df.drop(columns=['order_book_id', "trading_date"])
                df = pd.concat([pre_df, df])
                df = df.drop_duplicates("datetime")
                df.index = range(len(df))
                df.to_csv(data_root + name + '.csv')
                print(f"{name}合约数据补充成功")
                # assert 0
    except Exception as e:
        print(e, name)