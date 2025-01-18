import os
import numpy as np
from scipy.io import savemat

class ExportData():
    
    @staticmethod
    def export_as_mat(data, filename, directory):

        # Validar que el archivo tenga la extensión .mat
        if not filename.endswith('.mat'):
            filename = filename + ".mat"

        # Crear el directorio si no existe
        os.makedirs(directory, exist_ok=True)

        # Crear un diccionario para savemat si matlike_data no lo es
        if not isinstance(data, dict):
            data = {'data': data}

        # Construir la ruta completa
        filepath = os.path.join(directory, filename)

        # Guardar los datos en formato .mat
        savemat(filepath, data)

        return filepath

def main():
    # Ejemplo de datos matlike
    matlike_data = {
        'matrix': np.array([[1, 2, 3], [4, 5, 6]]),
        'vector': np.array([7, 8, 9]),
        'value': 42
    }

    filename = "mathlike_example.mat"
    directory = "./output"

    try:
        saved_path = ExportData.export_as_mat(matlike_data, filename, directory)
        print(f"Archivo guardado exitosamente en: {saved_path}")
    except Exception as e:
        print(f"Error al guardar el archivo: {e}")

if __name__ == "__main__":
    main()