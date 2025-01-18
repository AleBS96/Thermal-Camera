import numpy as np

# Crear variable 'videoInf', video de interés para evitar dañar la grabación
videoInf = recording1[192:384, :, :, :]  # Ajuste de índices de 0 en Python

# Obtener la cantidad de frames
tamano_v = videoInf.shape
tamano_i = tamano_v[3]

# Tamaño de la imagen en píxeles (alto x ancho)
altura = tamano_v[0]
ancho = tamano_v[1]

# Inicializar la imagen YUY2 de 16 bits
YUY2_imagen = np.zeros((altura, ancho), dtype=np.uint16)

# Crear las variables consecutivas desde el frame i para borrar los frames iniciales
j = 1

for i in range(999, tamano_i):  # Índices ajustados para empezar desde el frame 1000
    # Extraer las componentes Y, Cb y Cr
    Y = videoInf[:, :, 0, i]
    Cb1 = videoInf[:, :, 1, i]
    Cr1 = videoInf[:, :, 2, i]

    # Asegurar que Cb y Cr tengan la mitad del ancho que Cb1 y Cr1
    Cb = Cb1[:, ::2]  # Submuestreo en la dirección horizontal para Cb
    Cr = Cr1[:, ::2]  # Submuestreo en la dirección horizontal para Cr

    # Intercalar las componentes Y, Cb y Cr en el formato YUY2 (8 bits por componente)
    # El formato YUY2 es: Y1, U, Y2, V para cada par de píxeles
    for fila in range(altura):
        for col in range(0, ancho - 1, 2):  # Iterar sobre cada par de píxeles
            # Asignar valores a los píxeles de la imagen YUY2
            Y1 = float(Y[fila, col])         # Y del primer píxel
            Y2 = float(Y[fila, col + 1])     # Y del segundo píxel
            U = float(Cb[fila, col // 2])    # Cb común para dos píxeles
            V = float(Cr[fila, col // 2])    # Cr común para dos píxeles

            YUY2_imagen[fila, col] = (int(U) << 8) + int(Y1)    # Empaquetar Y1 y U en 16 bits
            YUY2_imagen[fila, col + 1] = (int(V) << 8) + int(Y2)  # Empaquetar Y2 y V en 16 bits

    # Visualizar la imagen YUY2 (descomentar si se quiere mostrar)
    # import matplotlib.pyplot as plt
    # plt.imshow(YUY2_imagen, cmap='gray')
    # plt.show()

    # Convertir a double para el procesamiento LockIn
    YUY2_imagen_d = YUY2_imagen.astype(np.float64)

    # Crear 'FramesXX' con aumento consecutivo para manipulación con Lock-inFelix
    nombre_variable = f"Frame{j}"  # Crear el nombre de la variable
    globals()[nombre_variable] = YUY2_imagen_d  # Guardar la variable en el espacio global
    j += 1
