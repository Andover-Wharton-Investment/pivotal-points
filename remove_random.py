with open('NASDAQ-AMEX-NYSE-Stock-List.txt', 'r') as f:
    lines = sorted(set([line.strip() for line in f if line.strip() and line.strip().isalpha()]))

with open('historical_raw.txt', 'w') as f:
    for line in lines:
        f.write(line + '\n')