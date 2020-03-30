#!/usr/bin/python
#-*- coding: utf-8 -*-

from threading import Lock
from LogManager import *
from L2 import *
#import numpy as np

"""
        #read
        #dato existe en cache y es valido
        #si
            #definido anteriormente
            #realiza update o realiza read
        #no
            #esta definicion misma
            #L1 envia la solitud de lectura al bus

            #!!! MISMO_NIVEL_CACHE <- el dato esta a mismo nivel de cache? (cache del otro chip) 
            #se valida que en el cache solicitado tenga espacio. tiene espacio?
            #si
                #pasar al estado [REPLACE_CACHE_LINE]
            #no
                # elegir cual hoja se va a reemplazar. (random/lru)
                # esperar hasta que L2 este disponible para la escritura
                # secuestrar L2 para la escritura
                # L2 tiene espacio?
                # si
                    #escribir el dato sobre L2
                    # si MISMO_NIVEL_CACHE es falso:
                        #está el dato en L2?
                        #si
                            #obtener el dato
                        #no
                            #NO DEFINIDO AUN

                # no
                    #NO DEFINIDO AUN
                #liberar L2
                
                #pasar al estado [REPLACE_CACHE_LINE]
            ======================== END ========================
            Estado:[REPLACE_CACHE_LINE]
            consu
"""


class CacheHandler:

    LOCK_CACHE = "LOCK_CACHE"
    UNLOCK_CACHE = "UNLOCK_CACHE"


    REQUEST_READ = "READ"
    REQUEST_WRITE= "WRITE"


    FREE_CACHE_SPACE_STATE = "VERIFYING_CACHE_SPACE_STATE"

    REPLACE_CACHE_LINE = "REPLACE_CACHE_LINE"

    REPLACE_CACHE_LINE_DONE = "REPLACE_CACHE_LINE_DONE"

    def __init__(self):
        self.lock = Lock()
        self.cache_subscription_list = []
        self.active_cache = None
        self.available = True
        self.l = LogManager()
        self.load_l1_direction = 0
        self.state = self.FREE_CACHE_SPACE_STATE
        self.asked_L2 = False
        self.cache_l2 = L2()
    
    def add_cache(self,cache):
        self.cache_subscription_list.append(cache)

    def getDatum(self):
        self.l.getInstance().log('Not Defined Yet!')

    def lock_cache_handler_aux(self,cache):
        can_lock = False
        if self.available:
            #self.l.getInstance().log("At [chip: " + str(cache.chip_nbr) + "][processor: " + str(cache.proc_nbr) + "] Locking")
            self.active_cache = cache
            self.available = False
            can_lock = True
        return can_lock
    def release_cache_handler_aux(self,cache):
        can_release = False
        #self.l.getInstance().log("UnLocking")
        if self.active_cache == cache and not self.available:
            self.active_cache = None
            self.available = True
            can_release = True
        return can_release


    def release_cache_handler(self,cache):
        return self.request_cache_handler(cache,self.UNLOCK_CACHE)

    def lock_cache_handler(self,cache):
        return self.request_cache_handler(cache,self.LOCK_CACHE)

    def request_cache_handler(self,cache,request_type):
        resquest_response = False
        self.lock.acquire()

        if(request_type == self.LOCK_CACHE):
            resquest_response = self.lock_cache_handler_aux(cache)
        elif(request_type == self.UNLOCK_CACHE):
            resquest_response = self.release_cache_handler_aux(cache)

        self.lock.release()

        return resquest_response


    def set_request_type(self,request_type):
        self.asked_L2 = False
        self.request_type = request_type

    def next_step(self):
        if self.state == self.FREE_CACHE_SPACE_STATE:
            #available space in cache
            self.free_cache_space_state()
            pass
        
        #this is going to down the current page to L2 cache
        #and then is going to load the information
        elif self.state == self.REPLACE_CACHE_LINE:
            self.replace_cache_line()
            pass
        return self.state == self.REPLACE_CACHE_LINE_DONE
    
        

    def free_cache_space_state(self):
        #asociativity include: direct mapping
        tag = self.active_cache.current_mem_searching
        if self.active_cache.cache_data[tag%2].d == 0 :
            self.load_l1_direction = tag%2
            self.state = self.REPLACE_CACHE_LINE
        else:
            self.state = self.REPLACE_CACHE_LINE_DONE
            #there is not space in cache
            #replacement is necessary: prune by asociativity
            #if not self.asked_L2:
            #    self.load_l1_direction = tag%2
            #    self.cache_l2.replacement(self.active_cache.current_mem_searching,self.active_cache.current_datum_to_write)
            #self.cache_l2.replacement_next_step()
            #if self.cache_l2.replacement_done():
            #    self.state = self.REPLACE_CACHE_LINE
            #print("free_cache_space_state for valid cache lines not defined yet!")
            #pass
    
    def replace_cache_line(self):
        tag = self.load_l1_direction
        ca = self.cache_subscription_list[self.active_cache.proc_nbr]
        cb = self.cache_subscription_list[(self.active_cache.proc_nbr+1)%2]
        #reemplazar cuando dirty
        
        if cb.cache_data[tag%2].d == 1 and cb.cache_data[tag%2].v == 1 and cb.cache_data[tag%2].memory_direction  == ca.current_mem_searching:
            #there is space in cache
            lineA = ca.cache_data[tag%2]
            lineB = cb.cache_data[tag%2]
            lineA.set_cache_line_state(lineA.M)
            lineB.set_cache_line_state(lineB.O)
            lineA.memory_direction = ca.current_mem_searching
            lineA.datum = lineB.datum

            print("replacing or sharing the data")
            self.state = self.REPLACE_CACHE_LINE_DONE
        else:
            print("replacing or sharing the data 2")
            #there is not space in cache
            #replacement is necesary
            #call replacement request in L2 cache
            self.state = self.REPLACE_CACHE_LINE_DONE
        