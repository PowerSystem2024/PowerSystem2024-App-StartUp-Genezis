import tkinter as tk
from tkinter import ttk

# Define la clase ReportsFrame, que hereda de tk.Frame para ser un contenedor de la UI de reportes.
class ReportsFrame(tk.Frame):
    # El constructor inicializa el frame de reportes.
    def __init__(self, parent, controller):
        super().__init__(parent)  # Llama al constructor de la clase base (tk.Frame).
        self.controller = controller  # Guarda una referencia al controlador (AdminController) para acceder a los datos.
        self.setup_ui()  # Configura los elementos visuales del reporte.

    # Configura la interfaz de usuario para mostrar los reportes y estadísticas.
    def setup_ui(self):
        # Crea y empaqueta un título para el panel de reportes.
        title = tk.Label(self, text="Reportes y Estadísticas", font=("Arial", 14, "bold"))
        title.pack(pady=10)

        # Obtiene las estadísticas del sistema a través del controlador.
        stats = self.controller.get_system_stats()
        if not stats:  # Si no se pueden cargar las estadísticas, muestra un mensaje de error.
            tk.Label(self, text="No se pudieron cargar las estadísticas.").pack()
            return

        # Crea un frame para contener las estadísticas y lo empaqueta.
        stats_frame = tk.Frame(self)
        stats_frame.pack(padx=20, pady=20)

        # Llama a create_stat_label para mostrar cada estadística individualmente.
        self.create_stat_label(stats_frame, "Usuarios totales", stats["usuarios_totales"], 0)
        self.create_stat_label(stats_frame, "Instituciones totales", stats["instituciones_totales"], 1)
        self.create_stat_label(stats_frame, "Médicos totales", stats["medicos_totales"], 2)
        self.create_stat_label(stats_frame, "Pacientes totales", stats["pacientes_totales"], 3)
        self.create_stat_label(stats_frame, "Turnos totales", stats["turnos_totales"], 4)

    # Función auxiliar para crear y posicionar etiquetas de estadísticas.
    def create_stat_label(self, parent, label_text, value, row):
        # Crea una etiqueta para el nombre de la estadística.
        label = tk.Label(parent, text=f"{label_text}:", font=("Arial", 12))
        label.grid(row=row, column=0, sticky="w", pady=5, padx=10) # Posiciona la etiqueta en una cuadrícula.

        # Crea una etiqueta para el valor de la estadística.
        value_label = tk.Label(parent, text=str(value), font=("Arial", 12, "bold"))
        value_label.grid(row=row, column=1, sticky="w", pady=5) # Posiciona el valor junto al nombre.