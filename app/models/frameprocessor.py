import cv2

class FrameProcessor:

    colorMapDict = {
        "GRAYS":cv2.COLOR_BGR2GRAY,
        "JET": cv2.COLORMAP_JET,
        "HOT": cv2.COLORMAP_HOT,
        "COOL": cv2.COLORMAP_COOL,
        "PLASMA": cv2.COLORMAP_PLASMA,
        "TURBO": cv2.COLORMAP_TURBO
            }

    def __init__(self) -> None:
        self.colorMapVar = "ORIGINAL"
        self.frameSectionVar = "FULL"

    def setColorMapVar (self, colormapvar):
        self.colorMapVar = colormapvar

    def setFrameSectionVar (self, framesection):
        self.frameSectionVar = framesection
    
    def setColorMap(self, frame):
        if self.colorMapVar == "ORIGINAL":
            color_mapped_frame = frame
        
        elif self.colorMapVar == "GRAYS":
            color_mapped_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
       
        else:
            color_map = self.colorMapDict.get(self.colorMapVar)
            color_mapped_frame = cv2.applyColorMap(frame, color_map)
    
        color_mapped_frame_RGB = cv2.cvtColor(color_mapped_frame, cv2.COLOR_BGR2RGB)
        
        return color_mapped_frame_RGB 
    
    def setFrameSection (self, frame, frameSectionVar):
        if frameSectionVar == "BUTTOM":
            # Get the bottom half of the image
            height, width = frame.shape[:2]
            frame = frame[height // 2:, :]  #separates the bottom half of the image
        elif frameSectionVar == "TOP":
            # Get the bottom half of the image
            height, width = frame.shape[:2]
            frame = frame[:height // 2, :]  #separates the top half of the image
        else:
            frame = frame
        
        return frame
          