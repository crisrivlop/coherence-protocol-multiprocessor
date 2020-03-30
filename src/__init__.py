from CacheHandler import * 
from Processor import * 
from Chip import * 
from LogManager import *
from GuiMonitor import *
import time
from CacheModel import *
from Clock import *

dir(Chip)


def set_up_chip(mychip,ui,clock):
    mychip.init(clock,ui)
    


if __name__ == "__main__":
    ui = GuiThread()
    clock = Clock(1000)
    mychip = Chip(0,None)
    mychip2 = Chip(1,None)
    l = LogManager()
    l.getInstance().set_facade(ui)


    clock.start()
    set_up_chip(mychip,ui,clock)
    set_up_chip(mychip2,ui,clock)
    
    ui.start()
    ui.main()


    mychip.turn_off()
    mychip2.turn_off()
    mychip.join()
    mychip2.join()
    