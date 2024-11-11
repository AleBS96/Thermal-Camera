import tkinter as tk

class VirtualKeyboard:
    def __init__(self, master, parent_frame=None, position="bottom"):
        self.master = master
        self.parent_frame = parent_frame or master
        self.position = position

        # Frame que contendrá el teclado
        self.keyboard_frame = tk.Frame(self.parent_frame)
        self.is_visible = False

        # Widget de entrada actual
        self.current_entry = None

        # Configurar botones del teclado
        self._create_keyboard()

        # Vincular el evento de clic en la ventana para verificar el enfoque
        self.master.bind("<Button-1>", self._check_focus_outside)

    def _create_keyboard(self):
        # Filas del teclado QWERTY
        qwerty_keys = [
            '1234567890',  # Números
            'QWERTYUIOP',  # Primera fila de letras
            'ASDFGHJKL',   # Segunda fila de letras
            'ZXCVBNM,.',   # Tercera fila de letras
        ]
        # Botones especiales
        special_keys = [
            ('Espacio', ' '),
            ('Borrar', '<-'),
            ('Enter', '\n')
        ]

        # Crear botones de letras y números
        for row, keys in enumerate(qwerty_keys):
            frame_row = tk.Frame(self.keyboard_frame)
            frame_row.pack()
            for key in keys:
                button = tk.Button(frame_row, text=key, width=3, command=lambda k=key: self._key_press(k))
                button.pack(side=tk.LEFT, padx=2, pady=2)

        # Crear botones especiales
        frame_special = tk.Frame(self.keyboard_frame)
        frame_special.pack()
        for label, key in special_keys:
            button = tk.Button(frame_special, text=label, width=8, command=lambda k=key: self._key_press(k))
            button.pack(side=tk.LEFT, padx=5, pady=2)

    def _key_press(self, key):
        # Insertar el carácter en el campo de texto
        if key == '<-':
            self.current_entry.delete(len(self.current_entry.get()) - 1, tk.END)  # Borrar
        else:
            self.current_entry.insert(tk.END, key)  # Insertar carácter

    def show(self, entry_widget):
        # Vincular el widget de entrada y mostrar el teclado
        self.current_entry = entry_widget
        if not self.is_visible:
            self.is_visible = True
            self._position_keyboard()
            self.keyboard_frame.pack()

    def hide(self):
        # Ocultar el teclado
        if self.is_visible:
            self.is_visible = False
            self.keyboard_frame.pack_forget()

    def _position_keyboard(self):
        # Posicionar el teclado según la propiedad `position`
        if self.position == "bottom":
            self.keyboard_frame.pack(side=tk.BOTTOM)
        elif self.position == "top":
            self.keyboard_frame.pack(side=tk.TOP)
        elif self.position == "left":
            self.keyboard_frame.pack(side=tk.LEFT)
        elif self.position == "right":
            self.keyboard_frame.pack(side=tk.RIGHT)

    def attach_entry(self, entry):
        # Configurar eventos para mostrar el teclado al enfocar un campo de entrada
        entry.bind("<FocusIn>", lambda event: self.show(entry))

    def _check_focus_outside(self, event):
        # Verifica si el clic ocurrió fuera del teclado y del campo de texto actual
        widget = event.widget

        # Verificar si el clic no es en el teclado ni en el campo de texto actual
        # Se utiliza "winfo_containing" para verificar si el clic está dentro del teclado
        if (widget != self.current_entry and
            not self.keyboard_frame.winfo_containing(event.x_root, event.y_root) and
            not isinstance(widget, tk.Entry)):  # Asegúrate de que no es un Entry
            self.hide()

if __name__ == "__main__":
    # Ejemplo de uso
    root = tk.Tk()
    root.geometry("300x400")

    # Crear tres campos de entrada de texto
    entry1 = tk.Entry(root)
    entry1.pack(pady=10)
    entry2 = tk.Entry(root)
    entry2.pack(pady=10)
    entry3 = tk.Entry(root)
    entry3.pack(pady=10)

    # Crear el teclado virtual
    keyboard = VirtualKeyboard(root, position="bottom")

    # Asociar el teclado a los campos de entrada
    keyboard.attach_entry(entry1)
    keyboard.attach_entry(entry2)
    keyboard.attach_entry(entry3)

    root.mainloop()
