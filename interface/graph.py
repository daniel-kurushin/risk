"""
Определение параметров кредитного риска
модуль отрисовки графиков
Курушин Д.С.
Васильева Е.Е.
Долгова Е.В.
"""
from tkinter import *
from tkinter import ttk
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d import proj3d
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib import cm

import numpy as np
import pylab

class GraphInterface(object):
    BL = np.array([0.2331,0.2594,0.2467,0.2638,0.2744,0.3753,0.3170,0.3427,0.2538,0.4594,0.4313,0.2569,0.4986,0.2250,0.2302,0.7736,0.3708,0.6593,0.1761,0.3325,0.2977,0.4611,0.5438,0.2038,0.3470,0.2479,0.4915,0.3303,0.4514,0.6289,0.1363,0.3300,0.5347,0.1342,0.1515,0.1790,0.3564,0.2205,0.2366,0.4440,0.4841,0.4618,0.5132,0.4392,0.4587,0.3142,0.4918,0.3269,0.6515,0.2803,0.2586,0.3942,0.2610,0.4157,0.3585,0.6262,0.7256,0.5375,0.4183,0.5371,0.4107,0.3681,0.4119,0.2310,0.4364,0.4554,0.5675,0.6609,0.4894,0.3125,0.3848,0.2995,0.5012,0.5816,0.3213,0.3120,0.2754,0.1437,0.2081])
    CL = np.array([0.2662,0.2571,0.2909,0.2460,0.4271,0.2710,0.4720,0.4476,0.5983,0.5591,0.3611,0.3277,0.5198,0.3242,0.3943,0.3582,0.4380,0.7783,0.4213,0.5093,0.4727,0.7346,0.3486,0.3846,0.4911,0.2825,0.4100,0.5029,0.3492,0.4261,0.2814,0.4835,0.3811,0.1893,0.6237,0.4505,0.5554,0.6490,0.1445,0.3078,0.2534,0.7748,0.1564,0.3204,0.3568,0.4406,0.3205,0.4189,0.2594,0.4114,0.2357,0.4911,0.3596,0.2246,0.2194,0.5219,0.2592,0.4591,0.6126,0.3991,0.4075,0.2889,0.6841,0.1510,0.3563,0.3161,0.3710,0.3549,0.4120,0.3212,0.1661,0.2211,0.2799,0.4480,0.1731,0.1347,0.2208,0.4356,0.0933])
    R = 0.5 * (CL - BL) + 0.5

    def __init__(self, frame):
        self.toplevel = frame

        fig = pylab.figure()
        self.ax = fig.add_subplot(111, projection='3d')

        self.ax.plot(self.BL, self.CL, self.R, 'bo', color = (0,0,0), markersize = 2)
        X, Y, Z = [],[],[]
        for x in np.linspace(0,1,10):
            _x, _y, _z = [],[],[]
            for y in np.linspace(0,1,10):
                z = 0.5 * (x - y) + 0.5
                _x += [x]
                _y += [y]
                _z += [z]
            X += [_x]
            Y += [_y]
            Z += [_z]

        X = np.arange(0, 1, 0.1)
        Y = np.arange(0, 1, 0.1)
        X, Y = np.meshgrid(X, Y)
        Z = 0.5 * (X - Y) + 0.5

        self.ax.plot_wireframe(Y, X, Z, color = (0.8,0.8,1.0))

        self.ax.set_xlabel('BL')
        self.ax.set_ylabel('CL')
        self.ax.set_zlabel('R')

        x2, y2, _ = proj3d.proj_transform(self.BL[34], self.CL[34], self.R[34], self.ax.get_proj())

        self.label = pylab.annotate(
            "Республика Ингушетия",
            xy = (x2, y2), xytext = (-20, 20),
            textcoords = 'offset points', ha = 'right', va = 'bottom',
            bbox = dict(boxstyle = 'round,pad=0.5', fc = 'yellow', alpha = 0.5),
            arrowprops = dict(arrowstyle = '->', connectionstyle = 'arc3,rad=0'))

        self.canvas = FigureCanvasTkAgg(fig, master=self.toplevel)
        self.canvas.show()
        self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

        self.toolbar = NavigationToolbar2TkAgg(self.canvas, self.toplevel)
        self.toolbar.update()
        self.canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=1)

        self.canvas.mpl_connect('button_release_event', self.update_position)

    def update_position(self,e):
        x2, y2, _ = proj3d.proj_transform(self.BL[34],self.CL[34],self.R[34], self.ax.get_proj())
        self.label.xy = x2,y2
        self.label.update_positions(self.canvas.renderer)
        self.canvas.draw()
#
#
# pylab.show()

if __name__ == '__main__':
	root = Tk()
	GraphInterface(root)
	root.mainloop()
