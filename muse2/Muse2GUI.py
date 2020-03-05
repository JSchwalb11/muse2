from distutils.util import strtobool

import matplotlib

matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
from pylsl import StreamInlet, resolve_byprop
import os
from muselsl.constants import LSL_SCAN_TIMEOUT, LSL_PPG_CHUNK
import time
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import tkinter as tk
from tkinter import ttk
import sys

# parser = argparse.ArgumentParser()
# parser.add_argument("live", help="Are we live streaming from the muse? True/False.", type=bool, default=False)
# args = parser.parse_args()

live = strtobool(sys.argv[1])
LARGE_FONT = ("Verdana", 12)
style.use("ggplot")
PROJECT_ROOT = os.getcwd()
DATA_DIR = PROJECT_ROOT + '/data/PPG'
print(DATA_DIR)
files = []
if (live == 1):
    data_source = "PPG"
    chunk_length = LSL_PPG_CHUNK
    dejitter = False
    print("Looking for a %s stream..." % (data_source))
    streams = resolve_byprop('type', data_source, timeout=LSL_SCAN_TIMEOUT)
    if len(streams) == 0:
        print("Can't find %s stream." % (data_source))
    print("Looking for a Markers stream...")
    marker_streams = resolve_byprop(
        'name', 'Markers', timeout=LSL_SCAN_TIMEOUT)

    if marker_streams:
        inlet_marker = StreamInlet(marker_streams[0])
    else:
        inlet_marker = False
        print("Can't find Markers stream.")

# plots = [Figure(figsize=(5, 5), dpi=100),
#         Figure(figsize=(5, 5), dpi=100),
#         Figure(figsize=(5, 5), dpi=100),
#         Figure(figsize=(5, 5), dpi=100)]
f = Figure(figsize=(5, 5), dpi=100)
a = f.add_subplot(111)


# subplots = []
# for i, item in enumerate(plots):
#    subplots.append(plots[i].add_subplot(111))

def animate_from_file(i):
    pullData = open(DATA_DIR + '/' + "PPG_recording_2020-02-25-21.57.48.csv", "r").read()
    rows = pullData.split('\n')
    arr = []
    labels = rows[0].split(',')
    for item in labels:
        arr.append([])

    for line in rows[1:]:
        if len(line) > 1:
            raw = line.split(',')
            for i, item in enumerate(raw):
                arr[i].append(float(item))

    a.clear()
    for i in range(1, len(arr)):
        a.plot(arr[0], arr[i], marker='', label=labels[i])

    f.legend(loc=2, ncol=2)


def animate_live(i):
    if (len(streams) > 0):
        print("Started acquiring data.")
        inlet = StreamInlet(streams[0], max_chunklen=chunk_length)

        info = inlet.info()
        description = info.desc()

        Nchan = info.channel_count()
        ch = description.child('channels').first_child()
        ch_names = [ch.child_value('label')]
        for i in range(1, Nchan):
            ch = ch.next_sibling()
            ch_names.append(ch.child_value('label'))

        res = []
        timestamps = []
        markers = []
        t_init = time.time()
        time_correction = inlet.time_correction()
        print('Start recording at time t=%.3f' % t_init)
        print('Time correction: ', time_correction)
        data, timestamp = inlet.pull_chunk(timeout=1.0,
                                           max_samples=chunk_length)

        if timestamp:
            res.append(data)
            timestamps.extend(timestamp)
        if inlet_marker:
            marker, timestamp = inlet_marker.pull_sample(timeout=0.0)
            if timestamp:
                markers.append([marker, timestamp])

        time_correction = inlet.time_correction()
        print('Time correction: ', time_correction)

        res = np.concatenate(res, axis=0)
        timestamps = np.array(timestamps) + time_correction

        if dejitter:
            y = timestamps
            X = np.atleast_2d(np.arange(0, len(y))).T
            lr = LinearRegression()
            lr.fit(X, y)
            timestamps = lr.predict(X)

        res = np.c_[timestamps, res]
        data = pd.DataFrame(data=res, columns=['timestamps'] + ch_names)

        """ -----------------------------------------------------------  """
        rows = streams.split('\n')
        arr = []
        labels = rows[0].split(',')
        for item in labels:
            arr.append([])

        for line in rows[1:]:
            if len(line) > 1:
                raw = line.split(',')
                for i, item in enumerate(raw):
                    arr[i].append(float(item))

        a.clear()
        for i in range(1, len(arr)):
            a.plot(arr[0], arr[i], marker='', label=labels[i])

        f.legend(loc=2, ncol=2)
    else:
        print("No streams found.")


class Muse2GUI(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # tk.Tk.iconbitmap(self, default="clienticon.ico")
        # tk.Tk.wm_title(self, "Muse2 GUI Client")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, PageOne, PageTwo, PageThree):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Start Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        page1 = tk.Button(self, text="Visit Page 1", command=lambda: controller.show_frame(PageOne))
        page1.pack()

        # page2 = tk.Button(self, text="Visit Page 2", command=lambda: controller.show_frame(PageTwo))
        # page2.pack()

        # page3 = tk.Button(self, text="Visit Page 3", command=lambda: controller.show_frame(PageThree))
        # page3.pack()


class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="PPG1 vs Time", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Back to Home", command=lambda: controller.show_frame(StartPage))
        button1.pack()

        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Live PPG vs Time", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Back to Home", command=lambda: controller.show_frame(StartPage))
        button1.pack()
        """
        canvas = FigureCanvasTkAgg(plots[1], self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        """


class PageThree(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="PPG3 vs Time", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Back to Home", command=lambda: controller.show_frame(StartPage))
        button1.pack()
        """
        canvas = FigureCanvasTkAgg(plots[2], self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        """


app = Muse2GUI()

if (live == 1):
    ani = animation.FuncAnimation(f, animate_live, interval=1000)
else:
    ani = animation.FuncAnimation(f, animate_from_file, interval=1000)

app.mainloop()
