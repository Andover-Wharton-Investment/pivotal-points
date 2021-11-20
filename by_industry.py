import pandas as pd
import numpy as np
import os

industry_dict = {}

for filename in os.listdir('industries'):
    if filename.endswith('.txt'):
        industry = filename[:-4]
        industry_dict[industry] = [ticker for ticker in open(os.path.join('industries', filename), 'r').read().split('\n') if ticker != '']

df = pd.read_csv('stock_list_checks.csv')

with open('Scores.xlsx', 'wb') as f:
    writer = pd.ExcelWriter(f)
    df.to_excel(writer, sheet_name='All Stocks', index=False)
    for industry, tickers in industry_dict.items():
        new_df = df[df['Stock'].isin(tickers)]
        new_df.to_excel(writer, sheet_name=industry, index=False)
    writer.save()