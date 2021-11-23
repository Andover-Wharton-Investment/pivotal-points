import pandas as pd
from scipy.stats import linregress
import numpy as np
from math import exp

def sigmoid(x):
    return 1 / (1 + exp(-x))

def trend(df):
    opens = df['Close'].iloc[-20:].values
    slope, intercept, r_value, p_value, std_err = linregress(range(len(opens)), opens)
    percent =  20 * slope / df['Close'].iloc[-20]
    return np.round(sigmoid(10*percent) * 2 - 1, 4)

def long_term_trend(df):
    opens = df['Close'].iloc[-60:].values
    slope, intercept, r_value, p_value, std_err = linregress(range(len(opens)), opens)
    percent = 60 * slope / df['Close'].iloc[-60]
    return np.round(sigmoid(5*percent) * 2 - 1, 4)

def volume(df):
    volumes = df['Volume'].iloc[-60:].values * df['Close'].iloc[-60:].values
    percent = np.mean(volumes[-5:])/ np.mean(volumes) - 1
    return np.round(sigmoid(4*percent) * 2 - 1, 4)

df = pd.DataFrame(columns=['Date', 'ticker', 'trend', 'long_term_trend', 'volume', 'return'])

with open('usable_stocks.txt', 'r') as f:
    row_num = 0
    for line in f:
        ticker = line.strip()
        print(ticker)
        cur_df = pd.read_csv("stocks/{}.csv".format(ticker))
        num_rows = len(cur_df.index)
        try:
            end_date = cur_df.index[cur_df['Date'] == '2020-12-31'].tolist()[0]
            for i in range(end_date, 60, -20):
                df.loc[row_num] = [cur_df['Date'][i], ticker, trend(cur_df.iloc[:i+1]), long_term_trend(cur_df.iloc[:i+1]), volume(cur_df.iloc[:i+1]), np.round(cur_df['Close'][i+1] / cur_df['Close'][i] - 1, 4)]
                row_num += 1
        except IndexError:
            pass

df.sort_values('Date', inplace=True)
df.to_csv('historical_correlation.csv', index=False)