#!/usr/bin/python
#-*- coding: utf-8 -*-
from threading import Thread
from Instruction import *
from RandomInstructionGenerator import *
from LogManager import *
from L1 import *


class Processor(Thread):


    STATE_LIST = [
        "WAIT_MISS_CACHE_L1"
    ]


    def __init__(self,chip_nbr,nbr,memoryHandler,cache_handler, group=None, target=None, name=None,
                 args=(), kwargs=None):
        super(Processor,self).__init__(group=group, target=target, 
			              name=name)
        self.chip_nbr = chip_nbr
        self.nbr = nbr
        self.cache = L1(chip_nbr,nbr,memoryHandler,cache_handler)
        self.wait = False
        self.r = RandomInstructionGenerator(16,8000)
        self.log = LogManager()
        self.ui_facade = None
        self.clock = None
        self.turned_on = False
        if (nbr == 1):
            self.cache.cache_data[1].v = 1
            self.cache.cache_data[1].d = 1
            self.cache.cache_data[1].datum = 87
            self.cache.cache_data[1].memory_direction = 5


    def next_step(self):
        if self.wait:
            #processor is idle until the status is a hit
            if self.cache.next_step():
                self.wakeup()
        else:
            #apply only for test
            self.generate_instruction()
            if (self.ins.isRD() or self.ins.isWR()):
                tag,datum = self.ins.getTag(),self.ins.getValue()
                #information to the cache desitions
                self.cache.send_cache_l1_request(tag,datum,self.ins.isRD())
                #if there is not a hit
                if(not self.cache.is_hit(tag)):
                    self.cache_miss(tag)
                else:
                    self.cache_hit(tag)
        #updating current informations in cache L1
        self.ui_facade.update_cache_l1(self.chip_nbr,self.nbr,self.build_cache_info())
    


    def generate_instruction(self):
        if (self.nbr == 0):
            self.insertInstruction(Instruction(RD,5,9))
        else:
            self.insertInstruction(self.r.getInstruction())
        #self.insertInstruction(self.r.getInstruction())
        self.log.getInstance().logInstructionGenerated(self.chip_nbr,self.nbr,self.ins) 


    def run(self):
        while(self.turned_on):
            if self.clock.isActive():
                self.next_step()
                self.clock.waitUntilUnactive()
            else:
                self.clock.waitUntilActive()

    def set_ui_facade(self,facade):
        self.ui_facade = facade
    def turn_on(self):
        self.turned_on = True
    def turn_off(self):
        self.turned_on = False


    def cache_miss(self,tag):
        #logging a cache miss
        self.log.getInstance().logCacheL1Miss(self.chip_nbr,self.nbr,tag)
        #wait for the data
        self.wait_for_data()
        #setting the cache initial state
        self.cache.set_ask_lock_state()
        #asking for the next step
        self.cache.next_step()
    
    def cache_hit(self,tag):
        #Logging the hit
        self.log.getInstance().logCacheL1Hit(self.chip_nbr,self.nbr,tag)
        #updating cache information
        self.cache.update_information()



    def process(self):
        pass
    def generateOp(self):
        pass

    def show(self):
        print("Processor: " + str(self.nbr))
        self.cache.show()
    
    
    def insertInstruction(self, ins):
        self.ins = ins

    def getInstruction(self):
        return self.ins
    
    def wait_for_data(self):
        self.wait = True
    
    def wakeup(self):
        self.wait = False

    
    def build_cache_info(self):
        return self.cache.build_cache_info()

    def setClock(self,clk):
        self.clock = clk