
from threading import Lock
class LogManager:

    class LogManager:
        def __init__(self):
            self.lck = Lock()
            self.facade = None
        def logCacheL1Miss(self,chip,processor,ref):
            self.log(self.logHead(chip,processor) +  "There is a L1 miss searching the block " + str(ref) )
        def logCacheL1Hit(self,chip,processor,ref):
            self.log(self.logHead(chip,processor) +  "There is a L1 HIT searching the block " + str(ref) )
        def logHead(self,chip,processor):
            return "At [chip:" + str(chip) + "][processor: " +str(processor)+ "], "
        def logInstructionGenerated(self,chip,processor,instruction):
            self.log( self.logHead(chip,processor) + "Instruction Generated: " + instruction.toString())
        def logSeparator(self):
            self.log( "===============================================================================" )
        def log(self,message):
            self.lck.acquire()
            #print( message)
            self.facade.log(message)
            self.lck.release()
        def set_facade(self,facade):
            self.facade = facade

    instance = None
    
    def __init__(self):
        if not LogManager.instance:
            LogManager.instance = LogManager.LogManager()
    def __getattr__(self, name):
        return getattr(self.instance, name)
    def getInstance(self):
        return self.instance