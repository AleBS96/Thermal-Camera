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
from app.models.lockin_model import LockIn

class MainController:
    
    def __init__(self):
        self.cap = CameraModel(0)
        self.frameProcessor = FrameProcessor()
        self.lockIn = LockIn(self.cap.fps(), 60.0, 0, 10000)
        self.recording = False
        self.lockInPorcentage = 0
        self.lockin_running = False
        self.frame = None

    def update_frame(self):
        ret, self.frame = self.cap.get_frame()
        formatted_time = None 
        if ret == True:
            
            if self.lockin_running:
                #Se realiza el procesamiento locin del frame actual
                self.lockInPorcentage, self.Thermogram_Amplitude, self.Thermogram_Phase = self.lockIn.Run_Fourier(self.frame)
                
                if self.lockInPorcentage >= 100:
                    self.lockin_running = False
                    #Save the amplitude and phase thermograms as two .png images
                    cv2.imwrite("./Amplitude1.png", self.lockIn.Fourier.Thermogram_Amplitude)
                    cv2.imwrite("./Phase1.png", self.lockIn.Fourier.Thermogram_Phase)

            #Formatea el frame segun los par'ametros seleccionados por el usuario
            color_mapped_frame = self.frameProcessor.setColorMap(self.frame)
            color_mapped_splitted_frame = self.frameProcessor.setFrameSection(color_mapped_frame, "TOP")   

            if self.recording:
                #Guarda el frame actual
                self.video_saver.save_frame(color_mapped_splitted_frame)
                #Calcula el tiempo transcurrido
                formatted_time = self.elapsed_time()
                
        color_mapped_splitted_frame_RGB = cv2.cvtColor(color_mapped_splitted_frame, cv2.COLOR_BGR2RGB)
        
        return ret, color_mapped_splitted_frame_RGB, formatted_time, self.recording, self.lockInPorcentage,  self.lockin_running,
    
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

        self.video_saver = VideoSaver(save_dir="./captures/videos", video_name="temp", frame_width=frame_width, frame_height=frame_height, fps = self.cap.fps())
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
            color_mapped_splitted_frame = self.frameProcessor.setFrameSection(color_mapped_frame, "TOP")
            
            imageserver = ImageSaver(color_mapped_splitted_frame, save_dir, file_name)
            imageserver.save_image()

    def on_frEntry_change(self, fr):
        self.lockIn.Fourier.FrameRate = fr
        
    def on_modEntry_change(self, mod):
        self.lockIn.Fourier.Modulation = mod

    def on_initEntry_change(self, init):
        self.lockIn.Fourier.InitFrame = init

    def on_finEntry_change(self, fin):
        self.lockIn.Fourier.FinalFrame = fin

    def start_lockin(self):
        self.lockin_running = True
    
    def stop_lockin(self):
        self.lockin_running = False

    def reset_Lockin(self):
        self.lockIn.reset_lockin()
    
    def get_Thermogram_Amplitude(self):
        return self.Thermogram_Amplitude
    
    def get_Thermogram_Phase(self):
        return self.Thermogram_Phase

    def release(self):
        self.cap.release()

    def shutdown_system(self):
       # Mostrar el diálogo de confirmación
        response = messagebox.askokcancel("Confirmación", "¿Estás seguro que desea apagar el dispsitivo?")   
        if response:  # Si se presiona "OK"
            os.system("sudo shutdown now")
        
    
