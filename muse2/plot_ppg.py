import matplotlib.pyplot as plt
import csv

x=[]
y=[]

with open('PPG_recording_2020-02-25-03.30.47.csv', 'r') as csvfile:
    plots= csv.reader(csvfile, delimiter=',')
    for row in plots:
        if (plots.line_num == 1):
            plt.xlabel = row[0]
            plt.ylabel = row[1]
        else:
            x.append(float(row[0]))
            y.append(float(row[1]))

plt.plot(x,y, marker='o')

plt.title('Data from the CSV File: {0} and {1}'.format(plt.xlabel, plt.ylabel))

plt.show()
