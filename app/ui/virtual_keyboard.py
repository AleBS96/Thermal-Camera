import tkinter as tk

class VirtualKeyboard:
    def __init__(self, root):
        self.root = root
        self.frame = tk.Frame(root, bg="lightgray")
        self.frame.place(x=0, rely=1.0, relwidth=1.0, anchor="sw")  # Fijar en la parte inferior


        # Teclas del teclado en minúsculas
        self.keys_lower = [
            ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'],
            ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p'],
            ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l'],
            ['z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.'],
            ['_',' ', '←', 'Shift']  # Barra espaciadora, tecla de borrar y Shift
        ]

        # Teclas del teclado en mayúsculas
        self.keys_upper = [
            ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'],
            ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
            ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'],
            ['Z', 'X', 'C', 'V', 'B', 'N', 'M', ',', '.'],
            ['_',' ', '←', 'Shift']  # Barra espaciadora, tecla de borrar y Shift
        ]

        # Estado inicial: minúsculas
        self.shift_active = False
        self.keys = self.keys_lower

        # Crear botones del teclado
        self.create_buttons()

        # Ocultar el teclado inicialmente
        self.frame.place_forget()

        # Variable para almacenar el Entry activo
        self.active_entry = None

    def create_buttons(self):
        # Limpiar el frame antes de recrear los botones
        for widget in self.frame.winfo_children():
            widget.destroy()

        # Crear botones del teclado
        for row in self.keys:
            row_frame = tk.Frame(self.frame, bg="lightgray")
            row_frame.pack()
            for key in row:
                button = tk.Button(
                    row_frame, text=key, width=4, height=2,
                    command=lambda k=key: self.on_key_press(k))
                button.pack(side=tk.LEFT, padx=2, pady=2)
        

    def on_key_press(self, key):
        if self.active_entry:
            if key == '←':
                # Borrar el último carácter
                self.active_entry.delete(len(self.active_entry.get()) - 1, tk.END)
            elif key == 'Shift':
                # Cambiar entre mayúsculas y minúsculas
                self.shift_active = not self.shift_active
                self.keys = self.keys_upper if self.shift_active else self.keys_lower
                self.create_buttons()  # Recrear los botones con el nuevo estado
            elif key == ' ':
                # Insertar un espacio
                self.active_entry.insert(tk.END, ' ')
            else:
                # Insertar la tecla presionada
                self.active_entry.insert(tk.END, key)

    def show(self, entry_widget):
        self.active_entry = entry_widget  # Asignar el Entry activo
        self.frame.place(x=0, rely=1.0, relwidth=1.0, anchor="sw")  # Fijar en la parte inferior


    def hide(self):
        self.active_entry = None  # Limpiar el Entry activo
        self.frame.place_forget()
