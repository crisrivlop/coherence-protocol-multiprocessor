from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication
import sys
from interface import Ui_MainWindow

class ExampleApp(QtWidgets.QMainWindow, Ui_MainWindow):
	def __init__(self, parent=None):
		super(ExampleApp, self).__init__(parent)
		self.setupUi(self)
		setNoTriggers = [self.cacheL2Chip0,self.cacheL2Chip1,self.cacheL1Proc1Chip0,self.cacheL1Proc1Chip1,self.cacheL1Proc0Chip0,self.cacheL1Proc0Chip1,self.sharedMemory]
		for i in setNoTriggers:
			i.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)

def main():
    app = QApplication(sys.argv)
    form = ExampleApp()
    form.show()
    app.exec_()




if __name__ == '__main__':
	print("calling interface...")
	main()