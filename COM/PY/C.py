class Cal(object):
    def __init__(self, v1, v2):
        if isinstance(v1, int):
            self.v1 = v1
        if isinstance(v2, int):
            self.v2 = v2
    def add(self):
        return self.v1+self.v2
    def subtract(self):
        return self.v1-self.v2
    def setV1(self, v):
        if isinstance(v, int):
            self.v1 = v
    def getV1(self):
        return self.v1

class CalMultiply(Cal):
    def multiply(self):
        return self.v1*self.v2
        
class CalDivide(CalMultiply):
    def divide(self):
        return self.v1/self.v2

