import cv2
import os

class VideoSaver:
    def __init__(self, save_dir='videos', video_name='output', frame_width=256, frame_height=192, fps=30):
        # Directorio donde se guardará el video
        self.save_dir = save_dir
        self.video_name = video_name
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.fps = fps
        self.video_writer = None

        # Crear directorio si no existe
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)

    def start_saving(self):
        # Crear el nombre completo del archivo de video
        video_path = os.path.join(self.save_dir, f"{self.video_name}.avi")
        
        # Definir el codec y crear el VideoWriter para guardar el video
        # Para Windows, 'MJPG' o 'XVID' suelen funcionar bien
        fourcc = cv2.VideoWriter_fourcc(*'MJPG')  # Prueba también 'XVID'
        self.video_writer = cv2.VideoWriter(video_path, fourcc, self.fps, (self.frame_width, self.frame_height))

        # Verificar si el VideoWriter se inicializó correctamente
        if not self.video_writer.isOpened():
            print("Error: No se pudo inicializar el VideoWriter")

    def save_frame(self, frame):
        if self.video_writer is not None:
            # Guardar el frame en el archivo de video
            self.video_writer.write(frame)

    def stop_saving(self):
        # Liberar el VideoWriter
        if self.video_writer is not None:
            self.video_writer.release()
            self.video_writer = None

'''if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: No se pudo abrir la cámara")
        exit()

    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    video_saver = VideoSaver(save_dir='videos', video_name='mi_video', frame_width=frame_width, frame_height=frame_height, fps=30)
    video_saver.start_saving()

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: No se pudo leer el frame de la cámara")
            break

        cv2.imshow('Frame', frame)

        video_saver.save_frame(frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    video_saver.stop_saving()
    cv2.destroyAllWindows()'''