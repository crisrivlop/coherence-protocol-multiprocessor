
RD   = "RD"
WR   = "WR"
CALC = "CALC"


class Instruction():
    def __init__(self,Itype,tag,value):
        self.type = Itype
        self.tag = tag
        self.value = value
    def toString(self):
        if self.type == RD:
            return self.type + " " + str(self.tag)
        elif self.type == WR:
            return self.type + " " + str(self.tag) + ", " + str(self.value)
        else:
            return self.type
    def isRD(self):
        return self.type == RD
    def isWR(self):
        return self.type == WR
    def isCALC(self):
        return self.type == CALC
    def getType(self):
        return self.type
    
    def getTag(self):
        return self.tag

    def getValue(self):
        return self.value