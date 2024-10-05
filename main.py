from app.ui.main_window import MainWindow
from app.controllers.main_controller import MainController


def main():
    # Instanciar los controladoresCameraController
    cameraController = MainController()
    
    # Crear la ventana principal, pasando los controladores
    window = MainWindow(cameraController)
    
    # Iniciar la interfaz gráfica
    window.run()

if __name__ == "__main__":
    main()
