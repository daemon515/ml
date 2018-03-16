import pandas as pd
import numpy as np
import quandl
import os
from stockstats import StockDataFrame

directory = "stock_data"

def download_data(stocks, usestockstats=True):
    # if directory does not exist, create & download the data
    stock_items = list()
    #stock_items = ["WIKI/INTC", "WIKI/QCOM", "WIKI/NVDA", "WIKI/TXN", "WIKI/BRCM", "WIKI/AAPL"]
    for item in stocks:
        stock_items += ["WIKI/"+item]
    if not os.path.exists(directory):
        os.makedirs(directory)
    for item in stock_items:
        fileName = os.path.join(directory, item[5:]+".csv")
        if os.path.exists(fileName):
            continue
        data = quandl.get(item)
        final_data = data.copy()
        if (usestockstats == True):
            stock_df = StockDataFrame.retype(data)
            final_data['RSI'] = stock_df['rsi_14']
            final_data['StocOsci'] = stock_df['kdjj']
            final_data['ADMI'] = stock_df['adx']
            final_data['VVR'] = stock_df['vr']
            final_data['SMA'] = stock_df['adj. close_14_sma']
        
        with open(fileName, 'w+') as f:
            final_data.to_csv(f)

def get_stocks_df_by_column(stocks, columnName = 'Adj. Close', dateFrom = '2006-01-01'):
    stock_info_df = pd.DataFrame()
    for stock_id in stocks:
        fileName = os.path.join(directory, stock_id +".csv")
        if not os.path.exists(fileName):
            print("get_stocks_dataframe: Missing {} data".format(stock_id))
            continue
        stock_dat = pd.read_csv(fileName, index_col= [0], header=0, parse_dates=[1])
        frame = stock_dat[[columnName]]
        frame.columns = [stock_id]
        stock_info_df = pd.concat([stock_info_df, frame], axis=1)

    info = stock_info_df.loc[dateFrom:]
    return info

def get_stock_dataframe(stockName, dateFrom = '2006-01-01'):
    fileName = os.path.join(directory, stockName + ".csv")
    stock_data = pd.read_csv(fileName, index_col= [0], header=0, parse_dates=[1])
    stock_data['Open'] = stock_data.Open.astype(float)
    stock_data.drop(['Ex-Dividend', 'Split Ratio', 'Open', 'High', 'Close', 'Low', 'Volume'], axis=1, inplace=True)
    return stock_data.loc[dateFrom:]
