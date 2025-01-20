from collections import deque
from app.Function.Methods import Fourier
import numpy as np
from cv2.typing import MatLike

class LockIn ():

    __frame                     = deque()       #Queue of frames to process
    __fourier                   = Fourier()     #lockin method

    def __init__(self, fps, modulation, initFrame, finFrame) -> None:
        self.Fourier.InitFrame = initFrame
        self.Fourier.FinalFrame = finFrame
        self.Modulation =  modulation
        self.FrameRate = fps
       
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
    
    @property
    def InitFrame(self) -> int:
        return self.Fourier.InitFrame
    
    @property
    def FinFrame(self) -> int:
        return self.Fourier.FinalFrame
    
    @property
    def Modulation(self) -> int:
        return self.Fourier.Modulation
    
    @property
    def FPS(self) -> int:
        return  self.Fourier.FrameRate
    
    @property
    def CurrentFrame(self) -> int:
        return  self.Fourier.CurrentFrame
    
    @CurrentFrame.getter
    def CurrentFrame(self) -> int:
        return self.Fourier.CurrentFrame + 1
    
    @InitFrame.setter
    def InitFrame(self, initframe):      
        self.Fourier.InitFrame = initframe

    @FinFrame.setter
    def FinFrame(self, finframe):
        self.Fourier.FinalFrame = finframe

    @Modulation.setter
    def Modulation(self, modulation):
        self.Fourier.Modulation =  modulation

    @FPS.setter
    def FrameRate(self, fps):
        self.Fourier.FrameRate = fps
        
    #  Execute the Fourier Method
    def Run_Fourier(self, img):
        self.__fourier.Thermogram = img
        return  self.__fourier.Porcentage, self.Thermogram_Amplitude, self.Thermogram_Phase, self.__fourier.Thermogram
    
    def get_FinalFrame(self):
        return self.Fourier.FinalFrame
    
    def reset_lockin(self):
        self.Fourier.reset_fourier()


