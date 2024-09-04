from app.ui.main_window import MainWindow
from app.controllers.main_controller import MainController

def main():
    # Crear una instancia del controlador principal
    controller = MainController()
    
    # Crear la ventana principal, pasando el controlador
    window = MainWindow(controller)
    
    # Iniciar la interfaz gráfica
    window.run()

if __name__ == "__main__":
    main()
