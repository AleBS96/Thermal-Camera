import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class MainWindow:
    def __init__(self, controller):
        self.controller = controller
        self.root = tk.Tk()
        self.root.title("Interfaz Táctil - Cámara Térmica")
        self.root.geometry("380x180")
        # Vincular el evento de cierre de la ventana al método de cierre
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.createWidgets()

    def createWidgets(self):
        # Crear marco principal
        self.mainFrame = tk.Frame(self.root, bg="white")
        self.mainFrame.pack(fill="both", expand=True)

        # Configurar las columnas del grid en el Frame principal
        self.mainFrame.grid_columnconfigure(0, weight=1)  # Columna izquierda
        self.mainFrame.grid_columnconfigure(1, weight=12) # Columna central
        self.mainFrame.grid_columnconfigure(2, weight=3)  # Columna derecha
        self.mainFrame.grid_rowconfigure(0, weight=1)     # Fila única
 
        # Crear marcos de segundo nivel
        self.optionsFrame = tk.Frame(self.mainFrame)  # Marco de opciones
        self.cameraFrame = tk.Frame(self.mainFrame)    # Marco para visualizar video la Cámara
        self.parametersFrame = tk.Frame(self.mainFrame)  # Crear marco de parámetros

        # Colocando los marcos en el grid
        self.optionsFrame.grid(row=0, column=0, sticky="nsew")
        self.cameraFrame.grid(row=0, column=1, sticky="nsew")
        self.parametersFrame.grid(row=0, column=2, sticky="nsew")

        # Crear marco Captura de Frames
        self.captureFrame = tk.Frame(self.optionsFrame)
        self.shutdownFrame = tk.Frame(self.optionsFrame)

        # Configurar las filas del grid en el Frame opciones
        self.optionsFrame.grid_rowconfigure(0, weight=1)  # Fila Superior
        self.optionsFrame.grid_rowconfigure(1, weight=1)  # Fila Inferior
        self.optionsFrame.grid_columnconfigure(0, weight=1)

        # Colocando los marcos en el grid
        self.shutdownFrame.grid(row=0, column=0, sticky="nsew")
        self.captureFrame.grid(row=1, column=0, sticky="nsew")

        # Creando el botón de apagado
        self.shutdownButton = tk.Button(self.shutdownFrame, text="OFF", command=self.controller.shutdown_system)
        self.shutdownButton.place(relx=0, rely=0, relwidth=0.5, relheight=0.5)  # Botón ocupa 50% del ancho y 50% del alto del shutdownFrame

        # Creando los botones de captura de frames
        self.recordButton = tk.Button(self.captureFrame, text="Record", command=self.controller.start_recording)
        self.stoprecordButton = tk.Button(self.captureFrame, text="Stop", command=self.controller.stop_recording)
        self.shotButton = tk.Button(self.captureFrame, text="Shot")

        # Crear un marco contenedor para los botones en el captureFrame
        self.buttonFrame = tk.Frame(self.captureFrame)
        self.buttonFrame.pack(fill="both", expand=True)

        self.recordButton.pack(side="top", fill="both", expand=True)
        self.stoprecordButton.pack(side="top", fill="both", expand=True)
        self.shotButton.pack(side="bottom", fill="both", expand=True)

        # Label para mostrar las imágenes de la cámara térmica
        self.video_label = tk.Label(self.cameraFrame, bg = "white")
        self.video_label.place(relx=0, rely=0, relwidth=1, relheight=1)  # Utilizar place para evitar que el Label cambie el tamaño del Frame

        # Crear un Label para mostrar el tiempo de grabación, sobre el video
        self.time_label = ttk.Label( self.video_label, text="00:00:00", font=('Arial', 12), background=None, foreground="red")
        self.time_label.grid(row=0, column=0, sticky="ne", padx=10, pady=10)

        # Crear un menú desplegable para seleccionar el mapa de colores
        self.color_map_var = tk.StringVar(value="ORIGINAL")
        self.color_map_menu = ttk.OptionMenu(
            self.optionsFrame, 
            self.color_map_var, 
            "ORIGINAL",
            "ORIGINAL", 
            "HOT", 
            "COOL", 
            "PLASMA", 
            "TURBO", 
            "GRAYS", 
            "JET",
            direction="above",
            command=self.controller.change_colorMapVar
        ) 
        self.color_map_menu.config(width=4)  # Establecer un ancho fijo para el OptionMenu 
        self.color_map_menu.grid(row=2, column=0, sticky="ew") 
        self.update_frame() 

    
    def update_frame(self):
        ret,frame = self.controller.update_frame()
        if ret == True:
            img = Image.fromarray(frame)
            img = self.resize_image(img)
            img = ImageTk.PhotoImage(image = img)
            self.video_label.image = img 
            self.video_label.configure(image=img)
            self.video_label.after(10,self.update_frame)
        else:
            self.video_label.configure(text="Camera not found")

    
    def resize_image(self, img):
         # Redimensionar la imagen al tamaño del Label
        label_width = self.video_label.winfo_width()
        label_height = self.video_label.winfo_height()
        if label_width > 0 and label_height > 0:  # Evitar redimensionar a 0x0
            img = img.resize((label_width, label_height), Image.ANTIALIAS)
        return img
    
    def run(self):
        self.root.mainloop()

    
    def on_closing(self):
        #Liberar el recurso de la cámara
        self.controller.release()
        self.root.destroy()
        