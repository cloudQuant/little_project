import akshare as ak
import pandas as pd
end_month_list = ["1503", "1506", "1509", "1512",
                  "1603", "1606", "1609", "1612",
                  "1703", "1706", "1709", "1712",
                  "1803", "1806", "1809", "1812",
                  "1903", "1906", "1909", "1912",
                  "2003", "2006", "2009", "2012",
                  "2103", "2106", "2109", "2112",
                  "2203", "2206", "2209", "2212",
                  "2303", "2306", "2309", "2312",
                  "2403", "2406", "2409", "2412",]

result_list = []

for end_month in end_month_list:
    try:
        df = ak.option_finance_board(symbol="华夏上证50ETF期权", end_month=end_month)
        print(df)
        result_list.append(df)
    except Exception as e:
        print(end_month, "failed", e)
result_df = pd.concat(result_list)
result_df.to_csv("上证50ETF期权基本数据.csv")
print(result_df)