# -*- coding: utf-8 -*-
import akshare as ak

df = ak.fund_etf_hist_em(symbol="510050", period="daily",
                         start_date="20000101",
                         end_date="20240629",
                         adjust="")
df.to_csv("上证50ETF_未复权.csv")
df = ak.fund_etf_hist_em(symbol="510050", period="daily",
                         start_date="20000101",
                         end_date="20240629",
                         adjust="hfq")
df.to_csv("上证50ETF_后复权.csv")
