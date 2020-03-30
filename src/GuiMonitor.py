#!/usr/bin/python3
#-*- coding: utf-8 -*-

# https://pythonprogramminglanguage.com/pyqt5-hello-world/
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication,QTableWidgetItem
import sys
from gui.interface import Ui_MainWindow
from threading import Thread
import time


class GuiMonitor(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(GuiMonitor, self).__init__(parent)
        self.setupUi(self)
        self.setNoTriggers = [self.cacheL2Chip0,self.cacheL2Chip1,self.cacheL1Proc1Chip0,self.cacheL1Proc1Chip1,self.cacheL1Proc0Chip0,self.cacheL1Proc0Chip1,self.sharedMemory]
        self.setUpdatesEnabled(True)
        for i in self.setNoTriggers:
            i.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.log.setReadOnly(True)

class GuiThread(Thread):
    def __init__(self, group=None, target=None, name=None,args=(), kwargs=None):
        super(GuiThread,self).__init__()
        self.guiMonitor = None

    def run(self):
        while True:
            self.rerender()
    def main(self):
        app = QApplication(sys.argv)
        self.guiMonitor = GuiMonitor()
        self.guiMonitor.setAnimated(True)
        self.guiMonitor.show()
        app.exec_()

    def update_cache_l1(self,chip,core,info):
        if (self.guiMonitor == None):
            return 0
        if (chip == 0):
            if (core == 0):
                self.update_cache_l1_info(self.guiMonitor.cacheL1Proc0Chip0,info)
            elif(core == 1):
                self.update_cache_l1_info(self.guiMonitor.cacheL1Proc1Chip0,info)
        elif(chip == 1):
            if (core == 0):
                self.update_cache_l1_info(self.guiMonitor.cacheL1Proc0Chip1,info)
            elif(core == 1):
                self.update_cache_l1_info(self.guiMonitor.cacheL1Proc1Chip1,info)
        
    def update_cache_l1_info(self,cache,info):
        if (self.guiMonitor == None):
            return 0
        index = 0
        for i in info:
            cache.setItem(index,0,QTableWidgetItem(i.v))
            cache.setItem(index,1,QTableWidgetItem(i.d))
            cache.setItem(index,2,QTableWidgetItem(i.s))
            cache.setItem(index,3,QTableWidgetItem(i.o))
            cache.setItem(index,4,QTableWidgetItem(i.tag))
            cache.setItem(index,5,QTableWidgetItem(i.data))            
            index +=1 
        #print("cache_data")

    def log(self,message):
        if (self.guiMonitor == None):
            return 0
        try:
            self.guiMonitor.log.append(message)
            self.guiMonitor.log.moveCursor(QtGui.QTextCursor.End)
        except:
            pass
    def rerender(self):
        if (self.guiMonitor == None):
            return 0
        for i in self.guiMonitor.setNoTriggers:
            #solution for table update was found in:
            #https://forum.qt.io/topic/10090/solved-qtablewidget-is-not-getting-refreshed-automatically/4
            i.viewport().update()
        time.sleep(1)