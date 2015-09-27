#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Created on Mon Apr 20 19:20:34 2015
This program currently works to just bring in data and parse it 
into something meaningful.
Plots real time Magnetometer data (HMC5983)
USED with the Arduino HMC_5983_LOG.ino code
Data is coming in at 230400 baud as comma separated data formatted by the Arduino.

CHECK OUT https://gist.github.com/turbinenreiter/7898985
for more details on how to plot serial data in PyQTgraph

Also, Check out   www.pyqtgraph.org

@author: rtb 9/27/2015
"""
from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
from pyqtgraph.ptime import time
import sys
import serial
import codecs

app = QtGui.QApplication([])
#p = pg.plot()
#p.setWindowTitle('live plot from serial')
#curve = p.plot()
#data1 = [0]

bytecount = 300   # This variable sets the number of bytes to read in
cnt = 0
XA = []
YA = []
ZA = []

#win = pg.GraphicsWindow()
#win.setWindowTitle('pyqtgraph example: Scrolling Plots')
#p1 = win.addPlot()
#p2 = win.addPlot()
p=pg.plot()
p.setWindowTitle('Live Plot from Serial')
p.setInteractive(True)
curve = p.plot(pen=(255,0,0), name="Red X curve")
curve2 = p.plot(pen=(0,255,0), name="Green Y curve")
curve3 = p.plot(pen=(0,0,255), name="Blue Z curve")
data = [0]
data2 = [0]
data3 = [0]

ser = serial.Serial('COM32', 230400, timeout=1)  # open first serial port
ser.close()
ser.open()

print ('Opening', ser.name)          # check which port was really used
print('Reading Serial port =',bytecount,'bytes')  # Maybe read as bytearray?

def update():
    global curve, data, curve2, data2, curve3, data3
    line = codecs.decode((ser.readline()),'ascii')
    DataArray = line.split(',')
    X = int(DataArray[0])
    Y = int(DataArray[1])
    Z = int(DataArray[2])    
    data.append(int(X))
    data2.append(int(Y))
    data3.append(int(Z))
    #xdata = np.array(data, dtype='float64')
    curve.setData(data)
    curve2.setData(data2)
    curve3.setData(data3)
    app.processEvents()

timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(0)

if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()   

