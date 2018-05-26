from scipy.spatial import Delaunay
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as lines
from matplotlib.widgets import Button
from matplotlib.backend_bases import MouseEvent
import math


class Node:
    def __init__(self, p, xp, xpx, x, y):
        self.l = None
        self.r = None
        self.p = p
        self.xp = xp
        self.xpx = x
        self.x = x
        self.y = y

class Tree:
    def __init__(self, vD2):
        self.root = None
        self.vD2 = vD2
    def add(self, p, x, y):
        if(self.root == None):
            self.root = Node(p, p, x, x, y)
        else:
            self._add(p, x, y, self.root)

    def _add(self, p, x, y, node):
        if node.xpx > x:
            node.xpx = x
            node.xp = p
        distD2_new = np.dot(np.array([x, y]), self.vD2) / np.dot(self.vD2, self.vD2)
        distD2_node = np.dot(np.array([node.x, node.y]), self.vD2) / np.dot(self.vD2, self.vD2)
        if distD2_new <= distD2_node:
            if node.l == None:
                node.l = Node(p, p, x, x, y)
                node.r = Node(node.p, node.p, node.x, node.x, node.y)
                node.p = p
                node.x = x
                node.y = y
                return (-1, 0, 0)
            else:
                _p, _x, _y = self._add(p, x, y, node.l)
                if _p != -1:
                    node.p = p
                    node.x = x
                    node.y = y
                    return (-1, 0, 0)
        else:
            if node.r == None:
                node.r = Node(p, p, x, x, y)
                node.l = Node(node.p, node.p, node.x, node.x, node.y)
                return (p, x, y)
            else:
                return self._add(p, x, y, node.r)

    def minAbove(self, p, x, y):
        if(self.root == None):
            return 0
        else:
            M = self._minAbove(p, x, y, self.root)
        _M = M[M[:,1].argsort()]
        smallest = -2;
        for m in _M:
            if smallest == -2 and m[0] != p:
                smallest = m[0]
        return smallest

    def _minAbove(self, p, x, y, node):
        distD2_new = np.dot(np.array([x, y]), self.vD2) / np.dot(self.vD2, self.vD2)
        distD2_node = np.dot(np.array([node.x, node.y]), self.vD2) / np.dot(self.vD2, self.vD2)
        if distD2_new <= distD2_node:
            if node.l:
                # _i = np.array([[node.xp, node.xpx]])
                # _j = np.array([self._minAbove(p, x, y, node.l)])
                # print _i
                # print _j
                return np.append(np.array([[node.r.xp, node.r.xpx]]), self._minAbove(p, x, y, node.l), axis = 0)
            else:
                return np.array([[node.xp, node.xpx]])
        else:
            if node.r:
                return self._minAbove(p, x, y, node.r)
            else:
                return np.array([[node.xp, node.xpx]])
    def printTree(self):
        if(self.root != None):
            self._printTree(self.root)

    def _printTree(self, node):
        if(node != None):
            self._printTree(node.l)
            print str(node.p) + ' '
            self._printTree(node.r)
def createEdgesForCoan(P):
    #sorts the points in to a visiting order (order induced by D1)
    #visits each point p and adds it to the tree T
    #queryes T for r = minAbove(p) this returns the edge [p,r]
    #saves and returns edges
    #vD1 = np.array([2 * sqrt(3), -3])
    vD1 = np.array([1, -math.sqrt(3)])
    vD2 = np.array([1, math.sqrt(3)])

    #creating the viewing order
    unsortedList = []
    for i in range(P[:,0].size):
        distD1 = np.dot(P[i], vD1) / np.dot(vD1,vD1)
        unsortedList.append([i, distD1])
    a = np.array(unsortedList)
    viewingOrder = a[a[:,1].argsort()]
    viewingOrder = viewingOrder[:,0].astype(int)[::-1]
    tree = Tree(vD2)

    for p in viewingOrder:
        tree.add(p, P[p][0], P[p][1])
        minAbove = tree.minAbove(p, P[p][0], P[p][1])












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
        # self._points = np.random.rand(3,2) * 100
        self._points = np.array([[10,30], [20,20], [40,30], [10,10], [30,20], [50,10]])
        self._trigangulation = None

        self._init_plot()

    def _init_plot(self):
        halfThetaSix(self._points)
        self._figure = plt.figure("Example plot")
        axes = plt.subplot(1, 1, 1)
        axes.set_xlim(0, 100)
        axes.set_ylim(0, 100)
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
        self._trigangulation = Delaunay(self._points)
        tri = self._trigangulation
        print tri.simplices
        # for each line:
        #line = lines.Line2D([30, 20], [20, 20])
        #self._axes.add_line(line)
        pltpoints = np.copy(self._points)
        self._axes.cla()
        self._axes.set_ylim(0, 100)
        self._axes.set_xlim(0, 100)
        self._axes.triplot(self._points[:,0], self._points[:,1], tri.simplices)
        self._axes.plot(pltpoints[:,0], pltpoints[:,1], 'bo')
        self._figure.canvas.draw()

if __name__ == "__main__":
    plot = examplePlot()
