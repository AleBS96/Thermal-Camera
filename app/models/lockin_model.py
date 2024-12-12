from collections import deque
from app.Function.Methods import Fourier
import numpy as np
from cv2.typing import MatLike

class LockIn ():

    __frame                     = deque()       #Queue of frames to process
    __fourier                   = Fourier()  #lock in method

    def __init__(self, fps, modulation, initFrame, finFrame) -> None:
        self.Fourier.InitFrame = initFrame
        self.Fourier.FinalFrame = finFrame
        self.Fourier.Modulation =  modulation
        self.Fourier.FrameRate = fps
       
    @property
    def Frame(self) -> deque: 
        return self.__frame
    
    @property
    def Thermogram_Amplitude(self):
        return self.Fourier.Thermogram_Amplitude
    
    @property
    def Thermogram_Phase(self):
        return self.Fourier.Thermogram_Phase
    
    @property
    def Fourier(self) -> Fourier: 
        return self.__fourier

    @Frame.getter
    def Frame(self) -> deque:
        if len(self.__frame) != 0:
            ret = True
        else:
            ret = False
        return ret, self.__frame.popleft()
    
    @Frame.setter
    def Frame(self, frame):
        self.__frame.append(frame)
        
    #  Execute the Fourier Method
    def Run_Fourier(self, img):
        self.Frame = img
        #Starts the Lock-in
        ret, frame = self.Frame
        if ret:
            self.__fourier.Thermogram = frame

        return  self.__fourier.Porcentage, self.Thermogram_Amplitude, self.Thermogram_Phase
    
    
    def reset_lockin(self):
        self.Fourier.reset_fourier()

