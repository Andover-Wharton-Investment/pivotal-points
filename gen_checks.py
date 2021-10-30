import pandas as pd
from scipy.stats import linregress
import numpy as np

df = pd.read_csv("usable_stocks.txt", header=None, names=["Stock"])

def trend(ticker):
    df = pd.read_csv("stocks/{}.csv".format(ticker), index_col=0)
    opens = df['Open'].iloc[-60:].values
    slope, intercept, r_value, p_value, std_err = linregress(range(len(opens)), opens)
    return slope > 0

def volume(ticker):
    df = pd.read_csv("stocks/{}.csv".format(ticker), index_col=0)
    volumes = df['Volume'].iloc[-60:].values
    return np.mean(volumes) * 1.15 <= np.mean(volumes[-5:])

checks = {'Trend':  trend, 'Volume': volume}


for check in checks:
    print("Checking {}".format(check))
    df[check] = df['Stock'].apply(checks[check])

def passes(row):
    return np.sum(row.drop(['Stock']).astype(np.int32))

df['Passes'] = df.apply(passes, axis=1)

df.sort_values('Passes', ascending=False, inplace=True)

df.to_csv("stock_list_checks.csv", index=False)