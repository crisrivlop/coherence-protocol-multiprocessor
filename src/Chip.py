#!/usr/bin/python
#-*- coding: utf-8 -*-

from CacheHandler import *
from Processor import *
from Clock import *
from L1 import *

class Chip:
    def __init__(self,nbr,memoryHandler):
        self.clock = None
        self.cache_handler = CacheHandler()
        self.nbr = nbr
        self.processor1 = Processor(nbr,0,memoryHandler,self.cache_handler)
        self.processor2 = Processor(nbr,1,memoryHandler,self.cache_handler)

    def set_clock(self,clk):
        self.clock = clk
        self.processor1.setClock(clk)
        self.processor2.setClock(clk)

    def getNumber(self):
        return self.nbr
    def run(self):
        self.processor1.process()
    def show(self):
        print("Chip: " + str(self.nbr))
        self.processor1.show()
        self.processor2.show()

    def init(self,clock,ui):
        self.turn_on()
        self.set_clock(clock)
        self.processor1.set_ui_facade(ui)
        self.processor2.set_ui_facade(ui)
        self.processor1.wakeup()
        self.processor2.wakeup()
        self.processor1.start()
        self.processor2.start()

    def turn_off(self):
        self.processor1.turn_off()
        self.processor2.turn_off()
    def turn_on(self):
        self.processor1.turn_on()
        self.processor2.turn_on()
    def join(self):
        self.processor1.join()
        self.processor2.join()

