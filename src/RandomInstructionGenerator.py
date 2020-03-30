import math
import numpy as np
from Instruction import *


class RandomInstructionGenerator():

    def __init__(self,memorySize,maxMemoryValue):
        self.memsize = memorySize
        self.max = maxMemoryValue
    def random(self):
        return np.random.poisson(self.max)
    
    def getInstructionType(self):
        type = ""
        random_value = self.random()
        if random_value%3 == 0:
            type = RD
        elif random_value%3 == 1:
            type = CALC
        else:
            type = WR
        return type
    def getAccessTag(self):
        return self.random()%self.memsize
    def getValueToWrite(self):
        return  self.random()%self.max

    def getInstruction(self):
        ins = Instruction(self.getInstructionType(),self.getAccessTag(),self.getValueToWrite())
        #ins = Instruction(CALC,self.getAccessTag(),self.getValueToWrite())
        return ins


if __name__ == "__main__":
    foo = RandomInstructionGenerator(16,1000)
    rd = 0
    wr = 0
    calc = 0
    for i in range(200):
        ins = foo.getInstruction()
        print(ins.toString())
        if ins.isCALC():
            calc += 1
        elif ins.isRD():
            wr += 1
        else:
            rd += 1
    
    print("RD > " + str(rd))
    print("WR > " + str(wr))
    print("CL > " + str(calc))