import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


class get_data():
    def __init__(self,tickers, market,start_date,end_date):
        self.tickers=tickers
        self.market=market
        self.start_date=start_date
        self.end_date=end_date
    def get_data_ticker(self):
        df=pd.DataFrame()
        for i in self.tickers:
            df[i]=yf.download(i,self.start_date,self.end_date)['Close']
        df=df.pct_change()
        return df
    def get_data_market(self):
        market=yf.download(self.market,self.start_date,self.end_date)['Close']
        df=pd.DataFrame(market)
        df=df.pct_change()
        return df




# I know my functions looks pretty much retarding, it's probably because of 12 pages demonstration in topology last weekend and 3 assigments in Analysis already suck all of the creativity out of me, please understand !!!
class capm():
    def __init__(self,tickers,market,start,end,riskfree):
        self.tickers=tickers
        self.market=market
        self.start=start
        self.end=end
        self.riskfree=riskfree
        a=get_data(tickers,market,start,end)
        self.df_mrk=a.get_data_market()
        self.df_tck=a.get_data_ticker()
    def beta(self):
        mrk_var= self.df_mrk.var()
        cov_bis= pd.concat([self.df_mrk,self.df_tck],axis=1,join='inner') #concat 2 df to calculate the covariance of each tickers with the marker
        cov_bis=cov_bis.cov()
        cov=cov_bis.take([0],axis=1)
        cov= cov.drop(cov.index[0])
        beta= cov/mrk_var
        return beta
    def capm(self):
        riskpre=self.df_mrk.mean() - self.riskfree
        beta=self.beta()
        beta_bis= beta.multiply(riskpre)
        capm= self.riskfree+beta_bis
        return capm 
    def sharpe(self):
        bis= self.capm() - self.riskfree
        tck_std= self.df_tck.std()
        tck_std=pd.DataFrame(tck_std)
        df=pd.concat([bis,tck_std],axis=1,join='inner',ignore_index=True)
        re= pd.DataFrame(df[0]/df[1])
        return re


    




