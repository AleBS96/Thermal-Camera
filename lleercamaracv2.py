import cv2
import numpy as np
import matplotlib.pyplot as plt

def frame_decoder(imagen):
        # Get the bottom half of the image
    height, width = imagen.shape[:2]
    imagen_seccionada = imagen[height // 2:, :]  #separates the bottom half of the image
        
    # Separar los canales Y, Cb y Cr
    Y = imagen_seccionada[:, :, 0]   # Luminancia
    Cb1 = imagen_seccionada[:, :, 1] # Crominancia azul

    # Obtener dimensiones de Y
    height, width = Y.shape

    # Inicializar la imagen YUY2 como una matriz de 16 bits
    Decoded_image = np.zeros((height, width), dtype=np.uint16)

    # Intercalar las componentes Y, Cb y Cr en el formato YUY2 (16 bits por componente)
    # El formato YUY2 es: Y1, U, Y2, V para cada par de píxeles.
    for row in range(height):
        for col in range(0, width, 2):  # Iterar sobre cada par de píxeles
            # Obtener los valores Y1, Y2, U y V
            Y1 = int(Y[row, col])           # Y del primer píxel
            Y2= int(Y[row, col + 1])       # Y del segundo píxel
            U = int(Cb1[row, col])      # Cb común para dos píxeles
            V = int(Cb1[row, col + 1])      # Cr común para dos píxeles

            # Empaquetar Y1 y U en 16 bits
            Decoded_image[row, col] = (U << 8) | Y1
            # Empaquetar Y2 y V en 16 bits
            Decoded_image[row, col + 1] = (V << 8) | Y2

    return  Decoded_image


# Abre la cámara
cap = cv2.VideoCapture(0)

# Verifica si la cámara está abierta correctamente
if not cap.isOpened():
    print("No se pudo abrir la cámara")
    exit()

# Configurar la cámara para que entregue frames en el formato YUY2
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'YUYV'))

x = 0
while x < 100:
    x += 1
    # Captura un frame
    ret, frame = cap.read()
    
    if not ret:
        print("No se pudo leer el frame")
        break
    
    imagen = cv2.cvtColor(frame, cv2.COLOR_YUV2BGR_YUYV)
    frame = frame_decoder(frame)
 
    # Muestra el frame
    cv2.imshow("Frame en YCbCr",  imagen)

    # Presiona 'q' para salir
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Visualizar la imagen YUY2
plt.figure()
plt.imshow(frame , cmap='gray', aspect='auto')
plt.title("Imagen YUY2")
plt.axis('off')

plt.show()

# Libera los recursos y cierra las ventanas
cap.release()
cv2.destroyAllWindows()
