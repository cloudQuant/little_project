import datetime
import talib
import pandas as pd
# 核心代码部分
from tsfresh import extract_features
from tsfresh.utilities.dataframe_functions import roll_time_series

start_time = datetime.datetime.now()  # 开始时间

data = pd.read_csv("D:/data/1m/okex-ACH-USDT-SWAP-1m.csv")
data['code'] = 'okex-ACH-USDT-SWAP-1m'
data = data.loc[:4000,]
# 收盘价的斜率
data['slope'] = talib.LINEARREG_SLOPE(data['c'].values, timeperiod=5)
# 相对强弱指标
data['rsi'] = talib.RSI(data['c'].values, timeperiod=14)
# 威廉指标值
data['wr'] = talib.WILLR(data['h'].values,
                         data['l'].values,
                         data['c'].values, timeperiod=7)
# MACD中的DIF、DEA和MACD柱
data['dif'], data['dea'], data['macd'] = talib.MACD(data['c'].values,
                                                    fastperiod=12,
                                                    slowperiod=26,
                                                    signalperiod=9)
# 抛物线指标
data['sar'] = talib.SAR(data['h'].values, data['l'].values)
# 删除开盘价、最高价和最低价
data = data.drop(columns=['o', 'h', 'l']).fillna(method='ffill').dropna().reset_index(drop=True)
print(data)
data_roll = roll_time_series(data, column_id='code', column_sort='ts', max_timeshift=20, min_timeshift=5).drop(
    columns=['code'])
data_feat = extract_features(data_roll, column_id='id', column_sort='ts')

end_time = datetime.datetime.now()  # 结束时间
print('开始时间：', start_time.strftime('%Y-%m-%d %H:%M:%S'))
print('结束时间：', end_time.strftime('%Y-%m-%d %H:%M:%S'))
print('耗时：%d 秒' % (end_time - start_time).seconds)
print('原始数据维度：', data.shape)
print('特征提取后维度：', data_feat.shape)
