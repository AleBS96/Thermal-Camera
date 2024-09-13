import cv2
import os
from app.models.camera_model import CameraModel
import imutils
from PIL import Image, ImageTk

class CameraController:
    colorMapDict = {
        "GRAYS":cv2.COLOR_BGR2GRAY,
        "JET": cv2.COLORMAP_JET,
        "HOT": cv2.COLORMAP_HOT,
        "COOL": cv2.COLORMAP_COOL,
        "PLASMA": cv2.COLORMAP_PLASMA,
        "TURBO": cv2.COLORMAP_TURBO
            }
    colorMapVar = "ORIGINAL"
    
    def __init__(self):
        self.cap = CameraModel()

    def show_video(self):
        ret, frame = self.cap.get_frame()
        if ret == True:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            color_mapped_frame = self.change_color_map(frame)
            img = Image.fromarray(color_mapped_frame)           
        return ret, img
    
    def change_colorMapVar(self, selected_map):
        self.colorMapVar = selected_map

    def change_color_map (self, frame):
        if self.colorMapVar == "ORIGINAL":
            color_mapped_frame = frame
        else:
            color_map = self.colorMapDict.get(self.colorMapVar)
            color_mapped_frame = cv2.applyColorMap(frame, color_map)
        return color_mapped_frame 

    def release(self):
        self.cap.release()

    def shutdown_system(self):
       os.system("sudo shutdown now")
 
