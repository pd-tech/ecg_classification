import sys
import csv
import matplotlib.pyplot as plt
import numpy as np

time = []
volts = []
marker = []

file = sys.argv[1]

with open(sys.argv[1], newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=' ')
    for row in spamreader:
        time.append(float(row[0]))
        volts.append(float(row[1]))
        marker.append(int(row[2]))

start = 0 if len(sys.argv)<3 else int(sys.argv[2])
end = len(time) if len(sys.argv)<4 else int(sys.argv[3])

fig, ax = plt.subplots()
ax.plot(time[start:end], volts[start:end])
plt.show()