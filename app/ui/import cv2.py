import cv2
import tkinter as tk
from tkinter import Label
from PIL import Image, ImageTk
import time

class VideoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Video con tiempo transcurrido")

        # Captura de video desde la cámara USB (índice 0)
        self.cap = cv2.VideoCapture(0)

        # Comprobamos si la cámara está disponible
        if not self.cap.isOpened():
            print("Error al acceder a la cámara.")
            return

        # Crear Label para mostrar el video
        self.video_label = Label(root)
        self.video_label.pack()

        # Crear Label para mostrar el tiempo transcurrido
        self.time_label = Label(root, text="", font=("Helvetica", 16), bg="yellow")
        self.time_label.pack()

        # Variable para guardar el tiempo de inicio
        self.start_time = time.time()

        # Actualizar el video y el tiempo transcurrido cada 10 ms
        self.update_video()

        # Cerrar la cámara cuando la ventana se cierra
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def update_video(self):
        # Leer frame de la cámara
        ret, frame = self.cap.read()
        if ret:
            # Convertir el frame de BGR a RGB
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # Convertir el frame a imagen de tkinter
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)
            self.video_label.imgtk = imgtk
            self.video_label.configure(image=imgtk)

        # Calcular el tiempo transcurrido
        elapsed_time = time.time() - self.start_time
        self.time_label.config(text=f"Tiempo transcurrido: {int(elapsed_time)} s")

        # Llamar a esta función de nuevo después de 10 ms
        self.root.after(10, self.update_video)

    def on_close(self):
        # Liberar la cámara y cerrar la ventana
        self.cap.release()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoApp(root)
    root.mainloop()
