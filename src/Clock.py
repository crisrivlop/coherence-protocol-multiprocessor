#!/usr/bin/python
#-*- coding: utf-8 -*-
from threading import Thread
import time
from LogManager import *


class Clock(Thread):
    def __init__(self,waitTimeMs, group=None, target=None, name=None, args=(), kwargs=None):
        super(Clock,self).__init__(group=group, target=target, name=name)
        self.clk = 0
        self.wait_time = waitTimeMs/1000
    def run(self):
        l = LogManager()
        while True:
            if self.isActive():
                l.getInstance().logSeparator()
            self.clk = (self.clk + 1 ) % 2
            time.sleep(self.wait_time)
    def isActive(self):
        return self.clk == 1
    def waitUntilActive(self):
        while not self.isActive():
            time.sleep(self.wait_time/10)
    def waitUntilUnactive(self):
        while self.isActive():
            time.sleep(self.wait_time/10)