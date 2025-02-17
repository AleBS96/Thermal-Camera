import tkinter as tk
from tkinter import ttk
from app.utils.style import Style

class CustomDialog:
    def __init__(self, parent, title, prompt, keyboard):
        self.parent = parent
        self.title = title
        self.prompt = prompt
        self.keyboard = keyboard
        self.result = None

    def show(self):
        # Crear una ventana de diálogo
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title(self.title)

        # Asociar el diálogo con la ventana principal (sin bloquearla)
        self.dialog.transient(self.parent)

        # Centrar el diálogo en la pantalla
        self.center_dialog()

        # Etiqueta con el mensaje
        label = ttk.Label(self.dialog, text=self.prompt, style="ModernDialog.TLabel")
        label.pack(padx= 10, pady=10)

        # Campo de entrada
        self.entry = ttk.Entry(self.dialog, width=40, style="Modern.TEntry")
        self.entry.pack(pady=10)

        # Botón de aceptar
        def on_accept():
            self.result = self.entry.get()
            self.dialog.destroy()

        accept_button = ttk.Button(self.dialog, text="Aceptar", command=on_accept, style="Modern.TButton")
        accept_button.pack(pady=10)

        # Mostrar el teclado virtual cuando se haga clic en el Entry
        def on_entry_click(event):
            self.keyboard.show(self.entry)

        self.entry.bind("<Button-1>", on_entry_click)

        # Esperar a que el diálogo se cierre
        self.dialog.wait_window()

        # Devolver el valor ingresado
        return self.result
    
    def center_dialog(self):
        # Actualizar la ventana para asegurarse de que se conozcan sus dimensiones
        self.dialog.update_idletasks()

        # Obtener las dimensiones de la pantalla
        screen_width = self.parent.winfo_width()
        screen_height = self.parent.winfo_height()

        # Obtener las dimensiones de la ventana del diálogo
        dialog_width = self.dialog.winfo_reqwidth()
        dialog_height = self.dialog.winfo_reqheight()

        # Calcular la posición para centrar la ventana
        x = (screen_width // 2) - (dialog_width // 2)
        y = (screen_height // 2) - (dialog_height // 2)

        # Establecer la posición de la ventana
        self.dialog.geometry(f"+{x}+{y}")
