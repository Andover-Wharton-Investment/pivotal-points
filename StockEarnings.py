import yahoo_fin.stock_info as si
import pandas as pd

used = []

with open('usable_stocks.txt', 'r') as f:
    for line in f:
        if line.strip() not in used:
            print(line)
            for i in range(100):
                try:
                    stock = si.get_earnings_history(line.strip())
                
                    df = pd.DataFrame.from_dict(stock)[['epsestimate', 'epsactual']].dropna()
                    df.to_csv('earnings/' + line.strip() + '.csv', index=False)
                    used.append(line.strip())
                    break
                except  KeyError:
                    print("Broken")
                    break
                except (IndexError, TypeError):
                    print("Trying again")

with open('usable_stocks.txt', 'w') as f:
    for l in used:
        f.write(l + '\n')