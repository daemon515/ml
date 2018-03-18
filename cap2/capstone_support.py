import pandas as pd
import numpy as np
import quandl
import os
import math
import matplotlib.pyplot as plt
import datetime
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

def get_datetime_from_str(date_str):
    return datetime.datetime.strptime(date_str, '%Y-%m-%d')

def get_gap_in_months(start_date, end_date):
    return (end_date.year - start_date.year) * 12 + end_date.month - start_date.month

def plot_graph(ax, test_dates, prediction, actual, title="Title goes here"):
    print("Test dates start {} end {}".format(test_dates[0], test_dates[-1]))
    start_date = get_datetime_from_str(test_dates[0])
    end_date = get_datetime_from_str(test_dates[-1])
    num_months = get_gap_in_months(start_date, end_date)
    #print(num_months)

    ax.set_title(title)
    ax.set_xticklabels('')
    #ax.set_xticks([datetime.date(start_year+int(i/12),1+i%12,1) for i in range(num_months)])
    ax.set_xticks([datetime.date(start_date.year+int(i),1,1) for i in range(1+int(num_months/12))])
    ax.set_xticklabels([datetime.date(start_date.year+int(i),1,1).strftime('%Y')  for i in range(1+int(num_months/12)+1)])
    ax.plot(test_dates.astype(datetime.datetime), prediction, 'r-', label = 'predicted')
    ax.plot(test_dates.astype(datetime.datetime), actual, 'g-.', label = 'actual')
    ax.legend(loc='upper right', shadow=True).get_frame().set_facecolor('0.8')
