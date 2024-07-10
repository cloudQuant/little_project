import pandas as pd
import numpy as np
import backtrader as bt
import datetime
import pyfolio as pf
import statsmodels.tsa.stattools as ts
import time
from backtrader.comminfo import ComminfoFuturesPercent, ComminfoFuturesFixed


class SmaStrategy(bt.Strategy):
    # params = (('short_window',10),('long_window',60))
    params = {"look_back_num": 360, "threshold": 2}

    def log(self, txt):
        """log信息的功能"""
        dt = bt.num2date(self.datas[0].datetime[0])
        print(f"{dt} ==> {txt}")

    def __init__(self):
        # 一般用于计算指标或者预先加载数据，定义变量使用
        # self.short_ma = bt.indicators.SMA(self.datas[0].close, period=self.p.short_window)
        # self.long_ma = bt.indicators.SMA(self.datas[0].close, period=self.p.long_window)
        self.beta = 1
        self.c = 0
        self.resid = 0
        self.can_trade = False
        self.up = np.inf
        self.down = -np.inf
        self.mean = None
        self.leg_pos = 0
        self.right_pos = 0

    def cointegration_check(self, series01, series02):
        series01 = np.array(series01)
        series02 = np.array(series02)
        urt_1 = ts.adfuller(series01, 1)[1]
        urt_2 = ts.adfuller(series02, 1)[1]

        # 同时平稳或不平稳则差分再次检验
        if (urt_1 > 0.1 and urt_2 > 0.1) or (urt_1 < 0.1 and urt_2 < 0.1):
            urt_diff_1 = ts.adfuller(np.diff(np.array(series01)), 1)[1]
            urt_diff_2 = ts.adfuller(np.diff(np.array(series02), 1))[1]

            # 同时差分平稳进行OLS回归的残差平稳检验
            if urt_diff_1 < 0.1 and urt_diff_2 < 0.1:
                matrix = np.vstack([series02, np.ones(len(series02))]).T
                beta, c = np.linalg.lstsq(matrix, series01, rcond=None)[0]
                resid = series01 - beta * series02 - c
                if ts.adfuller(np.array(resid), 1)[1] > 0.1:
                    result = False
                else:
                    result = True
                return beta, c, resid, result
            else:
                result = False
                return 0.0, 0.0, 0.0, result

        else:
            result = False
            return 0.0, 0.0, 0.0, result

    def prenext(self):
        self.next()

    def next(self):
        # 输出数据
        leg_data = self.getdatabyname("leg")
        right_data = self.getdatabyname("right")
        s1 = list(leg_data.close.get(size=self.p.look_back_num))
        s2 = list(right_data.close.get(size=self.p.look_back_num))
        now_time = leg_data.datetime.time()
        if now_time == datetime.time(21, 5):
            # print("s1 = ", s1)
            self.beta, self.c, resid, result = self.cointegration_check(s1, s2)
            # 计算残差的标准差上下轨
            mean = np.mean(resid)
            std = np.std(resid)
            self.up = mean + self.p.threshold * std
            self.down = mean - self.p.threshold * std
            self.mean = mean
            self.can_trade = result
            # self.log(f"leg_close = {leg_data.close[0]}, right_close = {right_data.close[0]}, c = {self.c}"
            #          f" beta = {self.beta}, len = {len(s1)}"
            #          f"mean = {round(self.mean, 2)}, up = {round(self.up, 2)}, dn = {round(self.down, 2)}")
        leg_size = self.getposition(leg_data).size
        if now_time < datetime.time(14, 30):
            resid_new = leg_data.close[0] - self.beta * right_data.close[0] - self.c
            # if leg_data.datetime[0] != right_data.datetime[0]:
            #     return
            if self.can_trade and resid_new < self.mean and self.leg_pos > 0:
                self.close(leg_data)
                self.close(right_data)
                self.log("多头止损")
                self.leg_pos = 0
                self.right_pos = 0

            if self.can_trade and resid_new > self.mean and self.leg_pos < 0:
                self.close(leg_data)
                self.close(right_data)
                self.log("空头止损")
                self.leg_pos = 0
                self.right_pos = 0

            if self.can_trade and resid_new < self.down and self.leg_pos == 0:
                self.sell(leg_data, 1)
                self.buy(right_data, 1)
                self.log("残差正向扩大，做空价差")
                self.leg_pos = -1
                self.right_pos = 1

            if self.can_trade and resid_new > self.up and self.leg_pos == 0:
                self.buy(leg_data, 1)
                self.sell(right_data, 1)
                self.log("残差正向扩大，做多价差")
                self.leg_pos = 1
                self.right_pos = -1

        if now_time == datetime.time(14, 55) and leg_size != 0:
            self.close(leg_data)
            self.close(right_data)
            self.leg_pos = 0
            self.right_pos = 0
            self.can_trade = False
            self.mean = None

    # def notify_order(self, order):
    #     if order.status in [order.Submitted, order.Accepted]:
    #         # order被提交和接受
    #         return
    #     if order.status == order.Rejected:
    #         self.log(f"order is rejected : order_ref:{order.ref}  order_info:{order.info}")
    #     if order.status == order.Margin:
    #         self.log(f"order need more margin : order_ref:{order.ref}  order_info:{order.info}")
    #     if order.status == order.Cancelled:
    #         self.log(f"order is concelled : order_ref:{order.ref}  order_info:{order.info}")
    #     if order.status == order.Partial:
    #         self.log(f"order is partial : order_ref:{order.ref}  order_info:{order.info}")
    #     # Check if an order has been completed
    #     # Attention: broker could reject order if not enougth cash
    #     if order.status == order.Completed:
    #         if order.isbuy():
    #             self.log("buy result : buy_price : {} , buy_cost : {} , commission : {}".format(
    #                 order.executed.price, order.executed.value, order.executed.comm))
    #
    #         else:  # Sell
    #             self.log("sell result : sell_price : {} , sell_cost : {} , commission : {}".format(
    #                 order.executed.price, order.executed.value, order.executed.comm))
    #
    # def notify_trade(self, trade):
    #     # 一个trade结束的时候输出信息
    #     if trade.isclosed:
    #         self.log('closed symbol is : {} , total_profit : {} , net_profit : {}'.format(
    #             trade.getdataname(), trade.pnl, trade.pnlcomm))
    #     if trade.isopen:
    #         self.log('open symbol is : {} , price : {} '.format(
    #             trade.getdataname(), trade.price))


