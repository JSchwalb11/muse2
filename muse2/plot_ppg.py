import matplotlib.pyplot as plt
import csv
import numpy as np
import os

def plot_muse_csv(path, file):
    x = []
    y = []
    bpi = []
    labels = []

    with open(path+'/'+file, 'r') as f:
        plots = csv.reader(f, delimiter=',')
        for row in plots:
            if (plots.line_num == 1):
                labels.append(row[0])
                labels.append(row[1])
            else:
                x.append(float(row[0]))
                y.append(float(row[1]))

        """
        labels[0] = plot[0][0]
        labels[1] = plot[0][1]
        """
        plt.xlabel = labels[0]
        plt.ylabel = labels[1]

        """
        for row in plot[1:]:
            x.append(float(row[0]))
            y.append(float(row[1]))
        """
        for i in range(0, plots.__sizeof__()):
            ppg_to_bpi(bpi, y[i])

        y_mean = np.mean(y)
        bpi_mean = np.mean(bpi)
        y_std_dev = np.std(y)
        bpi_std_dev = np.std(bpi)

        print("\n{0}".format(file))
        print("{0} mean: {1}\n{2} mean: {3}\n{4} std_dev: {5}\n{6} std_dev: {7}"
              .format(labels[1], y_mean, "BPI", bpi_mean,
                      labels[1], y_std_dev, "BPI", bpi_std_dev))


def ppg_to_bpi(arr,val):
    return arr.append(60000/val)

if __name__ == "__main__":
    PROJECT_ROOT = os.getcwd()
    DATA_DIR = PROJECT_ROOT + '/data/PPG'
    print(DATA_DIR)
    files = []
    for file in os.listdir(DATA_DIR):
        plot_muse_csv(DATA_DIR, file)

"""
#with open('PPG_recording_2020-02-25-21.57.48.csv', 'r') as csvfile:
with open('PPG_recording_2020-02-25-22.35.35.csv', 'r') as csvfile:
    plots= csv.reader(csvfile, delimiter=',')
    for row in plots:
        if (plots.line_num == 1):
            plt.xlabel = row[0]
            plt.ylabel = row[1]
        else:
            x.append(float(row[0]))
            y.append(float(row[1]))

for i in range(0, x.__len__()):
    print(i)
    bpi.append(60000 / y[i])

x_std_dev = np.std(x)
bpi_std_dev = np.std(bpi)
y_std_dev =np.std(y)
print("bpi mean: {0}".format(np.mean(bpi)))

print("{0} standard deviation: {1}\n {2} standard deviation: {3}\n{4} standard devitation: {5}\n".
      format(plt.xlabel, x_std_dev, plt.ylabel, y_std_dev, "bpi", bpi_std_dev))
plt.plot(x,y, marker='o')

plt.title('Data from the CSV File: {0} and {1}'.format(plt.xlabel, plt.ylabel))

plt.show()

"""