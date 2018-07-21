from __future__ import unicode_literals
import sys
import os
import random
import matplotlib

matplotlib.use('Qt5Agg')
from PyQt5 import QtCore, QtWidgets

from numpy import arange, sin, pi
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.collections import LineCollection

from datetime import datetime

temps = []
temp_x = []

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

temp_sensor_blue = '/sys/bus/w1/devices/28-0417c1167aff/w1_slave'
temp_sensor_black = '/sys/bus/w1/devices/28-0517c161ccff/w1_slave'

def read_temp_raw( device_file ):
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines
 
def read_temp( device_file ):
    lines = read_temp_raw(device_file)
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw(device_file)
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c


class TempSensorGraph(FigureCanvas):
	def __init__(self, parent=None, width=5, height=4, dpi=100):
		fig = Figure(figsize=(width, height), dpi=dpi)
		self.axes = fig.add_subplot(111, aspect='equal')
		
		FigureCanvas.__init__(self, fig)
		self.setParent(parent)

		FigureCanvas.setSizePolicy(self, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
		FigureCanvas.updateGeometry(self)

		self.timer = QtCore.QTimer(self)
		self.timer.timeout.connect(self.update_figure)
		self.timer.start(100)

	def update_figure(self):
		temp = read_temp(temp_sensor_blue)
		print(temp)
		temps.append( temp )
		temp_x.append( len(temp_x) + 1 )
		
		self.axes.cla()
		self.axes.plot(temp_x, temps, 'r')
		self.draw()


class ApplicationWindow(QtWidgets.QMainWindow):
	def __init__(self):
		QtWidgets.QMainWindow.__init__(self)
		self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
		self.setWindowTitle("application main window")

		self.file_menu = QtWidgets.QMenu('&File', self)
		self.file_menu.addAction('&Quit', self.fileQuit,
								 QtCore.Qt.CTRL + QtCore.Qt.Key_Q)
		self.menuBar().addMenu(self.file_menu)

		self.help_menu = QtWidgets.QMenu('&Help', self)
		self.menuBar().addSeparator()
		self.menuBar().addMenu(self.help_menu)

		self.help_menu.addAction('&About', self.about)

		self.main_widget = QtWidgets.QWidget(self)

		l = QtWidgets.QVBoxLayout(self.main_widget)
		dc = TempSensorGraph(self.main_widget, width=5, height=4, dpi=100)
		l.addWidget(dc)

		self.main_widget.setFocus()
		self.setCentralWidget(self.main_widget)

		self.statusBar().showMessage("Brew", 2000)

	def fileQuit(self):
		self.close()

	def closeEvent(self, ce):
		self.fileQuit()

	def about(self):
		QtWidgets.QMessageBox.about(self, "About", "Brewing" )

		
qApp = QtWidgets.QApplication(sys.argv)

aw = ApplicationWindow()
aw.setWindowTitle("Brew")
aw.show()
sys.exit(qApp.exec_())
#qApp.exec_()
