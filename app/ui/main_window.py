import tkinter as tk
from tkinter import ttk


class MainWindow:
    def __init__(self, controller):
        self.controller = controller
        self.root = tk.Tk()
        self.root.title("Interfaz Táctil - Cámara Térmica")
        self.root.geometry("380x180")
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
        self.recordButton = tk.Button(self.captureFrame, text="Record")
        self.shotButton = tk.Button(self.captureFrame, text="Shot")

        # Crear un marco contenedor para los botones en el captureFrame
        self.buttonFrame = tk.Frame(self.captureFrame)
        self.buttonFrame.pack(fill="both", expand=True)

        self.recordButton.pack(side="top", fill="both", expand=True)
        self.shotButton.pack(side="bottom", fill="both", expand=True)

        # Label para mostrar las imágenes de la cámara térmica
        self.video_label = tk.Label(self.cameraFrame)
        self.video_label.place(relx=0, rely=0, relwidth=1, relheight=1)  # Utilizar place para evitar que el Label cambie el tamaño del Frame

        # Crear un menú desplegable para seleccionar el mapa de colores
        self.color_map_var = tk.StringVar(value="JET")
        self.color_map_menu = ttk.OptionMenu(
            self.optionsFrame, 
            self.color_map_var, 
            "JET", 
            "JET", 
            "HOT", 
            "COOL", 
            "PLASMA", 
            "TURBO", 
            "GRAYS", 
            "ORIGINAL", 
            command=self.change_color_map
        )
        self.color_map_menu.config(width=1)  # Establecer un ancho fijo para el OptionMenu
        self.color_map_menu.grid(row=2, column=0, padx=5, pady=5, sticky="ew")

    def run(self):
        self.root.mainloop()
        