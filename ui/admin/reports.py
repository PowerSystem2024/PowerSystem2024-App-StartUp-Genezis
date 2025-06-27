import tkinter as tk
from tkinter import ttk

# Importaciones necesarias para el gráfico
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class ReportsFrame(tk.Frame):
    """
    Frame que muestra estadísticas, una tabla y un gráfico de barras responsivo
    con un layout vertical.
    """

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.chart_canvas = None
        self.chart_figure = None

        self.setup_ui()

    def setup_ui(self):
        """
        Construye la interfaz con un layout vertical:
        1. Título
        2. Sección superior (Estadísticas y Tabla)
        3. Sección inferior (Gráfico)
        """
        # 1. Título principal
        tk.Label(self, text="Reportes y Estadísticas",
                 font=("Arial", 14, "bold")).pack(pady=10, fill=tk.X)

        # --- INICIO DE LA REESTRUCTURACIÓN DEL LAYOUT ---

        # 2. Frame para la sección superior (estadísticas y tabla)
        top_frame = tk.Frame(self)
        # Usamos fill=tk.X para que ocupe todo el ancho, pero no se expanda verticalmente
        top_frame.pack(fill=tk.X, expand=False, padx=20, pady=(0, 10))

        # 3. Frame para la sección inferior (el gráfico)
        # Este sí se expandirá para ocupar el espacio restante
        chart_container_frame = tk.Frame(self)
        chart_container_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 10))

        # Vinculamos el evento de redimensionamiento al contenedor del gráfico
        chart_container_frame.bind("<Configure>", self._on_chart_resize)

        # --- FIN DE LA REESTRUCTURACIÓN ---

        # Ahora poblamos los frames que acabamos de crear
        self._create_stats_and_table_section(top_frame)
        self._create_bar_chart(chart_container_frame)

    def _create_stats_and_table_section(self, parent):
        """
        Crea un contenedor para las estadísticas y la tabla, uno al lado del otro.
        Este método ahora organiza la parte superior de la UI.
        """
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_columnconfigure(1, weight=1)

        stats_frame = tk.LabelFrame(parent, text="Estadísticas Clave", font=("Arial", 10, "bold"))
        stats_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 5))

        table_frame = tk.LabelFrame(parent, text="Resumen por Tipo", font=("Arial", 10, "bold"))
        table_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 0))

        # Lógica para poblar las estadísticas
        stats = self._get_stats()
        stats_data = [("Usuarios Totales", stats["usuarios_totales"]), ("Médicos", stats["medicos"]),
                      ("Pacientes", stats["pacientes"]), ("Instituciones", stats["instituciones"]),
                      ("Administradores", stats["admins"])]
        for i, (label, value) in enumerate(stats_data):
            row, col = divmod(i, 2)
            item_frame = tk.Frame(stats_frame);
            item_frame.grid(row=row, column=col, padx=10, pady=5, sticky="w")
            tk.Label(item_frame, text=f"{label}:", font=("Arial", 9)).pack(side=tk.LEFT)
            tk.Label(item_frame, text=str(value), font=("Arial", 9, "bold")).pack(side=tk.LEFT, padx=(5, 0))
        stats_frame.grid_columnconfigure(0, weight=1);
        stats_frame.grid_columnconfigure(1, weight=1)

        # Lógica para poblar la tabla
        columns = ("tipo", "cantidad", "porcentaje");
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=5)
        column_defs = [("tipo", "Tipo", 90), ("cantidad", "Cant.", 50), ("porcentaje", "%", 50)]
        for col, text, width in column_defs:
            self.tree.heading(col, text=text);
            self.tree.column(col, width=width, anchor='center' if col != 'tipo' else 'w')
        self._fill_table();
        self.tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def _on_chart_resize(self, event):
        """Gestiona el redimensionamiento del gráfico."""
        if not self.chart_canvas or not hasattr(event, 'width') or event.width < 50 or event.height < 50:
            return

        new_width = event.width / self.chart_figure.dpi
        new_height = event.height / self.chart_figure.dpi

        self.chart_figure.set_size_inches(new_width, new_height, forward=True)
        # Ajustamos el layout para evitar que las etiquetas se corten con el nuevo tamaño
        self.chart_figure.tight_layout()
        self.chart_canvas.draw_idle()

    def _create_bar_chart(self, parent):
        """Crea el gráfico de barras para que ocupe el frame padre."""
        # El LabelFrame ahora está dentro del método para mantenerlo autocontenido
        chart_labelframe = tk.LabelFrame(parent, text="Distribución de Usuarios", font=("Arial", 10, "bold"))
        chart_labelframe.pack(fill=tk.BOTH, expand=True)

        stats = self._get_stats()
        labels = ['Médicos', 'Pacientes', 'Instituciones', 'Admins']
        values = [stats.get("medicos", 0), stats.get("pacientes", 0), stats.get("instituciones", 0),
                  stats.get("admins", 0)]

        plt.style.use('seaborn-v0_8-pastel')
        self.chart_figure, ax = plt.subplots()

        bars = ax.bar(labels, values, color=['#66b3ff', '#ff9999', '#99ff99', '#ffcc99'])

        ax.set_ylabel('Cantidad de Usuarios')
        # Eliminamos el título del gráfico ya que el LabelFrame ya lo tiene
        # ax.set_title('Usuarios por Tipo')
        ax.bar_label(bars, padding=3)
        ax.get_yaxis().set_major_locator(plt.MaxNLocator(integer=True))
        self.chart_figure.tight_layout()

        self.chart_canvas = FigureCanvasTkAgg(self.chart_figure, master=chart_labelframe)
        self.chart_canvas.draw()
        self.chart_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=5)

    def refresh_data(self):
        """Actualiza todos los datos de la interfaz reconstruyéndola."""
        for widget in self.winfo_children():
            widget.destroy()
        self.setup_ui()

    def _fill_table(self):
        """Rellena la tabla con datos actualizados."""
        stats = self._get_stats();
        total = stats["usuarios_totales"];
        self.tree.delete(*self.tree.get_children())
        table_data = [("Médicos", stats["medicos"]), ("Pacientes", stats["pacientes"]),
                      ("Instituciones", stats["instituciones"]), ("Administradores", stats["admins"])]
        for tipo, cantidad in table_data:
            porcentaje = f"{(cantidad / total * 100):.1f}%" if total > 0 else "0%";
            self.tree.insert("", "end", values=(tipo, cantidad, porcentaje))

    def _get_stats(self):
        """Obtiene estadísticas del controlador."""
        stats = self.controller.obtener_estadisticas_sistema()
        if not stats: return {"usuarios_totales": 0, "medicos": 0, "pacientes": 0, "instituciones": 0, "admins": 0}
        return {"usuarios_totales": stats.get("usuarios_totales", 0), "medicos": stats.get("medicos_totales", 0),
                "pacientes": stats.get("pacientes_totales", 0), "instituciones": stats.get("instituciones_totales", 0),
                "admins": stats.get("admins_totales", 0)}