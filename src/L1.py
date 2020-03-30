#!/usr/bin/python
#-*- coding: utf-8 -*-

from MemoryHandler import *
from CacheHandler import *
from CacheL1Line import *
from LogManager import *
from CacheModel import *


class L1:

    ASK_FOR_LOCK = "ask_for_lock"
    LOCKED = "LOCKED"
    LOCKED_REPLACING_LINE_INTO_L2 = "LOCKED"
    LOCKED_1 = "LOCKED"
    LOCKED_2 = "LOCKED"
    ASK_FOR_UNLOCK = "ASK_FOR_UNLOCK"
    HIT = "HIT"

    MODE_WR = "WR"
    MODE_RD = "RD"

    def __init__(self,chip_nbr,proc_nbr,memoryHandler,cache_handler):
        self.l = LogManager()
        self.chip_nbr = chip_nbr
        self.proc_nbr = proc_nbr
        self.cache_data = [CacheL1Line(0),CacheL1Line(1)]
        self.cache_handler = cache_handler
        self.cache_handler.add_cache(self)
        self.cache_data[1].setMemoryDirection(1)
        self.cache_data[1].setDatum(1)
        self.current_mem_searching = None
        self.current_datum_to_write = None
        self.state = None
        self.counter = 0
        self.cache_selector = 0
        self.mode = self.MODE_RD

    def is_hit(self,memDir):
        line = self.cache_data[memDir%2]
        return line.getMemoryDirection() == memDir and line.v == 1

    def getDatum(self,memDir):
        if self.cache_data[0].getMemoryDirection() == memDir:
            return self.cache_data[0].getDatum()
        elif self.cache_data[1].getMemoryDirection() == memDir:
            return self.cache_data[1].getDatum()
        else: 
            return None
    


    def update_information(self):
        cache_line = self.cache_data[self.current_mem_searching%2]


    def show(self):
        print("L1: ")
        self.cache_data[0].show()
        self.cache_data[1].show()


    #Memory direction to write/read
    def set_current_search(self,memDir):
        self.current_mem_searching = memDir

    #Define the value of the datum that is going to be written
    def set_current_datum(self,datum):
        self.current_datum_to_write = datum



    def set_ask_lock_state(self):
        self.state = self.ASK_FOR_LOCK



    def set_write_mode(self):
        self.mode = self.MODE_WR
    
    def set_read_mode(self):
        self.mode = self.MODE_RD

    def is_data_loaded(self):
        return self.state == self.HIT
    
    def build_cache_info(self):
        c1 = self.build_cache_line_info(0)
        c2 = self.build_cache_line_info(1)
        return [c1,c2]

    def build_cache_line_info(self,i):
        c = self.cache_data[i]
        return CacheL1Model(c.v,c.d,c.s,c.o,c.memory_direction,c.datum)

    def is_read_instruction(self,rd):
        if rd:
            self.set_read_mode()
        else:
            self.set_write_mode()



    def next_step(self):
        #request the cache handler (cache bus) for a lock.  
        if (self.state == self.ASK_FOR_LOCK):
            self.ask_for_lock()
        elif (self.state == self.LOCKED):
            self.locked()
        elif (self.state == self.ASK_FOR_UNLOCK):
            self.ask_for_unlock()
        return self.is_data_loaded()

  
    """
    States definitions
    ===========================================
    """

    #L1 is asking if it is posible to block the Cache Handler
    #each clock cycle ask the availabity of the cache handler
    def ask_for_lock(self):
        self.l.log("[chip: " + str(self.chip_nbr) +"][proc: " + str(self.proc_nbr) + "] asking for lock")
        if self.cache_handler.lock_cache_handler(self):
            self.state = self.LOCKED
            self.send_cache_bus_request()
    
    #L1 is using the cache handler 
    #for writing and reading info which is not available or updating information in another cache
    def locked(self):
        #if is locked the cache L1 is waiting for cache L2 Response
        if self.cache_handler.next_step():
            self.state = self.ASK_FOR_UNLOCK
        self.l.log("[chip: " + str(self.chip_nbr) +"][proc: " + str(self.proc_nbr) + "] locked")
    
    #
    def ask_for_unlock(self):
        if self.cache_handler.release_cache_handler(self):
            self.state = self.HIT
            self.l.log("[chip: " + str(self.chip_nbr) +"][proc: " + str(self.proc_nbr) + "] setting as hit")
        else:
            self.l.log("[chip: " + str(self.chip_nbr) +"][proc: " + str(self.proc_nbr) + "] No enough permissions to unlock")


    """
    I/O Functions
    ===========================================
    """

    def send_cache_bus_request(self):
        request_type = self.cache_handler.REQUEST_READ
        if self.mode == self.MODE_WR:
            request_type = self.cache_handler.REQUEST_WRITE
        self.cache_handler.set_request_type(request_type)

    def send_cache_l1_request(self, mem_address,value,request_mode):
        self.set_current_search(mem_address)
        self.set_current_datum(value)
        self.is_read_instruction(request_mode)