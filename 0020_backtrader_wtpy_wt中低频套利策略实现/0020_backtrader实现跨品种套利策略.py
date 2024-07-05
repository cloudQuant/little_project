import pandas as pd
import numpy as np
import backtrader as bt
import datetime
import pyfolio as pf
import time
from backtrader.comminfo import ComminfoFuturesPercent, ComminfoFuturesFixed


class SmaStrategy(bt.Strategy):
    # params = (('short_window',10),('long_window',60))
    params = {"short_window": 10, "long_window": 60}

    def log(self, txt):
        """log信息的功能"""
        dt = bt.num2date(self.datas[0].datetime[0])
        print(f"{dt} ==> {txt}")

    def __init__(self):
        # 一般用于计算指标或者预先加载数据，定义变量使用
        self.short_ma = bt.indicators.SMA(self.datas[0].close, period=self.p.short_window)
        self.long_ma = bt.indicators.SMA(self.datas[0].close, period=self.p.long_window)

    def next(self):
        # Simply log the closing price of the series from the reference
        # self.log(f"工商银行,{self.datas[0].datetime.date(0)},收盘价为：{self.datas[0].close[0]}")
        # self.log(f"close:{self.datas[0].close[0]}, short_ma:{self.short_ma[0]},long_ma:{self.long_ma[0]}")
        # 得到当前的size
        size = self.getposition(self.datas[0]).size
        # 平空
        if size < 0 and self.short_ma[-1] < self.long_ma[-1] and self.short_ma[0] >= self.long_ma[0]:
            self.close(self.datas[0])
            size = 0
        # 平多
        if size > 0 and self.short_ma[-1] > self.long_ma[-1] and self.short_ma[0] <= self.long_ma[0]:
            self.close(self.datas[0])
            size = 0
        # 做多
        if size == 0 and self.short_ma[-1] < self.long_ma[-1] and self.short_ma[0] >= self.long_ma[0]:
            # 开仓
            self.buy(self.datas[0], size=1)

        # 做空
        if size == 0 and self.short_ma[-1] > self.long_ma[-1] and self.short_ma[0] <= self.long_ma[0]:
            self.sell(self.datas[0], size=1)


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


def run():
    begin_time = time.perf_counter()
    # 添加cerebro
    cerebro = bt.Cerebro()
    # 添加策略
    cerebro.addstrategy(SmaStrategy)
    # 准备数据
    params = dict(
        fromdate=datetime.datetime(2016, 1, 4),
        todate=datetime.datetime(2022, 3, 23),
        timeframe=bt.TimeFrame.Minutes,
        compression=5,
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
    data_path = './CFFEX.IF.HOT_m5.csv'
    df = pd.read_csv(data_path, encoding='gbk')
    df['datetime'] = df['date'] + " " + df['time']
    df.index = pd.to_datetime(df['datetime'])
    df['short_ma'] = df['close'].rolling(window=10).mean()
    df['long_ma'] = df['close'].rolling(window=60).mean()
    df.to_csv("均线计算结果.csv")
    df = df[['open', 'high', 'low', 'close', 'volume', 'open_interest']]
    df.columns = ['open', 'high', 'low', 'close', 'volume', 'openinterest']
    feed = bt.feeds.PandasDirectData(dataname=df, **params)
    # 添加合约数据
    cerebro.adddata(feed, name="index")
    comm = ComminfoFuturesPercent(commission=0.000023, margin=0.1, mult=300)
    cerebro.broker.addcommissioninfo(comm, name="index")
    # cerebro.broker.set_slippage_fixed(0.2, slip_open=True, slip_limit=True, slip_match=True, slip_out=False)
    # 添加资金
    cerebro.broker.setcash(1000000.0)

    cerebro.addanalyzer(bt.analyzers.TotalValue, _name='_TotalValue')
    cerebro.addanalyzer(bt.analyzers.PyFolio)
    # 开始运行
    results = cerebro.run()

    pyfoliozer = results[0].analyzers.getbyname('pyfolio')
    returns, positions, transactions, _ = pyfoliozer.get_pf_items()
    end_time = time.perf_counter()
    print("backtrader回测耗费的时间为", round(end_time - begin_time, 3), " 秒")
    returns.to_csv('returns.csv')
    positions.to_csv('positions.csv')
    transactions.to_csv('transactions.csv')
    total_value = pd.DataFrame([results[0].analyzers.getbyname('_TotalValue').get_analysis()]).T
    print(total_value)
    total_value.to_csv('total_value.csv')
    # pf.create_full_tear_sheet(
    #     returns,
    #     positions=positions,
    #     transactions=transactions,
    #     # gross_lev=gross_lev,
    #     live_start_date='2019-01-01',
    # )


if __name__ == '__main__':
    run()