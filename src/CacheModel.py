

class CacheL1Model():
    def __init__(self,v,d,s,o,tag,data):
        self.v = str(v)
        self.d = str(d)
        self.s = str(s)
        self.o = str(o)
        self.tag = str(tag)
        self.data = str(data)
    def show(self):
        print(self.v,self.d,self.s,self.o,self.tag,self.data)