from collections import deque
import app.Function.Basics as Basics
import numpy as np
from cv2.typing import MatLike

class LockIn ():

    __frame                     = deque()       #Queue of frames to process
    __fourier                   = Basics.Fou()  #lock in method

    def __init__(self, fps, modulation, initFrame, finFrame) -> None:
        self.Fourier.InitFrame = initFrame
        self.Fourier.FinalFrame = finFrame
        self.Fourier.Modulation =  modulation
        self.Fourier.FrameRate = fps
       
    @property
    def Frame(self) -> deque: 
        return self.__frame
    
    @property
    def Fourier(self) -> Basics.Fou: 
        return self.__fourier

    @Frame.getter
    def Frame(self) -> deque:
        self.__frame.append(self.read()) 
        return self.__frame.popleft()

    #  Execute the Fourier Method
    def Run_Fourier(self):
        #Starts the Lock-in
        while self.__fourier.Porcentage < 100:
            ret, img = self.Frame
            if ret:
                self.__fourier.Thermogram = img
            else:
                break



#Para Testeo
if __name__ == "__main__":
  
    camera = LockIn()
    camera.Fourier.InitFrame = 3000
    camera.Fourier.FinalFrame = 10000
    camera.Fourier.Modulation = 60
    #camera.Fourier.FrameRate = camera.get(cv2.CAP_PROP_FPS)
    
    camera.Run_Fourier()

  # Libera los recursos y cierra las ventanas
    camera.release()