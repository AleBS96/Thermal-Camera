import cv2
import os
from app.models.camera_model import CameraModel
from app.models.videosaver_model import VideoSaver
from app.models.frameprocessor import FrameProcessor
from tkinter import simpledialog, messagebox
from PIL import Image, ImageTk

class MainController:
    recording = False
    
    def __init__(self):
        self.cap = CameraModel(0)
        self.frameProcessor = FrameProcessor()

    def update_frame(self):
        ret, frame = self.cap.get_frame(False) 
        if ret == True:
            color_mapped_frame = self.frameProcessor.setColorMap(frame)
            color_mapped_splitted_frame = self.frameProcessor.setFrameSection(color_mapped_frame, "FULL")   

        if self.recording:
             self.video_saver.save_frame(color_mapped_splitted_frame)
             
        return ret, color_mapped_splitted_frame
      
    def change_colorMapVar(self, selected_map):
        self.frameProcessor.setColorMapVar(selected_map)
    
    def start_recording (self):
        # Seleccionar la ruta para guardar el archivo      
        frame_width = int(self.cap.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(self.cap.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        self.video_saver = VideoSaver(save_dir="./captures/videos", video_name="temp", frame_width=frame_width, frame_height=frame_height, fps=25)
        self.video_saver.start_saving()
     
        self.recording = True


    def stop_recording (self):
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


    def release(self):
        self.cap.release()

    def shutdown_system(self):
       os.system("sudo shutdown now")
 
