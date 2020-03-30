#!/usr/bin/python
#-*- coding: utf-8 -*-

class CacheL1Line:

    M = "M"
    O = "O"
    S = "S"
    I = "I"

    def __init__(self,blocknumber):
        self.v = 0
        self.d = 0
        self.s = 0
        self.o = 0
        self.datum = 0
        self.coherence_status = 0
        self.memory_direction = 0
        self.block_number = 0
    def getMemoryDirection(self):
        return self.memory_direction
    def setMemoryDirection(self,memory_direction):
        self.memory_direction = memory_direction
    def getDatum(self):
        return self.datum
    def setDatum(self,datum):
        self.datum = datum
    def show(self):
        print('CacheL1Line: ',self.datum,self.coherence_status,self.memory_direction,self.block_number)
    
    def toString(self):
        return 'CacheL1Line: ' + str(self.datum) + ", " + str(self.coherence_status) +", "+ str(self.memory_direction) + ", " + str(self.block_number)
    
    def set_cache_line_state(self,state):
        self.coherence_status = state
        if state == self.M:
            self.v = 1
            self.d = 1
            self.s = 0
            self.o = 0

        elif state == self.O:
            self.o = 1
            self.v = 1
            self.d = 1
            self.s = 1
            
        elif state == self.S: 
            self.s = 1
            self.v = 1
            self.d = 0
            self.o = 0
        elif state == self.I: 
            self.v = 0
            self.o = 0