from app.ui.main_window import MainWindow
from app.controllers.camera_controller import CameraController

def main():
    # Crear una instancia del controlador principal
    controller = CameraController()
    
    # Crear la ventana principal, pasando el controlador
    window = MainWindow(controller)
    
    # Iniciar la interfaz gráfica
    window.run()

if __name__ == "__main__":
    main()
