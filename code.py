from cProfile import run
import sys
import serial
import time
import io
import pynmea2
import math
import numpy as np
import decimal
import threading #test comm
import pyqtgraph as pg
import queue
from pyqtgraph import plot
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets,QtCore, QtGui
from PyQt5.QtWidgets import QDialog, QApplication,QVBoxLayout
from PyQt5.QtCore import QObject, QThread, pyqtSignal
from PyQt5.QtChart import QPolarChart, QChartView, QValueAxis, QScatterSeries



class Worker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(int)
    queue = queue.Queue()

    def cart2pol(x, y):
        rho = np.sqrt(x**2 + y**2)
        phi = np.arctan2(y, x)
        return(rho, phi)
    def pol2cart(phi, rho):
        x = phi * np.cos(rho)
        y = phi * np.sin(rho)
        return(x, y)

    #functieon
    def run(queue):
        """Long-running task."""
        ser = serial.Serial('COM1', 19200, timeout=5.0)
        sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))
        f1 = open('da.txt')
        f2 = open('vn.txt')
       
        while 1:
            try:
                line = sio.readline()
                msg = pynmea2.parse(line)
                if line.startswith('$WIMWV'):
                    Worker.queue.queue.clear()
                    first.valdirvant.setText(str(msg.wind_angle))
                    first.valvantapar.setText(str(msg.wind_speed))
                    da = f1.readline()
                    vn = f2.readline()
                    first.valda.setText(da)
                    first.valvitnav.setText(vn)
                    vn = float(vn)
                    da = float(da)
                    va = (float(msg.wind_speed))
                    dva = (float(msg.wind_angle)) 
                    [ya, xa] = Worker.pol2cart(vn,math.radians(da))
                    [yb, xb] = Worker.pol2cart(-va, math.radians(dva))
                    yc = -ya+yb
                    xc = xa+xb
                    [b,a] = Worker.cart2pol(xc, yc)
                    first.valvitadevvant.setText(str(format(b, '.1f')))
                    if math.degrees(a) <= 270 and math.degrees(a) >180:
                        vantadev = math.degrees(-a)
                        first.valvantadev.setText(str(format(vantadev,'.1f')))
                    else:
                        vantadev = 180-math.degrees(-a)
                        first.valvantadev.setText(str(format(vantadev,'.1f')))
                    Worker.queue.put(da)
                    Worker.queue.put(vn)
                    Worker.queue.put(dva)
                    Worker.queue.put(va)
                    Worker.queue.put(a)
                    Worker.queue.put(b)
                    Worker.queue.put(vantadev)
            except serial.SerialException as e:
                print('Device error: {}'.format(e))
                break
            except pynmea2.ParseError as e:
                print('Parse error: {}'.format(e))
                continue 


class MainWindow(QDialog):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("meteo.ui", self)
        
        #butoane
        self.on.clicked.connect(self.runLongTask)
        self.plot.clicked.connect(self.desen)

        #customizaregrafic
        self.graphWidget.setBackground('white')

        # Add polar grid lines
        self.graphWidget.addLegend()
        self.graphWidget.addLine(x=0, pen=0.2)
        self.graphWidget.addLine(y=0, pen=0.2)
        for r in range(2, 20, 2):
            circle = pg.QtGui.QGraphicsEllipseItem(-r, -r, r * 2, r * 2)
            circle.setPen(pg.mkPen(0.2))
            self.graphWidget.addItem(circle)


    def runLongTask(self):
        self.thread = QThread()
        self.worker = Worker()
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.thread.start()


    def desen(self):
        first.graphWidget.clear()
        first.graphWidget.addLine(x=0, pen=0.2)
        first.graphWidget.addLine(y=0, pen=0.2)
        for r in range(2, 20, 2):
            circle = pg.QtGui.QGraphicsEllipseItem(-r, -r, r * 2, r * 2)
            circle.setPen(pg.mkPen(0.2))
            first.graphWidget.addItem(circle)
        da = first.worker.queue.get()
        vn = first.worker.queue.get()
        dva = first.worker.queue.get()
        va = first.worker.queue.get()
        a = first.worker.queue.get()
        b = first.worker.queue.get()
        vantadev = first.worker.queue.get()
        first.valda_2.setText(str(da))
        first.valdirvant_2.setText(str(format(dva, '.1f')))
        first.valvantadev_2.setText(str(format(vantadev, '.1f')))
        first.valvitnav_2.setText(str(vn))
        first.valvantapar_2.setText(str(va))
        first.valvitadevvant_2.setText(str(format(b, '.1f')))
        first.graphWidget.plot([0,math.radians(da)], [0,-vn], pen ='r', symbol ='o', symbolPen ='r', symbolBrush = 0.5, name ='Ship wind heading')
        first.graphWidget.plot([0,-va],[0,math.radians(dva)],pen ='b', symbol ='o', symbolPen ='b', symbolBrush = 0.5, name ='Apparent Wind')
        #first.graphWidget.plot([math.radians(da),-va],[-vn, math.radians(dva)],pen ='g', symbol ='o', symbolPen ='r', symbolBrush = 0.5)
        #first.graphWidget.plot ([0,-b],[0,-a],pen ='g', symbol ='o', symbolPen ='r', symbolBrush = 0.2, name ='Real Wind')
        first.graphWidget.plot([math.radians(da),-va],[-vn, math.radians(dva)],pen ='g', symbol ='o', symbolPen ='r', symbolBrush = 0.5, name ='Real Wind')

    

   


# main
app = QApplication(sys.argv)
first = MainWindow()
widget = QtWidgets.QStackedWidget()
widget.addWidget(first)
widget.setFixedHeight(770)
widget.setFixedWidth(1100)
widget.show()
try:
    sys.exit(app.exec_())
except:
    print('Exiting')
