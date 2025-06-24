# ui/admin/reports.py

import tkinter as tk
from tkinter import ttk


class ReportsFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.setup_ui()

    def setup_ui(self):
        # Título
        tk.Label(self, text="Reportes y Estadísticas",
                 font=("Arial", 14, "bold")).pack(pady=10)

        # Estadísticas principales
        self._create_stats_section()

        # Tabla resumen
        self._create_summary_table()

    def _create_stats_section(self):
        stats_frame = tk.LabelFrame(self, text="Estadísticas", font=("Arial", 10, "bold"))
        stats_frame.pack(fill=tk.X, padx=20, pady=10)

        stats = self._get_stats()

        # Grid de estadísticas (2 columnas)
        stats_data = [
            ("Usuarios Totales", stats["usuarios_totales"]),
            ("Médicos", stats["medicos"]),
            ("Pacientes", stats["pacientes"]),
            ("Instituciones", stats["instituciones"]),
            ("Administradores", stats["admins"])
        ]

        for i, (label, value) in enumerate(stats_data):
            row, col = divmod(i, 2)

            item_frame = tk.Frame(stats_frame)
            item_frame.grid(row=row, column=col, padx=10, pady=5, sticky="w")

            tk.Label(item_frame, text=f"{label}:", font=("Arial", 9)).pack(side=tk.LEFT)
            tk.Label(item_frame, text=str(value), font=("Arial", 9, "bold")).pack(side=tk.LEFT, padx=(5, 0))

        # Configurar expansión de columnas
        stats_frame.grid_columnconfigure(0, weight=1)
        stats_frame.grid_columnconfigure(1, weight=1)

    def _create_summary_table(self):
        table_frame = tk.LabelFrame(self, text="Resumen por Tipo", font=("Arial", 10, "bold"))
        table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Tabla
        columns = ("tipo", "cantidad", "porcentaje")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=5)

        for col, text, width in [("tipo", "Tipo", 150), ("cantidad", "Cantidad", 80), ("porcentaje", "Porcentaje", 80)]:
            self.tree.heading(col, text=text)
            self.tree.column(col, width=width, anchor='center' if col != 'tipo' else 'w')

        self._fill_table()
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Análisis simple
        self._create_analysis(table_frame)

    def _fill_table(self):
        stats = self._get_stats()
        total = stats["usuarios_totales"]

        self.tree.delete(*self.tree.get_children())

        table_data = [
            ("Médicos", stats["medicos"]),
            ("Pacientes", stats["pacientes"]),
            ("Instituciones", stats["instituciones"]),
            ("Administradores", stats["admins"])
        ]

        for tipo, cantidad in table_data:
            porcentaje = f"{(cantidad / total * 100):.1f}%" if total > 0 else "0%"
            self.tree.insert("", "end", values=(tipo, cantidad, porcentaje))

    def _create_analysis(self, parent):
        analysis_frame = tk.Frame(parent, relief='solid', bd=1, bg='#f5f5f5')
        analysis_frame.pack(fill=tk.X, padx=10, pady=(0, 10))

        tk.Label(analysis_frame, text="Análisis:", font=("Arial", 9, "bold"),
                 bg='#f5f5f5').pack(anchor='w', padx=10, pady=(5, 0))

        analysis_points = self._generate_analysis()
        for point in analysis_points:
            tk.Label(analysis_frame, text=f"• {point}", font=("Arial", 8),
                     bg='#f5f5f5', anchor='w').pack(fill=tk.X, padx=15, pady=1)

        tk.Frame(analysis_frame, height=5, bg='#f5f5f5').pack()

    def _get_stats(self):
        # Usar el método de estadísticas optimizado del controlador
        stats = self.controller.obtener_estadisticas_sistema()

        if not stats:
            return {"usuarios_totales": 0, "medicos": 0, "pacientes": 0, "instituciones": 0, "admins": 0}

        # Adaptamos las estadísticas al formato esperado por la UI
        return {
            "usuarios_totales": stats.get("usuarios_totales", 0),
            "medicos": stats.get("medicos_totales", 0),
            "pacientes": stats.get("pacientes_totales", 0),
            "instituciones": stats.get("instituciones_totales", 0),
            "admins": stats.get("admins_totales", 0)  # Ahora sí tenemos conteo específico de admins
        }

    def _generate_analysis(self):
        stats = self._get_stats()
        analysis = []

        total = stats["usuarios_totales"]
        medicos = stats["medicos"]
        pacientes = stats["pacientes"]
        instituciones = stats["instituciones"]

        # Análisis básico
        if total == 0:
            return ["Sistema sin usuarios registrados"]

        if total < 10:
            analysis.append(f"Sistema inicial ({total} usuarios)")
        else:
            analysis.append(f"Sistema activo ({total} usuarios)")

        # Ratio médicos-pacientes
        if medicos > 0 and pacientes > 0:
            ratio = round(pacientes / medicos, 1)
            if ratio < 10:
                analysis.append(f"Ratio P/M: {ratio}:1 (Buena cobertura)")
            else:
                analysis.append(f"Ratio P/M: {ratio}:1 (Considerar más médicos)")
        elif pacientes > 0 and medicos == 0:
            analysis.append("Pacientes sin médicos disponibles")

        # Instituciones
        if instituciones > 0 and medicos > 0:
            med_por_inst = round(medicos / instituciones, 1)
            analysis.append(f"Promedio: {med_por_inst} médicos/institución")

        return analysis[:3]  # Máximo 3 puntos

    def refresh_data(self):
        """Actualiza los datos de la interfaz sin reconstruir toda la UI"""
        # Obtenemos las estadísticas actualizadas
        stats = self._get_stats()

        # Actualizamos la sección de estadísticas
        for widget in self.winfo_children():
            if isinstance(widget, tk.LabelFrame) and widget.cget("text") == "Estadísticas":
                for child in widget.winfo_children():
                    if isinstance(child, tk.Frame):
                        for label in child.winfo_children():
                            if isinstance(label, tk.Label) and label.cget("font") == ("Arial", 9, "bold"):
                                # Encontramos una etiqueta de valor
                                label_text = label.cget("text")
                                for key, value in stats.items():
                                    if key in label_text.lower():
                                        label.config(text=str(value))
                                        break

        # Actualizamos la tabla
        self._fill_table()

        # Actualizamos el análisis
        for widget in self.winfo_children():
            if isinstance(widget, tk.LabelFrame) and widget.cget("text") == "Resumen por Tipo":
                for child in widget.winfo_children():
                    if isinstance(child, tk.Frame) and child.cget("relief") == "solid":
                        for label in child.winfo_children():
                            if isinstance(label, tk.Label) and "•" in label.cget("text"):
                                label.destroy()
                        analysis_points = self._generate_analysis()
                        for point in analysis_points:
                            tk.Label(child, text=f"• {point}", font=("Arial", 8),
                                     bg='#f5f5f5', anchor='w').pack(fill=tk.X, padx=15, pady=1)