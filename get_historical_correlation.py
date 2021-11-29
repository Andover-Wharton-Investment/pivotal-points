import swifter
import pandas as pd
from scipy.stats import linregress
import numpy as np
from math import exp

def sigmoid(x):
    return 1 / (1 + exp(-x))

def trend_twenty_day(df):
    opens = df['Close'].iloc[-20:].values
    slope, intercept, r_value, p_value, std_err = linregress(range(len(opens)), opens)
    percent =  20 * slope / df['Close'].iloc[-20]
    return np.round(percent, 4)
    return np.round(sigmoid(10*percent) * 2 - 1, 4)

def trend_sixty_day(df):
    opens = df['Close'].iloc[-60:].values
    slope, intercept, r_value, p_value, std_err = linregress(range(len(opens)), opens)
    percent = 60 * slope / df['Close'].iloc[-60]
    return np.round(percent, 4)
    return np.round(sigmoid(5*percent) * 2 - 1, 4)
    
def volume(df):
    volumes = df['Volume'].iloc[-60:].values * df['Close'].iloc[-60:].values
    percent = np.mean(volumes[-5:])/ np.mean(volumes) - 1
    np.round(percent, 4)
    return np.round(sigmoid(4*percent) * 2 - 1, 4)

def rsi(df):
    closes = df['Close'].iloc[-15:]
    window_length = 14
    delta = closes.diff()
    gain = delta.clip(lower=0)
    loss = delta.clip (upper=0).abs()
    average_gain = gain.ewm(com=window_length-1, adjust=True, min_periods=window_length).mean()
    average_loss = loss.ewm(com=window_length-1, adjust=True, min_periods=window_length).mean()
    rs = average_gain.iloc[-1] / average_loss.iloc[-1]
    rsi_final = (100 - (100 / (1+rs)))*0.01
    return ((-1)*(rsi_final-1)*2)-1

dfs = {}

def get_cols(ticker, i):
    cur_df = dfs[ticker]
    return {"20 day trend": trend_twenty_day(cur_df.iloc[:i+1]), "60 day trend": trend_sixty_day(cur_df.iloc[:i+1]), "Volume": volume(cur_df.iloc[:i+1]), "RSI": rsi(cur_df.iloc[:i+1]), "5 day return": np.round(cur_df['Close'][i+5] / cur_df['Close'][i] - 1, 4), "20 day return": np.round(cur_df['Close'][i+20] / cur_df['Close'][i] - 1, 4), "60 day return": np.round(cur_df['Close'][i+60] / cur_df['Close'][i] - 1, 4), "One year return": np.round(cur_df['Close'][i+252] / cur_df['Close'][i] - 1, 4)}

df = pd.DataFrame(columns=['i', 'Date', 'ticker'])

print("Dates")
with open('usable_stocks.txt', 'r') as f:
    row_num = 0
    for line in f:
        ticker = line.strip()
        print(ticker)
        cur_df = pd.read_csv("stocks/{}.csv".format(ticker))
        dfs[ticker] = cur_df
        try:
            end_date = cur_df.index[cur_df['Date'] == '2019-12-31'].tolist()[0]
            for i in range(end_date, 60, -5):
                df.loc[row_num] = [i, cur_df['Date'][i], ticker]
                row_num += 1
        except IndexError:
            pass

print("Applying")

appiled_df = df.swifter.apply(lambda row: get_cols(row.ticker, row.i), axis='columns', result_type='expand')
df = pd.concat([df.drop(columns=['i']), appiled_df], axis='columns')

df.sort_values('Date', inplace=True)
df.to_csv('historical_correlation.csv', index=False)