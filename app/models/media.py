import numpy as np
from scipy.io import loadmat

class MatFile ():
    
    def __init__(self, path):
        self.data = loadmat(path)
        # Extraer la matriz del video
        self.video_frames =self.data[list(self.data.keys())[3]]
        self.totalframes = self.video_frames.shape[0]

    def get_videoFrame(self, index):
        return True , self.video_frames[index,:,:,:]
    
"""if __name__ == "__main__":
    MatFile("video.mat")"""