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

def intervals(ticker):
    INTERVALS = [(100, 105), (200, 205), (300, 305), (400, 405), (500, 510), (1000, 1010), (1500, 1520), (2000, 2020), (2500, 2520), (3000, 3030), (3500, 3530), (4000, 4040), (4500, 4540), (5000, 5050)]
    df = pd.read_csv("stocks/{}.csv".format(ticker), index_col=0)
    closes = df['Close'].iloc[-3:].values
    counts = 0
    for close in closes:
        for interval in INTERVALS:
            if interval[0] <= close <= interval[1]:
                return True
    two_year_high = df['High'].iloc[-500:].max()
    five_day_high = df['High'].iloc[-5:].max()
    return five_day_high == two_year_high


checks = {'Trend':  trend, 'Volume': volume, 'Hundreds': intervals}

for check in checks:
    print("Checking {}".format(check))
    df[check] = df['Stock'].apply(checks[check])

def passes(row):
    return np.sum(row.drop(['Stock']).astype(np.int32))

df['Passes'] = df.apply(passes, axis=1)

df.sort_values('Passes', ascending=False, inplace=True)

df.to_csv("stock_list_checks.csv", index=False)