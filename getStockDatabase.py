import yfinance as yf
import pandas as pd
import json

used = []

with open('stock_list.txt') as f:
    for line in f:
        if line.strip() not in used:
            print(line)
            used.append(line.strip())
            while True:
                try:
                    stock = yf.Ticker(line.strip())
                
                    if stock.info['marketCap'] is not None and stock.info['marketCap'] > 2000000000:
                        stock.history(period='max').to_csv('stocks/' + line.strip() + '.csv')
                        with open('usable_stocks.txt', 'a') as usable_stocks:
                            usable_stocks.write(line)
                    break
                except KeyError:
                    print('KeyError')
                    break
                except json.decoder.JSONDecodeError:
                    print('JSONDecodeError')