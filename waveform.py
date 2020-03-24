# -*- coding: utf-8 -*-
"""
Demonstrates use of PlotWidget class. This is little more than a
GraphicsView with a PlotItem placed in its center.
"""

from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg

class WaveForm:

    def __init__(self):
        self.widget = pg.PlotWidget(lockAspect=False)
        self.widget.setMouseEnabled(y=False)  # Only allow zoom in X-axis
        self.widget.scene().sigMouseClicked.connect(self._set_pos)
        self.line = pg.InfiniteLine(angle=90, movable=True)
        self.widget.addItem(self.line)
        self.line.setBounds([0, 200])
        self.line.getPos()

    def plot(self, sample):
        time = np.linspace(0, sample.length(), num=sample.nframes())
        curve = self.widget.plot(time, sample.a, autoDownsample=True)
        curve.curve.setClickable(True)
        curve.setDownsampling(ds=256, auto=True, method='peak')
        curve.setPen('w')  ## white pen
        curve.setShadowPen(pg.mkPen((70, 70, 30), width=6, cosmetic=True))
        curve.sigClicked.connect(self._set_pos)
        curve2 = self.widget.plot(time, sample.a, autoDownsample=True)
        curve2.curve.setClickable(True)
        curve2.setDownsampling(ds=256, auto=True, method='mean')
        curve2.setPen('r')  ## white pen
        curve2.setShadowPen(pg.mkPen((70, 70, 30), width=6, cosmetic=True))

    def set_parent(self, parent):
        parent.addWidget(self.widget)

    def _set_pos(self, event):
        self.line.setPos(self.widget.getPlotItem().vb.mapSceneToView(event.scenePos()))

    def audio_position(self):
        return self.line.value()

"""
pw = pg.PlotWidget(name='Plot1')  ## giving the plots names allows us to link their axes together
# l.addWidget(pw)
pw2 = pg.PlotWidget(name='Plot2')
# l.addWidget(pw2)
pw3 = pg.PlotWidget()
l.addWidget(pw3)

mw.show()

## Create an empty plot curve to be filled later, set its pen
p1 = pw.plot()
p1.setPen((200, 200, 100))

## Add in some extra graphics
rect = QtGui.QGraphicsRectItem(QtCore.QRectF(0, 0, 1, 5e-11))
rect.setPen(pg.mkPen(100, 200, 100))
pw.addItem(rect)

pw.setLabel('left', 'Value', units='V')
pw.setLabel('bottom', 'Time', units='s')
pw.setXRange(0, 2)
pw.setYRange(0, 1e-10)


def rand(n):
    data = np.random.random(n)
    data[int(n * 0.1):int(n * 0.13)] += .5
    data[int(n * 0.18)] += 2
    data[int(n * 0.1):int(n * 0.13)] *= 5
    data[int(n * 0.18)] *= 20
    data *= 1e-12
    return data, np.arange(n, n + len(data)) / float(n)


def updateData():
    yd, xd = rand(10000)
    p1.setData(y=yd, x=xd)


## Start a timer to rapidly update the plot in pw
t = QtCore.QTimer()
t.timeout.connect(updateData)
t.start(50)
# updateData()

## Multiple parameterized plots--we can autogenerate averages for these.
for i in range(0, 5):
    for j in range(0, 3):
        yd, xd = rand(10000)
        pw2.plot(y=yd * (j + 1), x=xd, params={'iter': i, 'val': j})

## Test large numbers
curve = pw3.plot(np.random.normal(size=100) * 1e0, clickable=True)
curve.curve.setClickable(True)
curve.setPen('w')  ## white pen
curve.setShadowPen(pg.mkPen((70, 70, 30), width=6, cosmetic=True))


def clicked():
    print("curve clicked")


curve.sigClicked.connect(clicked)

lr = pg.LinearRegionItem([1, 30], bounds=[0, 100], movable=True)
pw3.addItem(lr)
line = pg.InfiniteLine(angle=90, movable=True)
pw3.addItem(line)
line.setBounds([0, 200])

## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys

    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
        """
