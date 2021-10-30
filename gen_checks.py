import pandas as pd
from scipy.stats import linregress
import numpy as np

df = pd.read_csv("usable_stocks.txt", header=None, names=["Stock"])

def trend(ticker):
    print(ticker)
    df = pd.read_csv("stocks/{}.csv".format(ticker), index_col=0)
    opens = df['Open'].iloc[-60:].values
    slope, intercept, r_value, p_value, std_err = linregress(range(len(opens)), opens)
    return slope > 0

checks = {'Trend':  trend}


for check in checks:
    print("Checking {}".format(check))
    df[check] = df['Stock'].apply(checks[check])

df.to_csv("stock_list_checks.csv", index=False)