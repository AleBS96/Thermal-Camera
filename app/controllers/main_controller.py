from app.models.model import DataModel
import os

class MainController:
    def __init__(self):
        self.model = DataModel()

    def change_color_map(self, selected_map):
        # Cambiar el mapa de colores basado en la selección del usuario
        self.color_map = selected_map
        print(f"Color map changed to: {self.color_map}")

    def shutdown_system(self):
       os.system("sudo shutdown now")

    def on_closing(self):
        # Liberar el recurso de la cámara
        self.cap.release()
        self.root.destroy()