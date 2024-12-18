import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os

class MainWindow:
    def __init__(self, controller):
        self.controller = controller
        # Variable para manejar el estado de visibilidad de la etiqueta tiempo
        self.time_visivle= False
        self.recording = False
        self.root = tk.Tk()
        self.root.title("Interfaz Táctil - Cámara Térmica")
        self.root.attributes("-fullscreen", True)
        self.counttime = 1000
        # Vincular el evento de cierre de la ventana al método de cierre
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.createWidgets()

    def createWidgets(self):
        self.colormapIcon_height = 60
        self.colormapIcon_width = 60
        #CargarIconos
        self.shutdownIcon = self.load_icon("app/assets/apagar.png",self.colormapIcon_height,self.colormapIcon_width)


        self.loadButtonIcon = self.load_icon("app/assets/file/load.png",self.colormapIcon_height,self.colormapIcon_width) 
        self.recordButtonIcon = self.load_icon("app/assets/capture/iniciargrabacion.png", self.colormapIcon_height + 5,self.colormapIcon_width + 5)
        self.stoprecordButtonIcon = self.load_icon("app/assets/capture/detenergrabacion.png", self.colormapIcon_height + 5,self.colormapIcon_width + 5)
        self.shotButtonIcon = self.load_icon("app/assets/capture/capturaimagen.png", self.colormapIcon_height,self.colormapIcon_width)

        # Cargar imágenes de los mapas de colores
        self.noicon = self.load_icon("app/assets/color_map/nocolormap.png",self.colormapIcon_height,self.colormapIcon_width)  
        self.hoticon = self.load_icon("app/assets/color_map/hot.png",self.colormapIcon_height,self.colormapIcon_width)  
        self.coolicon = self.load_icon("app/assets/color_map/cool.png",self.colormapIcon_height,self.colormapIcon_width)  
        self.plasmaicon = self.load_icon("app/assets/color_map/plasma.png",self.colormapIcon_height,self.colormapIcon_width)
        self.turboicon = self.load_icon("app/assets/color_map/turbo.png",self.colormapIcon_height,self.colormapIcon_width)  
        self.graysicon = self.load_icon("app/assets/color_map/gray.png",self.colormapIcon_height,self.colormapIcon_width)  
        self.jeticon = self.load_icon("app/assets/color_map/jet.png",self.colormapIcon_height,self.colormapIcon_width)
       
        # Crear marco principal
        self.mainFrame = tk.Frame(self.root, bg="white")
        self.mainFrame.pack(fill="both", expand=True)

        # Configurar las columnas del grid en el Frame principal
        self.mainFrame.grid_columnconfigure(0, weight=4)  # Columna izquierda
        self.mainFrame.grid_columnconfigure(1, weight=30) # Columna central
        self.mainFrame.grid_columnconfigure(2, weight=15)  # Columna derecha
        self.mainFrame.grid_rowconfigure(0, weight=1)     # Fila única
 
        # Crear marcos de segundo nivel
        self.optionsFrame = tk.Frame(self.mainFrame, width=30)  # Marco de opciones
        self.cameraFrame = tk.Frame(self.mainFrame)    # Marco para visualizar video la Cámara
        self.parametersFrame = tk.Frame(self.mainFrame)  # Crear marco de parámetros

        # Colocando los marcos en el grid
        self.optionsFrame.grid(row=0, column=0, sticky="nsew")
        self.cameraFrame.grid(row=0, column=1, sticky="nsew")
        self.parametersFrame.grid(row=0, column=2, sticky="nsew")

        # Crear marco Captura de Frames
        self.captureFrame = tk.Frame(self.optionsFrame)
        self.shutdownFrame = tk.Frame(self.optionsFrame)
        self.fileFrame = tk.Frame(self.optionsFrame)
        self.colormapFrame = tk.Frame(self.optionsFrame)

        # Configurar las filas del grid en el Frame opciones
        self.optionsFrame.grid_rowconfigure(0, weight=2)  # Fila Superior
        self.optionsFrame.grid_rowconfigure(1, weight=2)  # Fila Media
        self.optionsFrame.grid_rowconfigure(2, weight=3)  # Fila Inferior
        self.optionsFrame.grid_rowconfigure(3, weight=2)  # Fila Inferior
        self.optionsFrame.grid_columnconfigure(0, weight=1)

        # Colocando los marcos en el grid
        self.shutdownFrame.grid(row=0, column=0, sticky="nsew")
        self.fileFrame.grid(row=1, column=0, sticky="nsew")
        self.captureFrame.grid(row=2, column=0, sticky="nsew")
        self.colormapFrame.grid(row=3, column=0, sticky="nsew")

        # Creando el botón de apagado
        self.shutdownButton = tk.Button(self.shutdownFrame, image=self.shutdownIcon, borderwidth=0, highlightthickness=0, command=self.controller.shutdown_system)
        self.shutdownButton.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        # Creando los botones para gestion de archivos
        self.loadButton = tk.Button(self.fileFrame, image = self.loadButtonIcon, borderwidth=0, highlightthickness=0, command=self.load_image)
        self.loadButton.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        # Creando los botones de captura de frames
        self.recordButton = tk.Button(self.captureFrame, image=self.recordButtonIcon , borderwidth=0, highlightthickness=0, command=self.toggle_recording)
        self.shotButton = tk.Button(self.captureFrame, image=self.shotButtonIcon, borderwidth=0, highlightthickness=0, command=self.capture_image, pady=10)
        self.recordButton.place(relx=0, rely=0, relwidth=1, relheight=0.5)
        self.shotButton.place(relx=0, rely=0.5, relwidth=1, relheight=0.5)

        # Crear un Menubutton para el menú con imagen y sin texto
        self.menubutton = tk.Menubutton(self.colormapFrame, relief="raised", borderwidth=0)
        self.menubutton.place(relx=0, rely=0, relwidth=1, relheight=1)

        # Crear un Menu desplegable
        self.menu = tk.Menu(self.menubutton, tearoff=0)
        self.menubutton.config(menu=self.menu, image=self.noicon)
        
        # Agregar las opciones al menú sin texto (solo imágenes)
        self.menu.add_command(image=self.noicon, command=lambda:self.change_colorMap("ORIGINAL", self.noicon))
        self.menu.add_command(image=self.hoticon, command=lambda:self.change_colorMap("HOT", self.hoticon))
        self.menu.add_command(image=self.coolicon, command=lambda:self.change_colorMap("COOL", self.coolicon))
        self.menu.add_command(image=self.plasmaicon, command=lambda:self.change_colorMap("PLASMA", self.plasmaicon))
        self.menu.add_command(image=self.turboicon, command=lambda:self.change_colorMap("TURBO", self.turboicon))
        self.menu.add_command(image=self.graysicon, command=lambda:self.change_colorMap( "GRAYS", self.graysicon))
        self.menu.add_command(image=self.jeticon, command=lambda:self.change_colorMap("JET", self.jeticon))

        # Crear un canvas para mostrar el video y el tiempo encima
        self.canvas = tk.Canvas(self.cameraFrame)
        self.canvas.place(relx=0, rely=0, relwidth=1, relheight=1)  # Utilizar place para evitar que el Label cambie el tamaño del Frame

        # Crear un texto para mostrar el tiempo y notificacion de capturade imagen
        self.notification = self.canvas.create_text(30, 10, anchor=tk.NW, text='', fill="black", font=("Helvetica", 24))

        self.update_frame() 

    def update_frame(self):
        ret,frame,elapsedtime,self.time_visible = self.controller.update_frame()
        if ret == True:
            img = Image.fromarray(frame)
            img = self.resize_image(img)
            img = ImageTk.PhotoImage(image = img)       
             # Dibujar el video en el canvas
            self.canvas.create_image(0, 0, anchor=tk.NW, image=img)
            self.canvas.img = img 

            if self.time_visible == True:
                # Actualizar el tiempo en el canvas
                self.canvas.itemconfigure(self.notification, text=elapsedtime)
                self.canvas.tag_raise(self.notification)
            
            if self.counttime < 10:
                self.set_notification("Imagen Capturada")

            self.canvas.after(10,self.update_frame)
        else:
            self.canvas.configure(self.notification,text="Camera not found")
            self.canvas.tag_raise(self.notification)
 
    def resize_image(self, img):
         # Redimensionar la imagen al tamaño del Label
        label_width = self.canvas.winfo_width()
        label_height = self.canvas.winfo_height()
        if label_width > 0 and label_height > 0:  # Evitar redimensionar a 0x0
            img = img.resize((label_width, label_height), Image.ANTIALIAS)
        return img
    
    def toggle_recording(self):
        if not self.recording:
            # Inicia la grabación
            self.recording = True
            self.recordButton.config(image=self.stoprecordButtonIcon)
            self.controller.start_recording()
        else:
            # Detiene la grabación y solicita el nombre del archivo
            self.recording = False
            self.recordButton.config(image=self.recordButtonIcon)
            self.controller.stop_recording()
    
    def capture_image(self):
        ##IMPLEMENTAR NOTIFICACION AL USUARIO DE CAPRUTA DE PANTALLA##
        self.controller.capture_img()
        self.counttime = 0

        
    def run(self):
        self.root.mainloop()

    def on_closing(self):
        #Liberar el recurso de la cámara
        self.controller.release()
        self.root.destroy()

    # Función para redimensionar la imagen
    def load_icon(self, ruta, alto, ancho):
        imagen = Image.open(ruta)         # Abre la imagen
        imagen = imagen.resize((ancho, alto), Image.ANTIALIAS)  # Redimensiona la imagen
        return ImageTk.PhotoImage(imagen)  # Convierte la imagen para usar en tkinter

    def change_colorMap(self, color_map, imagen):
            # Cambiar la imagen en el Menubutton cuando se selecciona una opción
        self.menubutton.config(image=imagen)
        self.controller.change_colorMapVar(color_map)

    def load_image(self):
        pass

    def set_notification(self, text):
        self.counttime += 1
        if (self.counttime < 200):
            self.canvas.itemconfigure(self.notification, text=text)
            self.canvas.tag_raise(self.notification)  
       
        