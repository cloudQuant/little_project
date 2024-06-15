import pandas as pd
import numpy as np
import backtrader as bt
import datetime


class SmaStrategy(bt.Strategy):
    # params = (('short_window',10),('long_window',60))
    params = {"short_window": 10, "long_window": 60}

    def log(self, txt, dt=None):
        ''' log信息的功能'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # 一般用于计算指标或者预先加载数据，定义变量使用
        self.short_ma = bt.indicators.SMA(self.datas[0].close, period=self.p.short_window)
        self.long_ma = bt.indicators.SMA(self.datas[0].close, period=self.p.long_window)

    def next(self):
        # Simply log the closing price of the series from the reference
        # self.log(f"工商银行,{self.datas[0].datetime.date(0)},收盘价为：{self.datas[0].close[0]}")
        # self.log(f"short_ma:{self.short_ma[0]},long_ma:{self.long_ma[0]}")
        # 得到当前的size
        size = self.getposition(self.datas[0]).size
        # 做多
        if size == 0 and self.short_ma[-1] < self.long_ma[-1] and self.short_ma[0] > self.long_ma[0]:
            # 开仓
            self.order_target_value(self.datas[0], target=50000)
        # 平多
        if size > 0 and self.short_ma[-1] > self.long_ma[-1] and self.short_ma[0] < self.long_ma[0]:
            self.close(self.datas[0])

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # order被提交和接受
            return
        if order.status == order.Rejected:
            self.log(f"order is rejected : order_ref:{order.ref}  order_info:{order.info}")
        if order.status == order.Margin:
            self.log(f"order need more margin : order_ref:{order.ref}  order_info:{order.info}")
        if order.status == order.Cancelled:
            self.log(f"order is concelled : order_ref:{order.ref}  order_info:{order.info}")
        if order.status == order.Partial:
            self.log(f"order is partial : order_ref:{order.ref}  order_info:{order.info}")
        # Check if an order has been completed
        # Attention: broker could reject order if not enougth cash
        if order.status == order.Completed:
            if order.isbuy():
                self.log("buy result : buy_price : {} , buy_cost : {} , commission : {}".format(
                    order.executed.price, order.executed.value, order.executed.comm))

            else:  # Sell
                self.log("sell result : sell_price : {} , sell_cost : {} , commission : {}".format(
                    order.executed.price, order.executed.value, order.executed.comm))

    def notify_trade(self, trade):
        # 一个trade结束的时候输出信息
        if trade.isclosed:
            self.log('closed symbol is : {} , total_profit : {} , net_profit : {}'.format(
                trade.getdataname(), trade.pnl, trade.pnlcomm))
        if trade.isopen:
            self.log('open symbol is : {} , price : {} '.format(
                trade.getdataname(), trade.price))


# 添加cerebro
cerebro = bt.Cerebro()
# 添加策略
cerebro.addstrategy(SmaStrategy)
# 准备数据
params = dict(
    fromdate=datetime.datetime(2006, 10, 27),
    todate=datetime.datetime(2020, 8, 14),
    timeframe=bt.TimeFrame.Days,
    compression=1,
    # dtformat=('%Y-%m-%d %H:%M:%S'),
    # tmformat=('%H:%M:%S'),
    datetime=0,
    high=2,
    low=3,
    open=1,
    close=4,
    volume=5,
    openinterest=6)
# 数据的地址，使用自己的数据地址
data_path = 'C:/data/股票/零散/工商银行.csv'
df = pd.read_csv(data_path, encoding='gbk')
df = df[['日期', '开盘价', '最高价', '最低价', '收盘价', '成交量', '成交金额']]
df.columns = ['datetime', 'open', 'high', 'low', 'close', 'volume', 'openinterest']
df = df.sort_values("datetime")
df.index = pd.to_datetime(df['datetime'])
df = df[['open', 'high', 'low', 'close', 'volume', 'openinterest']]
feed = bt.feeds.PandasDirectData(dataname=df, **params)
# 添加合约数据
cerebro.adddata(feed, name="gsyh")
cerebro.broker.setcommission(commission=0.0005)

# 添加资金
cerebro.broker.setcash(100000.0)

# 开始运行
cerebro.run()

# 打印相关信息
cerebro.plot()