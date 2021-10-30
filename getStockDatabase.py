import yfinance as yf
import pandas as pd

with open('stock_list.txt') as f:
    for line in f:
        stock = yf.Ticker(line.strip())
        print(line)
        stock.history(period='max').to_csv('stocks/' + line.strip() + '.csv')