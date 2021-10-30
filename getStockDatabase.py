import yfinance as yf
import pandas as pd

with open('stock_list.txt') as f:
    for line in f:
        stock = yf.Ticker(line.strip())
        print(line)
        try:
            if stock.info['marketCap'] is not None and stock.info['marketCap'] > 2000000000:
                stock.history(period='max').to_csv('stocks/' + line.strip() + '.csv')
                with open('usable_stocks.txt', 'a') as usable_stocks:
                    usable_stocks.write(line)
        except KeyError:
            print('KeyError')