from app.ui.main_window import MainWindow
from app.controllers.main_controller import MainController


def main():
    # Instanciar los controladoresCameraController
    Controller = MainController()
    
    # Crear la ventana principal, pasando los controladores
    window = MainWindow(Controller)
    
    # Iniciar la interfaz gráfica
    window.run()

if __name__ == "__main__":
    main()
