import cv2
import os
import datetime
from pathlib import Path
from tkinter import simpledialog, messagebox
import time
from app.models.camera_model import CameraModel
from app.models.mediasaver_model import VideoSaver
from app.models.mediasaver_model import ImageSaver
from app.models.frameprocessor import FrameProcessor

class MainController:
    
    def __init__(self):
        self.cap = CameraModel(0)
        self.frameProcessor = FrameProcessor()
        self.recording = False
        self.frame = None

    def update_frame(self):
        ret, self.frame = self.cap.get_frame()
        formatted_time = None 
        if ret == True:
            #Formatea el frame segun los par'ametros seleccionados por el usuario
            color_mapped_frame = self.frameProcessor.setColorMap(self.frame)
            color_mapped_splitted_frame = self.frameProcessor.setFrameSection(color_mapped_frame, "FULL")   

            if self.recording:
                #Guarda el frame actual
                self.video_saver.save_frame(color_mapped_splitted_frame)
                #Calcula el tiempo transcurrido
                formatted_time = self.elapsed_time()

        color_mapped_splitted_frame_RGB = cv2.cvtColor(color_mapped_splitted_frame, cv2.COLOR_BGR2RGB)
        
        return ret,  color_mapped_splitted_frame_RGB, formatted_time, self.recording
    
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

        self.video_saver = VideoSaver(save_dir="./captures/videos", video_name="temp", frame_width=frame_width, frame_height=frame_height, fps=30)
        self.video_saver.start_saving()
     
        # Variable para guardar el tiempo de inicio
        self.recordingstart_time = time.time()

        self.recording = True

    def stop_recording (self):
        self.recording = False
        self.show_keyboard()
        file_name = simpledialog.askstring("Nombre del archivo", "Introduce el nombre del video:")
        
        if file_name:
            self.hide_keyboard()
            # Asegurarse de que el nombre no tenga extensión
            file_name = os.path.splitext(file_name)[0]  
            save_path = os.path.join(self.video_saver.save_dir, f"{file_name}.avi")
            
            # Cerrar el video_writer
            self.video_saver.stop_saving()

            # Renombrar el archivo temporal
            os.rename('./captures/videos/temp.avi', save_path)
   
            ###cambiar la ventana emergente por notificacione en la app
            messagebox.showinfo("Éxito", f"El video ha sido guardado como: {save_path}")
        else:
            ###cambiar la ventana emergente por notificacione en la app
            messagebox.showwarning("Advertencia", "No se ha guardado el video.")

    def capture_img (self):
            save_dir = Path(os.getcwd()) / "captures/images"  # Carpeta 'capturas' en el directorio actual         
           
            # Crear un nombre de archivo único usando la fecha y hora actual
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            file_name = f"captura_{timestamp}.jpg"
           
            #Formatea el frame segun los par'ametros seleccionados por el usuario
            color_mapped_frame = self.frameProcessor.setColorMap(self.frame)
            color_mapped_splitted_frame = self.frameProcessor.setFrameSection(color_mapped_frame, "FULL")
            
            imageserver = ImageSaver(color_mapped_splitted_frame, save_dir, file_name)
            imageserver.save_image()


    def release(self):
        self.cap.release()

    def shutdown_system(self):
       # Mostrar el diálogo de confirmación
        response = messagebox.askokcancel("Confirmación", "¿Estás seguro que desea apagar el dispsitivo?")   
        if response:  # Si se presiona "OK"
            os.system("sudo shutdown now")
       

 
    def show_keyboard(self):
        # Llamar al teclado embebido de la Raspberry Pi
        os.system('matchbox-keyboard &')

    def hide_keyboard(self):
        # Cerrar el teclado embebido
        os.system('pkill matchbox-keyboard')