import cv2

class CameraModel:
    def __init__(self,index) -> None:
        self.cap = cv2.VideoCapture(index)      
    
    def get_frame(self):
        if self.cap is not None:
            ret, frame = self.cap.read()
            if ret != True:               
                self.cap.release() 

            return ret, frame
    
    #Release camera resources
    def release(self):
        self.cap.release()
