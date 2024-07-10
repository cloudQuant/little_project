# -*- coding: utf-8 -*-
"""
策略逻辑：
covered call 策略：
买入50ETF基金，同时卖出虚值看涨期权，获取权利金，降低持有50ETF的成本
"""

import datetime
import os
import re
import backtrader as bt  # backtrader
import pandas as pd
import pyfolio as pf
from backtrader.comminfo import ComminfoFuturesPercent, ComminfoFuturesFixed  # 期货交易的手续费用，按照比例或者按照金额
import quantstats as qs

# returns = pd.read_csv("./returns.csv", index_col=0)
# returns.index = [i.strftime("%Y-%m-%d") for i in pd.to_datetime(returns.index)]
# returns.index = pd.to_datetime(returns.index)
total_value = pd.read_csv("./total_value.csv", index_col=0)
total_value.index = [i.strftime("%Y-%m-%d") for i in pd.to_datetime(total_value.index)]
# 识别重复的索引
duplicate_index = total_value.index.duplicated(keep='first')
# 删除重复的行
total_value = total_value[~duplicate_index]
total_value.index = pd.to_datetime(total_value.index)
total_value.columns = ['value']
total_value['value'] = total_value['value']-1000000+20000
total_value['rate'] = total_value['value'].pct_change()
total_value = total_value.dropna()
total_value = total_value[total_value.index > pd.to_datetime("2017-06-30")]
print(total_value)


qs.reports.html(total_value['rate'],
                # benchmark=total_value['bench_rate'],
                output="rb_i_arbitrage_strategy.html",
                title="rb_i_arbitrage_strategy")
