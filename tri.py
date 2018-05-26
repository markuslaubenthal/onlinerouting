from scipy.spatial import Delaunay
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from matplotlib.backend_bases import MouseEvent
import math


class Node:
    def __init__(self, p, xp):
        self.l = None
        self.r = None
        self.p = p
        self.xp = xp
        self.x = x
        self.y = y

class Tree:
    def __init__(self):
        self.root = None
    def add(self, p, x, y):
        if(self.root == None):
            self.root = Node(p, p, x, y)
        else:
            self._add(p, x, y, self.root)

    def _add(self, p, x, y, node):




def createEdgesForCoan(P):
    #sorts the points in to a visiting order (order induced by D1)
    #visits each point p and adds it to the tree T
    #queryes T for r = minAbove(p) this returns the edge [p,r]
    #saves and returns edges
    #vD1 = np.array([2 * sqrt(3), -3])
    vD1 = np.array([2 * math.sqrt(3), -3])
    vD2 = np.array([2 * math.sqrt(3), 3])

    #creating the viewing order
    unsortedList = []
    for i in range(P[:,0].size):
        distD1 = np.dot(P[i], vD1) / np.dot(vD1,vD1)
        unsortedList.append([i, distD1])
    a = np.array(unsortedList)
    viewingOrder = a[a[:,1].argsort()]
    viewingOrder = viewingOrder[:,0].astype(int)












def halfThetaSix(S):
    #rotates the points all three directions
    #   90deg 210deg 330deg
    #calls createEdgesForCoan
    #collects the edges
    print S
    createEdgesForCoan(S)


class examplePlot(object):
    u""" An example of plot with draggable markers """

    def __init__(self):
        self._figure, self._axes, self._line = None, None, None
        self._dragging_point = None
        self._points = np.random.rand(3,2) * 100
        self._trigangulation = None

        self._init_plot()

    def _init_plot(self):
        self._figure = plt.figure("Example plot")
        axes = plt.subplot(1, 1, 1)
        axes.set_xlim(0, 100)
        axes.set_ylim(0, 100)
        #axes.grid(which="both")
        axes.plot(self._points[:,0], self._points[:,1], 'bo')
        self._axes = axes
        self._figure.canvas.mpl_connect('button_press_event', self._on_click)
        plt.show()

    def _add_point(self, x, y=None):
        if isinstance(x, MouseEvent):
            x, y = int(x.xdata), int(x.ydata)
        self._points = np.concatenate((self._points, np.array([[x, y]])))
        return x, y

    def _on_click(self, event):
        if event.inaxes != self._axes: return
        self._add_point(event)
        self._update_plot()

    def _update_plot(self):
        halfThetaSix(self._points)
        self._trigangulation = Delaunay(self._points)
        tri = self._trigangulation
        pltpoints = np.copy(self._points)
        self._axes.cla()
        self._axes.set_ylim(0, 100)
        self._axes.set_xlim(0, 100)
        self._axes.triplot(self._points[:,0], self._points[:,1], tri.simplices)
        self._axes.plot(pltpoints[:,0], pltpoints[:,1], 'bo')
        self._figure.canvas.draw()

if __name__ == "__main__":
    plot = examplePlot()













    #
