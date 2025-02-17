import os
import numpy as np
from scipy.io import savemat

class ExportData():
    
    @staticmethod
    def export_as_mat(data, filename, directory):

        # Validar que el archivo tenga la extensión .mat
        if not filename.endswith('.thrm'):
            filename = filename + ".thrm"

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
