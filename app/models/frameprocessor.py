import cv2
import numpy as np
from app.models.pixel import Pixel

class FrameProcessor:

    colorMapDict = {
        "JET": cv2.COLORMAP_JET,
        "HOT": cv2.COLORMAP_WINTER,
        "COOL": cv2.COLORMAP_PLASMA,
        "PLASMA": cv2.COLORMAP_COOL,
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
        else:
            color_map = self.colorMapDict.get(self.colorMapVar)
            color_mapped_frame = cv2.applyColorMap(frame, color_map) 
          
        return color_mapped_frame
    
    def setFrameSection (self, frame, frameSectionVar):
        if frameSectionVar == "BOTTOM":
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

    def frame_decoder(self,imagen):
        """summary for frame_decoder
        The function receives  an image in YUYV format distributed in 2 
        arrays.One with the Y luminances and others with the UV chromances 
        (CbCr) and is returned in a 16-bit matrix in the form UYVY

        Args:
            imagen ([type]): [image to be processed]

        Returns:
            [type]: [Processed image]
        """
            
        # Separar los canales Y, Cb y Cr
        Y = imagen[:, :, 0]   # Luminancia
        Cb1 = imagen[:, :, 1] # Crominancia azul

        # Obtener dimensiones de Y
        height, width = Y.shape

        # Inicializar la imagen YUY2 como una matriz de 16 bits
        Decoded_image = np.zeros((height, width), dtype=np.uint16)

        # Intercalar las componentes Y, Cb y Cr en el formato YUY2 (16 bits por componente)
        # El formato YUY2 es: Y1, U, Y2, V para cada par de píxeles.
        for row in range(height):
            for col in range(0, width, 2):  # Iterar sobre cada par de píxeles
                # Obtener los valores Y1, Y2, U y V
                Y1 = int(Y[row, col])           # Y del primer píxel
                Y2= int(Y[row, col + 1])       # Y del segundo píxel
                U = int(Cb1[row, col])      # Cb común para dos píxeles
                V = int(Cb1[row, col + 1])      # Cr común para dos píxeles

                # Empaquetar Y1 y U en 16 bits
                Decoded_image[row, col] = (U << 8) | Y1
                # Empaquetar Y2 y V en 16 bits
                Decoded_image[row, col + 1] = (V << 8) | Y2

        return Decoded_image.astype(np.float64)
    
    def pixel_decoder(self,pixel):
        return np.float64((int(pixel[1]) << 8) | pixel[0])

    def Get_MaxMin (self, grayFrame, frame):
        maxPixel = Pixel()
        minPixel = Pixel()
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(grayFrame)
        maxPixel.eightbitsvalue = max_val
        minPixel.eightbitsvalue = min_val
        maxPixel.Position = max_loc
        minPixel.Position = min_loc

        minPixel.Value = self.pixel_decoder(frame[minPixel.Position[1],minPixel.Position[0]])
        maxPixel.Value = self.pixel_decoder(frame[maxPixel.Position[1],maxPixel.Position[0]])

        return minPixel, maxPixel
    
    def yuv2gray_yuyv (self, frame):
        return cv2.cvtColor(frame, cv2.COLOR_YUV2GRAY_YUYV)
    
    
