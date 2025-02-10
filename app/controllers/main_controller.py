import cv2
import os
import datetime
import numpy as np
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
from app.models.media import MatFile
from app.models.pixel import Pixel
from app.utils.converter import pixel_to_temperature

class MainController:
    
    __lock                      = threading.Lock()
    __frames_buffer             = deque()
    __frame                     = None
    maxValuePixel               = Pixel()
    minValuePixel               = Pixel()


    def __init__(self):
        self.cap = CameraModel(0, "YUYV")
        self.frameProcessor = FrameProcessor()
        self.fps = self.cap.fps()
        self.lockIn = LockIn(self.fps, 1.0, 0, 3000)
        self.inlive = True
        self.softwarerunning = True
        self.recording = False
        self.lockInPorcentage = 0
        self.lockin_running = False
        self.frameMaxvalue = 255
        self.frameMaxvalue = 255
        self.ret = False
        self.lockin_done = False
        self.capturedFrameslockin = 0
        self.start_time = time.time() 
        self.i = 0

        self.hilo_video = threading.Thread(target=self.Capture_Frame)
        self.hilo_video.start()


    @property
    def FrameBuffer(self) -> deque: 
        return self.__frames_buffer
    
    @property
    def Frame(self) -> deque:
        return self.__frame
    
    @Frame.getter
    def Frame(self) -> deque:
        return self.__frame
    
    @Frame.setter
    def Frame(self,frame):
        self.__frame = frame

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
        colorscale = None
        self.color_mapped_splitted_frame = None
        if self.ret == True:
            if self.lockin_running:
                buffer_ret, self.Frame = self.FrameBuffer                           
                #Se realiza el procesamiento lockin del frame actual
                if buffer_ret:
                    decoded_frame = self.frameProcessor.frame_decoder(self.Frame)
                    self.lockInPorcentage, self.Thermogram_Amplitude, self.Thermogram_Phase, self.Thermogram = self.lockIn.Run_Fourier(decoded_frame)
                    self.lockin_done = True
                    if self.lockInPorcentage == 100:
                        self.lockin_running = False
            else:
                #Formatea el frame segun los parametros seleccionados por el usuario
                self.top_splitted_frame = self.frameProcessor.setFrameSection(self.Frame, "TOP") 
                self.bottom_splitted_frame = self.frameProcessor.setFrameSection(self.Frame, "BOTTOM")
                self.top_splitted_frame_gray = self.frameProcessor.yuv2gray_yuyv(self.top_splitted_frame) 
                self.color_mapped_splitted_frame = self.frameProcessor.setColorMap(self.top_splitted_frame_gray)
                elapsed_time = time.time() - self.start_time
               
                if (elapsed_time > 1):
                    self.minValuePixel, self.maxValuePixel = self.frameProcessor.Get_MaxMin(self.top_splitted_frame_gray, self.bottom_splitted_frame)
                    self.minValuePixel = pixel_to_temperature(self.minValuePixel)
                    self.maxValuePixel = pixel_to_temperature(self.maxValuePixel)
                    self.start_time = time.time()

            if self.recording:
                #Calcula el tiempo transcurrido
                formatted_time = self.elapsed_time()
            
            self.color_mapped_splitted_frame = cv2.cvtColor(self.color_mapped_splitted_frame, cv2.COLOR_BGR2RGB)

        return self.ret, self.color_mapped_splitted_frame, formatted_time, self.recording, self.lockInPorcentage,  self.lockin_running, self.maxValuePixel, self.minValuePixel,colorscale
    
    def create_color_scale(self,min, max, width=25, height=250):
        # Crear una imagen de gradiente vertical (de mínimo a máximo)
        gradient = np.linspace(max, min, int(height * 0.9), dtype=np.uint8).reshape(int((height * 0.9)), 1)
        gradient = np.tile(gradient, (1, int(width / 3)))  # Expandir a lo ancho
        # Aplicar el mapa de colores seleccionado
        color_map = self.frameProcessor.setColorMap(gradient)
        color_map = cv2.cvtColor(color_map, cv2.COLOR_BGR2RGB)
        return color_map

    def elapsed_time (self):
        # Calcular el tiempo transcurrido y formatearlo como hh:mm:ss
        elapsed_time = time.time() - self.recordingstart_time
        formatted_time = time.strftime('%H:%M:%S', time.gmtime(elapsed_time))
        return formatted_time
    
    def change_colorMapVar(self, selected_map):
        self.frameProcessor.setColorMapVar(selected_map)
        
    def start_recording (self):
        """# Seleccionar la ruta para guardar el archivo      
        frame_width = int(self.cap.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(self.cap.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        self.video_saver = VideoSaver(save_dir="./captures/videos", video_name="temp", frame_width=frame_width, frame_height=frame_height, fps = self.cap.fps())
        self.video_saver.start_saving()
     
        # Variable para guardar el tiempo de inicio
        self.recordingstart_time = time.time()
        self.recording = True"""
     
        self.videoframes = []
        # Variable para guardar el tiempo de inicio
        self.recordingstart_time = time.time()

        self.recording = True

    def stop_recording (self):
        self.recording = False
        file_name = simpledialog.askstring("Nombre del archivo", "Introduce el nombre del video:")    
        if file_name:
            ExportData.export_as_mat({"video_frames": self.videoframes}, file_name ,"./captures/videos")
            
            """ # Cerrar el video_writer
            self.video_saver.stop_saving()"""

            """# Renombrar el archivo temporal
            os.rename('./captures/videos/temp.avi', save_path)"""
   
            ###cambiar la ventana emergente por notificacione en la app
            messagebox.showinfo("Éxito", f"El video ha sido guardado como: ./captures/videos/{file_name}")
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
        if not self.inlive:
            self.videoindex = 0
        self.start_time1 = time.time()
    
    def stop_lockin(self):
        self.lockin_running = False

    def reset_Lockin(self):
        self.lockIn.reset_lockin()
        self.lockin_done = False
        self.clearFrameBuffer()
        self.capturedFrameslockin = 0
    
    def export_data(self):
        ExportData.export_as_mat(self.Thermogram_Amplitude, "Amplitude","./")
        ExportData.export_as_mat(self.Thermogram_Phase, "Phase","./")           
        Thermogram_Amplitude_N = Basics.imgNormalize(self.Thermogram_Amplitude)
        Thermogram_Phase_N = Basics.imgNormalize(self.Thermogram_Phase)
        #Save the amplitude and phase thermograms as two .png images 
        cv2.imwrite("./Phase"+".png", Thermogram_Phase_N)
        cv2.imwrite("./Amplitude"+".png",Thermogram_Amplitude_N)

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
    
    def load_file(self, path):
        """Carga una archivo .mat"""
        self.file = MatFile(path)
        self.inlive = False
        self.videoindex = 0
    
    def on_toLive(self):
        self.inlive = True
    
    def release(self):
        self.softwarerunning = False
        self.hilo_video.join()
        self.cap.release()

    def shutdown_system(self):
       # Mostrar el diálogo de confirmación
        response = messagebox.askokcancel("Confirmación", "¿Estás seguro que desea apagar el dispsitivo?")   
        if response:  # Si se presiona "OK"
            os.system("sudo shutdown now")


    """SECOND THREAD: GET THE FRAMES FROM THE THERMAL DETECTOR"""
    def Capture_Frame (self):
        while self.softwarerunning:

            with self.__lock:
                if self.inlive:
                   ret, self.Frame = self.cap.get_frame()
                   if not ret:
                      print("No se pudo leer el frame")
                      break
                   else:
                        if self.recording:
                            self.videoframes.append(self.Frame)

                        self.ret = ret 

                        if self.ret and self.lockin_running and self.capturedFrameslockin <= self.lockIn.get_FinalFrame():
                            self.FrameBuffer = self.Frame
                            self.capturedFrameslockin += 1
                else:
                    time.sleep(0.04)
                    ret, self.Frame = self.file.get_videoFrame(self.videoindex)
                    if not ret:
                        print("No se pudo leer el frame")
                        break  
                    else:
                        self.ret = ret
                        self.videoindex += 1     
                        if self.videoindex >= self.file.totalframes:
                            self.videoindex = 0
                        if self.lockin_running:
                            self.i = self.i+1
                            self.FrameBuffer = self.Frame
                