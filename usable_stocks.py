import os

with open('usable_stocks.txt', 'w') as f:
    for file in os.listdir("stocks"):
        
        with open('stocks/' + file, 'r') as s:
            num_lines = sum(1 for line in s)
            if num_lines > 1:
                f.write(file[:-4] + '\n')