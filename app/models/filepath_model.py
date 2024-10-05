#####ESTA CLASE AUN NO SE EMPLEA EN EL PROYECTO PERO ESTA PENDIENTE PARA POSTERIORMENTE IMPLEMENTAR UNA 
#####FUNCIONALIDAD QUE PERMITA AL USUARIO SELECCIONAR LA RUTA DONDE GUARDAR LOS FICEROS 


import os
from tkinter import Tk, filedialog

class FilePathManager:
    def __init__(self, default_dir='.', default_filename='archivo', extension='.avi'):
        """
        Clase que gestiona la selección de rutas para abrir y guardar archivos.

        :param default_dir: Directorio por defecto donde se abrirá el cuadro de diálogo.
        :param default_filename: Nombre del archivo por defecto (para guardar).
        :param extension: Extensión del archivo por defecto (para guardar).
        """
        self.default_dir = default_dir
        self.default_filename = default_filename
        self.extension = extension

    def select_file_to_save(self):
        """
        Abre un cuadro de diálogo para que el usuario seleccione la ruta y nombre del archivo a guardar.
        :return: Ruta completa del archivo seleccionado por el usuario para guardar.
        """
        root = Tk()
        root.withdraw()  # Ocultar la ventana principal de tkinter

        # Cuadro de diálogo para guardar archivo
        file_path = filedialog.asksaveasfilename(
            initialdir=self.default_dir,
            initialfile=self.default_filename,
            defaultextension=self.extension,
            filetypes=[("Archivos", f"*{self.extension}"), ("Todos los archivos", "*.*")]
        )
        directory, file_name = os.path.split(file_path)
        name = os.path.splitext(os.path.basename(file_name))[0]
        root.destroy()
        return directory, name

    def select_file_to_open(self):
        """
        Abre un cuadro de diálogo para que el usuario seleccione un archivo para abrir.
        :return: Ruta completa del archivo seleccionado por el usuario para abrir.
        """
        root = Tk()
        root.withdraw()  # Ocultar la ventana principal de tkinter

        # Cuadro de diálogo para abrir archivo
        file_path = filedialog.askopenfilename(
            initialdir=self.default_dir,
            filetypes=[("Archivos", f"*{self.extension}"), ("Todos los archivos", "*.*")]
        )

        root.destroy()
        return 



#PRUEBA
#if __name__ == "__main__":
#    path_manager = FilePathManager(default_dir='C:/', default_filename='mi_video', extension='.avi')

#    # Seleccionar la ruta para guardar el archivo
#    save_path = path_manager.select_file_to_save()

#    if save_path:
#        print(f"El archivo se guardará en: {save_path}")
#    else:
#        print("No se seleccionó ninguna ruta para guardar.")

#PRUEBA ABRIR ARCHIVO
#if __name__ == "__main__":
#    path_manager = FilePathManager(default_dir='C:/', extension='.avi')

#    # Seleccionar la ruta para abrir un archivo
#    open_path = path_manager.select_file_to_open()

#    if open_path:
#        print(f"El archivo seleccionado para abrir es: {open_path}")
#    else:
#        print("No se seleccionó ningún archivo.")