def clean_data(data_path):
    df_leg = pd.read_csv(data_path, encoding='utf-8')
    # print(df_leg)
    df_leg['datetime'] = df_leg['date'] + " " + df_leg['time']
    df_leg.index = pd.to_datetime(df_leg['datetime'])
    df_leg = df_leg[['open', 'high', 'low', 'close', 'volume', 'open_interest']]
    df_leg.columns = ['open', 'high', 'low', 'close', 'volume', 'openinterest']
    return df_leg


def run():
    begin_time = time.perf_counter()
    # 添加cerebro
    cerebro = bt.Cerebro()
    # 添加策略
    cerebro.addstrategy(SmaStrategy)
    # 添加合约数据
    df_leg = clean_data("./rb.csv")
    df_leg = df_leg[df_leg.index >= pd.to_datetime("2013-10-18 09:00:00")]
    feed = bt.feeds.PandasDirectData(dataname=df_leg)
    cerebro.adddata(feed, name="leg")

    df_right = clean_data("./i.csv")
    df_right = df_right[df_right.index >= pd.to_datetime("2013-10-18 09:00:00")]
    feed = bt.feeds.PandasDirectData(dataname=df_right)
    cerebro.adddata(feed, name="right")
    # 设置交易费用，杠杆和合约乘数
    comm_leg = ComminfoFuturesPercent(commission=0.0001, margin=0.1, mult=10)
    cerebro.broker.addcommissioninfo(comm_leg, name="leg")
    comm_right = ComminfoFuturesPercent(commission=0.0001, margin=0.1, mult=100)
    cerebro.broker.addcommissioninfo(comm_right, name="right")
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
