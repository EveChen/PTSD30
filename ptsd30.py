import sys
import csv
import pandas as pd

df = pd.read_csv("data/TX1M.txt", sep = ',', names = ["date", "time", "open", "high", "low", "close", "volume"])

position = action = 0  # 1 as Long and -1 as Short
position_price = 0
revenue = 0
lower_bound, upper_bound = 0, 10e4

for i in range(len(df)):
    price = df.iloc[i]['close']
    if price > upper_bound and position != 1:
        action = 1
    elif price < lower_bound and position != -1:
        action = -1

    if action != position:
        print("[%s %5s] %-5s at %s, revenue: %4d" % (df.iloc[i]['date'], df.iloc[i]['time'], [None, "Long", "Short"][action], price, (price - position_price) * position))
        revenue += (price - position_price) * position
        position = action
        position_price = price
        lower_bound, upper_bound = 0, 10e4

    lower_bound = max(lower_bound, price * 0.99)
    upper_bound = min(upper_bound, price * 1.01)

print("Total revenue: %d, ROI: %d%%" % (revenue, revenue / 2000.0 * 100)) # starting capital at 2000
