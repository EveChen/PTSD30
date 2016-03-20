import sys
import csv
import collections

KBar = collections.namedtuple("KBar", ["date", "time", "open", "high", "low", "close", "volume"])
data = map(KBar._make, [row[:2] + map(int, row[2:]) for row in csv.reader(open(sys.argv[1]))])

position = action = 0  # 1 as Long and -1 as Short
position_price = 0
revenue = 0
lower_bound, upper_bound = 0, 10e4

for bar in data:
    price = bar.close
    if price > upper_bound and position != 1:
        action = 1
    elif price < lower_bound and position != -1:
        action = -1

    if action != position:
        print "[%s %5s] %-5s at %s, revenue: %4d" % (bar.date, bar.time, [None, "Long", "Short"][action], price, (price - position_price) * position)
        revenue += (price - position_price) * position
        position = action
        position_price = price
        lower_bound, upper_bound = 0, 10e4

    lower_bound = max(lower_bound, price * 0.99)
    upper_bound = min(upper_bound, price * 1.01)

print "Total revenue: %d, ROI: %d%%" % (revenue, revenue / 2000.0 * 100) # starting capital at 2000
