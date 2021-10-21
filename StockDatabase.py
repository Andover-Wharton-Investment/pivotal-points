import yfinance as yf
import pandas as pd
from typing import List
import os.path
import pickle
import numpy as np
from datetime import datetime, timedelta
from typing import Dict

class StockDatabase:
    def __init__(self, stock_list_file) -> None:
        with open(stock_list_file, 'r') as f:
            self.stocklists = f.readlines()
        self.stocklists = [stock[:-2] for stock in self.stocklists]

    def get_all_stocks(self):
        data = {}
        for stock in self.stocklists:
            ret = self.get_stock_prices(stock)
            if ret is not None and isinstance(ret, (Dict)):
                print(stock)
                data[stock] = ret
        with open('all_stocks.pkl', 'wb') as f:
            pickle.dump(data,f)

    def get_stock_prices(self, symbol : str):
        '''
        length should be in 1-day
        '''
        print(symbol)
        data = yf.Ticker(symbol).history(interval='1d',period="max")
        data = {'Date' : data.index.to_numpy(), 'Open' : data['Open'].to_numpy().astype(np.float32), 'High' : data['High'].to_numpy().astype(np.float32), 'Low' : data['Low'].to_numpy().astype(np.float32)}
        return data

a = StockDatabase('stock_list.txt')
a.get_all_stocks()
# for i in range(len(a.stocklists)):
#     a.get_stock_prices(a.stocklists[i])

