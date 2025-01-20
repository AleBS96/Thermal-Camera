from tkinter import ttk

class Style:
    def __init__(self, master):
        self.style = ttk.Style(master)
        
        # Estilo general para botones
        self.style.configure(
            "Modern.TButton",
            font=("Helvetica", 14, "bold"),
            relief="flat", 
            anchor="nsew",
            borderwidth=0,
            background="#FFFFFF",
            highlightthickness=0,
            padx=0,  # Sin espacio horizontal adicional
            pady=0,   
            bordercolor = "#FFFFFF"
        )
        self.style.map(
            "Modern.TButton",
            background=[("active", "#45A049")],  # Color más oscuro al pulsar
        )

         # Estilo general para menuButton
        self.style.configure(
            "ModernMenu.TButton",
            font=("Helvetica", 14, "bold"),
            padding=10,
            relief="raised", 
            borderwidth=0, 
            highlightthickness=0
        )
        self.style.map(
            "ModernMenu.TButton",
            background=[("active", "#45A049")],  # Color más oscuro al pulsar
        )

        # Estilo general para labels
        self.style.configure(
            "Modern.TLabel",
            font=("Helvetica", 12),
            background="#FFFFFF"
        )

        # Estilo general para label de porciento
        self.style.configure(
            "ModernPercent.TLabel",
            font=("Helvetica", 10),
            background="#FFFFFF"
        )

        # Estilo general para frames
        self.style.configure(
            "Modern.TFrame",
            background="#FFFFFF",
            borderwidth=0,
        )

        # Estilo general para frames
        self.style.configure(
            "Modern.TSeparator",
            background="#FFFFFF",
            pading = 10
        )

        # Estilo para entradas (Entry)
        self.style.configure(
            "Modern.TEntry",
            padding=10,
            font=("Helvetica", 20),
            fieldbackground="#FFFFFF",
            bordercolor="#CCCCCC",
        )

        # Estilo para barra de progreso
        self.style.configure(
            "Modern.Horizontal.TProgressbar",
            thickness=10,
            background="#4CAF50",
            troughcolor="#D3D3D3",
            bordercolor="#CCCCCC",
        )
