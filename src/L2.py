#!/usr/bin/python
#-*- coding: utf-8 -*-
from CacheL2Line import *




class L2:

    INIT_REPLACEMENT = 0


    def __init__(self):
        self.tag_to_write = 0
        self.data_to_write = 0
        self.replacement_state = self.INIT_REPLACEMENT

        self.data = [
            CacheL2Line(0),
            CacheL2Line(1),
            CacheL2Line(2),
            CacheL2Line(3)   
        ]


    def setMemoryHandler(self, memHandler):
        pass

    def replacement(self,old_tag,old_data):
        self.tag_to_write = old_tag
        self.data_to_write = old_data
        self.replacement_state = self.INIT_REPLACEMENT
    def replacement_next_step(self):
        if self.replacement_state == self.INIT_REPLACEMENT:
            is_necessary_a_memory_access = True
            tag = self.tag_to_write
            #there is space at the correponding block
            condition = (self.data[tag%2].v == 0 or self.data[tag%2].tag == self.tag_to_write)
            if (condition):
                is_necessary_a_memory_access = False
                self.data[x].v = 1
                self.data[x].tag = self.tag_to_write
                self.data[x].data = self.data_to_write
                
            if is_necessary_a_memory_access:
                pass
        else:
            pass

    def replacement_done(self):
        return False
