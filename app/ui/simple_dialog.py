import tkinter as tk
from tkinter import simpledialog

class TextDialog(simpledialog.Dialog):
    def __init__(self, parent, title):
        '''self.keyboard = keyboard'''
        super().__init__(parent, title=title)
        self.body(parent)

    def body(self, master):
        """Construye el diálogo con un campo de texto"""
        tk.Label(master, text="Ingrese texto:").pack(pady=10)
        self.text_input = tk.Entry(master, font=("Arial", 14))
        self.text_input.pack(pady=10, fill=tk.X)
        
        '''# Mostrar el teclado cuando se abre el diálogo
        self.keyboard.show()

        # Detectar clics en cualquier parte de la ventana
        self.bind("<Button-1>", self.click_handler)'''
        
        return self.text_input  # Enfocar el campo de texto

    '''def click_handler(self, event):
        """Maneja los clics dentro y fuera del campo de texto y el teclado"""
        widget = event.widget

        # Verificar si el clic fue en el campo de texto
        if widget == self.text_input:
            self.keyboard.show()
        # Verificar si el clic no fue en el teclado
        elif not self.is_click_on_keyboard(widget):
            self.keyboard.hide()

    def is_click_on_keyboard(self, widget):
        """Verifica si el clic fue en el teclado virtual"""
        # Recorrer el árbol de widgets hasta la raíz para verificar si pertenece al teclado
        while widget:
            if widget == self.keyboard.keyboard_frame:
                return True
            widget = widget.master
        return False'''

    def apply(self):
        """Toma el valor del campo de texto"""
        self.result = self.text_input.get()
        '''self.keyboard.hide()  # Ocultar el teclado cuando el diálogo se cierre'''