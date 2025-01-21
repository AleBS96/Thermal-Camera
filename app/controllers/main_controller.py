import cv2
import os
import datetime
from pathlib import Path
from tkinter import simpledialog, messagebox
import time
import threading
from collections import deque
import app.Function.Basics as Basics
from app.models.camera_model import CameraModel
from app.models.mediasaver_model import VideoSaver
from app.models.mediasaver_model import ImageSaver
from app.models.frameprocessor import FrameProcessor
from app.models.lockin_model import LockIn
from app.models.exportData_model import ExportData
from app.models.media import Video

class MainController:
    
    __lock                      = threading.Lock()
    __frames_buffer             = deque()

    def __init__(self):
        self.cap = CameraModel(0, "YUYV")
        #self.video = Video("video.mat")
        self.frameProcessor = FrameProcessor()
        self.fps = self.cap.fps()
        self.lockIn = LockIn(self.fps, 1.0, 0, 3000)
        self.softwarerunning = True
        self.recording = False
        self.lockInPorcentage = 0
        self.lockin_running = False
        self.frame = None
        self.ret = False
        self.lockin_done = False
        self.capturedFrameslockin = 0
        self.delay = 1/self.cap.fps()
  
        #self.n = 0
        self.i = 3000

        self.hilo_video = threading.Thread(target=self.Capture_Frame)
        self.hilo_video.start()


    @property
    def FrameBuffer(self) -> deque: 
        return self.__frames_buffer

    @FrameBuffer.getter
    def FrameBuffer(self) -> deque:
        if len(self.__frames_buffer) != 0:
            return True, self.__frames_buffer.popleft()
        else:
            return False, None
        
    @FrameBuffer.setter
    def FrameBuffer(self, frame):
        self.__frames_buffer.append(frame)
 
    def clearFrameBuffer(self):
        self.__frames_buffer.clear()

    def update_frame(self):
        formatted_time = None
        b = self.lockIn.CurrentFrame
        color_mapped_splitted_frame_RGB = None
        if self.ret == True:
            if self.lockin_running:
                buffer_ret, buffer_frame = self.FrameBuffer                
                
                #Se realiza el procesamiento lockin del frame actual
                if buffer_ret:
                    decoded_frame = self.frameProcessor.frame_decoder(buffer_frame)
                    self.lockInPorcentage, self.Thermogram_Amplitude, self.Thermogram_Phase, self.Thermogram = self.lockIn.Run_Fourier(decoded_frame)
                    self.lockin_done = True
                    a = self.lockIn.CurrentFrame
                    if self.lockInPorcentage == 100:
                        ExportData.export_as_mat(self.Thermogram_Amplitude, "Amplitude","./")
                        ExportData.export_as_mat(self.Thermogram_Phase, "Phase","./")           
                        Thermogram_Amplitude_N = Basics.imgNormalize(self.Thermogram_Amplitude)
                        Thermogram_Phase_N = Basics.imgNormalize(self.Thermogram_Phase)
                        #Save the amplitude and phase thermograms as two .png images 
                        cv2.imwrite("./Phase"+".png", Thermogram_Phase_N )
                        cv2.imwrite("./Amplitude"+".png",Thermogram_Amplitude_N)
                        self.lockin_running = False

            #Formatea el frame segun los par'ametros seleccionados por el usuario
            self.color_mapped_frame = self.frameProcessor.setColorMap(self.frame)
            self.color_mapped_splitted_frame = self.frameProcessor.setFrameSection(self.color_mapped_frame, "TOP") 
            if self.recording:
                #Guarda el frame actual
                 self.video_saver.save_frame(self.color_mapped_splitted_frame)
                 #Calcula el tiempo transcurrido
                 formatted_time = self.elapsed_time()
                
            color_mapped_splitted_frame_RGB = cv2.cvtColor(self.color_mapped_splitted_frame, cv2.COLOR_BGR2RGB)

        return self.ret, color_mapped_splitted_frame_RGB, formatted_time, self.recording, self.lockInPorcentage,  self.lockin_running,
    
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
             
            self.save_image(self.color_mapped_splitted_frame, save_dir, file_name)

    def save_image(self, image, image_save_dir, image_name):       
        imageserver = ImageSaver( image, image_save_dir, image_name)
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
        self.start_time1 = time.time()
    
    def stop_lockin(self):
        self.lockin_running = False

    def reset_Lockin(self):
        self.lockIn.reset_lockin()
        self.lockin_done = False
        self.clearFrameBuffer()
        self.capturedFrameslockin = 0

    def get_Thermogram_Amplitude(self):
        Thermogram_Amplitude_N = Basics.imgNormalize(self.Thermogram_Amplitude)
        Thermogram_Amplitude_N_RGB = cv2.cvtColor(Thermogram_Amplitude_N, cv2.COLOR_BGR2RGB)
        return Thermogram_Amplitude_N_RGB
    
    def get_Thermogram_Phase(self):
        Thermogram_Phase_N = Basics.imgNormalize(self.Thermogram_Phase)
        Thermogram_Phase_N_RGB = cv2.cvtColor(Thermogram_Phase_N, cv2.COLOR_BGR2RGB)
        return Thermogram_Phase_N_RGB

    def is_lockin_done(self):
        return self.lockin_done
    
    def release(self):
        self.softwarerunning = False
        self.cap.release()

    def shutdown_system(self):
       # Mostrar el diálogo de confirmación
        response = messagebox.askokcancel("Confirmación", "¿Estás seguro que desea apagar el dispsitivo?")   
        if response:  # Si se presiona "OK"
            os.system("sudo shutdown now")

    """ SECOND THREAD: GET THE FRAMES FROM THE THERMAL DETECTOR"""
    def Capture_Frame (self):
        adframes = 0
        index = 0
        start_time = time.time()
        while self.softwarerunning:
            with self.__lock:      
                ret, encoded_frame = self.cap.get_frame()
                #ret, encoded_frame = self.video.get_videoFrame(index)

                if not ret:
                    print("No se pudo leer el frame")
                    break
               
                self.frame = self.frameProcessor.yuv2bgr_yuyv(encoded_frame)
                self.ret = ret
                
                #adframes += 1
                if(adframes == self.fps):
                    elapsed_time = time.time() - start_time
                    print(f"Time for {self.fps}: {elapsed_time:.2f}")
                    adframes = 0
                    start_time = time.time()
                
                if self.ret and self.lockin_running and self.capturedFrameslockin <= self.lockIn.get_FinalFrame():
                    #color_mapped_frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
                    self.FrameBuffer = encoded_frame
                    self.capturedFrameslockin += 1
                    #if(index < 2999):
                    #    index += 1
                    
                #time.sleep(0.01)

                """ if(self.capturedFrameslockin > self.lockIn.get_FinalFrame()):
                    # Calcula el tiempo transcurrido
                    elapsed_time1 = time.time() - self.start_time1
                    print(f"Time for 3000: {elapsed_time1:.2f}")"""
                
                """if self.ret:
                    if self.ret and self.lockin_running and self.i<8000:
                        # Extraer la matriz del video # La clave 'Video' puede variar según el archivo
                        self.frame = self.video.video_frames[:, :, 0, self.i]  # Extraer el frame i
                        self.i = self.i+1
                        self.FrameBuffer = self.frame
                else:
                    self.frame = self.video.video_frames[:, :, 0, self.i]  # Extraer el frame i
                    self.ret = 1"""

                    

    
