import cv2
import platform

class CameraModel:

    def __init__(self,index,color_space = "Default") -> None:
        self.cap = cv2.VideoCapture(index)  
        
        # Verificar si la cámara se abrió correctamente
        if not self.cap.isOpened():
            print("CameraModel:Error al abrir la cámara.")    
        
        # Configurar la cámara para que entregue frames en el formato deseado
        if(color_space != "Default"):
            # Obtener el sistema operativo
            os_name = platform.system()
            if(os_name == "Linux"):
                # Configurar para evitar la conversión automática a BGR
                self.cap.set(cv2.CAP_PROP_CONVERT_RGB, 0)
            self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*color_space))
    
    def get_frame(self):
        if self.cap is not None:
            ret, frame = self.cap.read()
            if ret != True:               
                self.cap.release() 

            return ret, frame
        
    def fps (self):
        return self.cap.get(cv2.CAP_PROP_FPS)
    
    #Release camera resources
    def release(self):
        self.cap.release()
