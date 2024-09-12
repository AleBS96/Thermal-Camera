import cv2

class CameraModel:
    def __init__(self) -> None:
        self.cap = cv2.VideoCapture(0)      
    
    def get_frame(self, half = True):
        if self.cap is not None:
            ret, frame = self.cap.read()
            if ret == True:
                if half == True:
                    # Get the bottom half of the image
                    height, width = frame.shape[:2]
                    frame = frame[height // 2:, :]  #separates the bottom half of the image
            else:
                self.cap.release() 
            return ret, frame
    
    #Release camera resources
    def release(self):
        self.cap.release()
