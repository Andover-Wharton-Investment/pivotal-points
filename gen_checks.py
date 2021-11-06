import pandas as pd
from scipy.stats import linregress, logistic
import numpy as np

df = pd.read_csv("usable_stocks.txt", header=None, names=["Stock"])

def trend(ticker):
    df = pd.read_csv("stocks/{}.csv".format(ticker), index_col=0)
    opens = df['Open'].iloc[-20:].values
    slope, intercept, r_value, p_value, std_err = linregress(range(len(opens)), opens)
    percent =  20 * slope / df['Open'].iloc[-20]
    return np.round(logistic.cdf(10*percent) * 2 - 1, 4)

def long_term_trend(ticker):
    df = pd.read_csv("stocks/{}.csv".format(ticker), index_col=0)
    opens = df['Open'].iloc[-60:].values
    slope, intercept, r_value, p_value, std_err = linregress(range(len(opens)), opens)
    percent = 60 * slope / df['Open'].iloc[-60]
    return np.round(logistic.cdf(5*percent) * 2 - 1, 4)

def volume(ticker):
    df = pd.read_csv("stocks/{}.csv".format(ticker), index_col=0)
    volumes = df['Volume'].iloc[-60:].values * df['Close'].iloc[-60:].values
    percent = np.mean(volumes[-5:])/ np.mean(volumes) - 1
    return np.round(logistic.cdf(4*percent) * 2 - 1, 4)

def intervals(ticker):
    df = pd.read_csv("stocks/{}.csv".format(ticker), index_col=0)
    two_year_high = df['High'].iloc[-500:].max()
    five_day_high = df['High'].iloc[-5:].max()
    if five_day_high == two_year_high:
        return 2
    INTERVALS = [(100, 105), (200, 205), (300, 305), (400, 405), (500, 510), (1000, 1010), (1500, 1520), (2000, 2020), (2500, 2520), (3000, 3030), (3500, 3530), (4000, 4040), (4500, 4540), (5000, 5050)]
    closes = df['Close'].iloc[-3:].values
    opens = df['Open'].iloc[-3:].values
    for i in range(3):
        for interval in INTERVALS:
            if interval[0] <= closes[i] <= interval[1] or (opens[i] < interval[0] and closes[i] > interval[1]):
                return 1
    return 0
    


checks = {'Trend':  trend, 'Long Term Trend': long_term_trend, 'Volume': volume, 'Hundreds': intervals}

for check in checks:
    print("Checking {}".format(check))
    df[check] = df['Stock'].apply(checks[check])

def passes(row):
    return np.round(np.sum(row.drop(['Stock']).astype(np.float32)), 4)

df['Passes'] = df.apply(passes, axis=1)

df.sort_values('Passes', ascending=False, inplace=True)

df.to_csv("stock_list_checks.csv", index=False)