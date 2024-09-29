import cv2
import os
import datetime
from pathlib import Path
from tkinter import simpledialog, messagebox
import time
from app.models.camera_model import CameraModel
from app.models.videosaver_model import VideoSaver
from app.models.frameprocessor import FrameProcessor

class MainController:
    recording = False
    
    def __init__(self):
        self.cap = CameraModel(0)
        self.frameProcessor = FrameProcessor()

    def update_frame(self):
        ret, frame = self.cap.get_frame()
        formatted_time = None 
        if ret == True:
            color_mapped_frame = self.frameProcessor.setColorMap(frame)
            color_mapped_splitted_frame = self.frameProcessor.setFrameSection(color_mapped_frame, "FULL")   

            if self.recording:
                #Guarda el frame actual
                self.video_saver.save_frame(color_mapped_splitted_frame)
                #Calcula el tiempo transcurrido
                formatted_time = self.elapsed_time()

        return ret, color_mapped_splitted_frame, formatted_time, self.recording
    
    def elapsed_time (self):
        # Calcular el tiempo transcurrido y formatearlo como hh:mm:ss
        elapsed_time = time.time() - self.recordingstart_time
        formatted_time = time.strftime('%H:%M:%S', time.gmtime(elapsed_time))
        return formatted_time
    
    def change_colorMapVar(self, selected_map):
        self.frameProcessor.setColorMapVar(selected_map)
        
    def start_recording (self):
        # Seleccionar la ruta para guardar el archivo      
        frame_width = int(self.cap.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(self.cap.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        self.video_saver = VideoSaver(save_dir="./captures/videos", video_name="temp", frame_width=frame_width, frame_height=frame_height, fps=25)
        self.video_saver.start_saving()
     
        # Variable para guardar el tiempo de inicio
        self.recordingstart_time = time.time()

        self.recording = True

    def stop_recording (self):
        self.recording = False

        file_name = simpledialog.askstring("Nombre del archivo", "Introduce el nombre del video:")
        
        if file_name:
            # Asegurarse de que el nombre no tenga extensión
            file_name = os.path.splitext(file_name)[0]  
            save_path = os.path.join(self.video_saver.save_dir, f"{file_name}.avi")
            
            # Cerrar el video_writer
            self.video_saver.stop_saving()

            # Renombrar el archivo temporal
            os.rename('./captures/videos/temp.avi', save_path)
            messagebox.showinfo("Éxito", f"El video ha sido guardado como: {save_path}")
        else:
            messagebox.showwarning("Advertencia", "No se ha guardado el video.")

    def capture_img (self):
        ret, frame = self.cap.get_frame()
        if ret:
            save_dir = Path(os.getcwd()) / "captures/images"  # Carpeta 'capturas' en el directorio actual
            
            # Crear el directorio si no existe
            if not save_dir.exists():
                save_dir.mkdir(parents=True, exist_ok=True)
            
            # Crear un nombre de archivo único usando la fecha y hora actual
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            file_name = f"captura_{timestamp}.jpg"
            
            # Ruta completa del archivo (con pathlib que maneja correctamente caracteres especiales)
            save_path = save_dir / file_name

            # Convertir la ruta a string en formato UTF-8 para OpenCV
            save_path_str = str(save_path)
            print(save_path_str)
            cv2.imwrite(save_path_str, frame) 
        else:
            messagebox.showwarning("Advertencia", "No se ha guardado el video.")

    def release(self):
        self.cap.release()

    def shutdown_system(self):
       os.system("sudo shutdown now")
 
