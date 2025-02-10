import numpy as np

class Pixel ():
    __value         = np.uint16
    __x             = int
    __y             = int

    def __init__(self):
        self.__value = 0
        self.eightbitsvalue = 0
        self.__x = 0
        self.__y = 0

    
    @property
    def Value(self):
        return self.__value
    
    @property
    def Position(self):
        return self.__x, self.__y
    
    @Position.getter
    def Position(self):
        return [self.__x, self.__y]

    @Value.getter
    def Value(self):
        return self.__value
    
    @Position.setter
    def Position(self,axis):
        self.__x = axis[0]       
        self.__y = axis[1]
    
    @Value.setter
    def Value(self, value):
        self.__value = value