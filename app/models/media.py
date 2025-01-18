import numpy as np
from scipy.io import loadmat

class Video ():
    
    def __init__(self, path):
        self.data = loadmat(path)
        # Extraer la matriz del video
        self.video_frames = self.data['Decoded_video']  # La clave 'Video' puede variar según el archivo

    def get_videoFrame(self, index):
        return True , self.video_frames[:,:,index]
