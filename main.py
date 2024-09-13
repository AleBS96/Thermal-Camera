from app.ui.main_window import MainWindow
from app.controllers.camera_controller import CameraController
from app.controllers.file_controller import FileController
from app.models.camera_model import CameraModel
from app.models.file_model import FileModel


def main():
    # Instanciar los controladores
    cameraController = CameraController(CameraModel())
    fileController = FileController(FileModel())
    
    # Crear la ventana principal, pasando los controladores
    window = MainWindow(cameraController, fileController)
    
    # Iniciar la interfaz gráfica
    window.run()

if __name__ == "__main__":
    main()
