from app.ui.main_window import MainWindow
from app.controllers.main_controller import MainController
from app.controllers.file_controller import FileController
from app.models.file_model import FileModel


def main():
    # Instanciar los controladoresCameraController
    cameraController = MainController()
    fileController = FileController(FileModel())
    
    # Crear la ventana principal, pasando los controladores
    window = MainWindow(cameraController)
    
    # Iniciar la interfaz gráfica
    window.run()

if __name__ == "__main__":
    main()
