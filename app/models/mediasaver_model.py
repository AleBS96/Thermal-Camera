import cv2
import os
from pathlib import Path

class VideoSaver:
    def __init__(self, save_dir='videos', video_name='video_00', frame_width=256, frame_height=192, fps=30):
        # Directorio donde se guardará el video
        self.save_dir = save_dir
        self.video_name = video_name
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.fps = fps
        self.video_writer = None

        # Crear directorio si no existe
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)

    def start_saving(self):
        # Crear el nombre completo del archivo de video
        video_path = os.path.join(self.save_dir, f"{self.video_name}.avi")
        
        # Definir el codec y crear el VideoWriter para guardar el video
        fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        self.video_writer = cv2.VideoWriter(video_path, fourcc, self.fps, (self.frame_width, self.frame_height))

        # Verificar si el VideoWriter se inicializó correctamente
        if not self.video_writer.isOpened():
            print("Error: No se pudo inicializar el VideoWriter")

    def save_frame(self, frame):
        if self.video_writer is not None:
            # Guardar el frame en el archivo de video
            self.video_writer.write(frame)

    def stop_saving(self):
        # Liberar el VideoWriter
        if self.video_writer is not None:
            self.video_writer.release()
            self.video_writer = None


class ImageSaver:
    
    def __init__(self, frame = None, save_dir = "images", image_name = "image_00") -> None:
        # Directorio donde se guardará el video
        self.frame = frame
        self.save_dir = save_dir
        self.image_name = image_name


    def save_image(self):
        #Se conforma la ruta en que se va a guardar la imagen agregandole el nombre del archivo
        save_path = self.save_dir / self.image_name
        
        #Si no existe una ruta se crea
        if not (self.save_dir.exists()):
            self.save_dir.mkdir(parents=True, exist_ok=True)
            
        # Convertir la ruta a string en formato UTF-8 para OpenCV
        save_path_str = str(save_path)
        print(save_path_str)
          
        cv2.imwrite(save_path_str , self.frame) 
