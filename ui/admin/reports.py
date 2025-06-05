# ui/admin/reports.py - Versión corregida y simplificada

import tkinter as tk
from tkinter import ttk


class ReportsFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.setup_ui()

    # ===========================================
    # CONFIGURACIÓN DE LA INTERFAZ
    # ===========================================

    def setup_ui(self):
        """Configura la interfaz de usuario"""
        self._create_title()
        self._create_stats_cards()
        self._create_summary_table()

    def _create_title(self):
        """Crea el título principal"""
        title_frame = tk.Frame(self, bg='white')
        title_frame.pack(fill=tk.X, pady=(0, 20))

        tk.Label(title_frame,
                 text="📊 Reportes y Estadísticas",
                 font=("Arial", 14, "bold"),
                 fg="#2c3e50",
                 bg='white').pack(pady=15)

    def _create_stats_cards(self):
        """Crea las tarjetas de estadísticas principales"""
        cards_frame = tk.Frame(self, bg='white')
        cards_frame.pack(fill=tk.X, pady=(0, 20), padx=20)

        # Obtener estadísticas corregidas
        stats = self._get_corrected_stats()

        # Configurar tarjetas
        cards_config = [
            ("👥", "Usuarios Totales", stats["usuarios_totales"], "#3498db"),
            ("👨‍⚕️", "Médicos", stats["medicos"], "#27ae60"),
            ("🤒", "Pacientes", stats["pacientes"], "#e74c3c"),
            ("🏥", "Instituciones", stats["instituciones"], "#f39c12"),
            ("👨‍💼", "Administradores", stats["admins"], "#9b59b6")
        ]

        # Crear grid de tarjetas (3 columnas)
        for i, (icon, title, value, color) in enumerate(cards_config):
            row = i // 3
            col = i % 3
            self._create_stat_card(cards_frame, icon, title, value, color, row, col)

    def _create_stat_card(self, parent, icon, title, value, color, row, col):
        """Crea una tarjeta individual de estadística"""
        card = tk.Frame(parent, bg=color, relief='flat', bd=1)
        card.grid(row=row, column=col, padx=10, pady=10, sticky='ew', ipadx=15, ipady=10)

        # Configurar expansión de columnas
        parent.grid_columnconfigure(col, weight=1)

        # Contenido de la tarjeta
        tk.Label(card, text=icon, font=("Arial", 20), fg='white', bg=color).pack()
        tk.Label(card, text=str(value), font=("Arial", 16, "bold"), fg='white', bg=color).pack()
        tk.Label(card, text=title, font=("Arial", 10), fg='white', bg=color).pack()

    def _create_summary_table(self):
        """Crea la tabla resumen"""
        # Frame contenedor
        table_frame = tk.LabelFrame(self,
                                    text="📋 Resumen por Tipo de Usuario",
                                    font=("Arial", 12, "bold"),
                                    fg="#2c3e50",
                                    bg='white')
        table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Crear tabla
        columns = ("tipo", "cantidad", "porcentaje")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=6)

        # Configurar columnas
        self.tree.heading("tipo", text="Tipo de Usuario")
        self.tree.heading("cantidad", text="Cantidad")
        self.tree.heading("porcentaje", text="Porcentaje")

        self.tree.column("tipo", width=200, anchor='w')
        self.tree.column("cantidad", width=100, anchor='center')
        self.tree.column("porcentaje", width=120, anchor='center')

        # Llenar tabla
        self._populate_summary_table()

        # Empaquetar tabla
        self.tree.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        # Crear análisis rápido
        self._create_quick_analysis(table_frame)

    # ===========================================
    #  MANEJO DE DATOS
    # ===========================================

    def _get_corrected_stats(self):
        """Obtiene estadísticas correctas contando por tipo de usuario"""
        result = self.controller.get_all_users()

        if not result or not result.data:
            return {
                "usuarios_totales": 0,
                "medicos": 0,
                "pacientes": 0,
                "instituciones": 0,
                "admins": 0
            }

        # Contar por tipo de usuario
        usuarios = result.data
        tipos_count = {"medico": 0, "paciente": 0, "institucion": 0, "admin": 0}

        for usuario in usuarios:
            tipo = usuario.get("tipo", "").lower()
            if tipo in tipos_count:
                tipos_count[tipo] += 1

        return {
            "usuarios_totales": len(usuarios),
            "medicos": tipos_count["medico"],
            "pacientes": tipos_count["paciente"],
            "instituciones": tipos_count["institucion"],
            "admins": tipos_count["admin"]
        }

    def _populate_summary_table(self):
        """Llena la tabla con datos estadísticos"""
        stats = self._get_corrected_stats()
        total = stats["usuarios_totales"]

        # Limpiar tabla
        self.tree.delete(*self.tree.get_children())

        # Datos para la tabla
        data = [
            ("👨‍⚕️ Médicos", stats["medicos"]),
            ("🤒 Pacientes", stats["pacientes"]),
            ("🏥 Instituciones", stats["instituciones"]),
            ("👨‍💼 Administradores", stats["admins"])
        ]

        # Insertar filas
        for tipo, cantidad in data:
            porcentaje = f"{(cantidad / total * 100):.1f}%" if total > 0 else "0%"
            self.tree.insert("", "end", values=(tipo, cantidad, porcentaje))

    def _create_quick_analysis(self, parent):
        """Crea una sección de análisis rápido"""
        analysis_frame = tk.Frame(parent, bg='#f8f9fa', relief='solid', bd=1)
        analysis_frame.pack(fill=tk.X, padx=15, pady=(0, 15))

        # Título
        tk.Label(analysis_frame,
                 text="🔍 Análisis Rápido",
                 font=("Arial", 11, "bold"),
                 fg="#2c3e50",
                 bg='#f8f9fa').pack(anchor='w', padx=15, pady=(10, 5))

        # Generar y mostrar análisis
        analysis_points = self._generate_quick_analysis()

        for point in analysis_points:
            tk.Label(analysis_frame,
                     text=f"• {point}",
                     font=("Arial", 9),
                     fg="#2c3e50",
                     bg='#f8f9fa',
                     anchor='w',
                     justify='left').pack(fill=tk.X, padx=15, pady=1)

        # Espaciado inferior
        tk.Label(analysis_frame, text="", bg='#f8f9fa').pack(pady=5)

    # ===========================================
    # BLOQUE 3: ANÁLISIS DE DATOS
    # ===========================================

    def _generate_quick_analysis(self):
        """Genera puntos de análisis rápido"""
        stats = self._get_corrected_stats()
        analysis = []

        total = stats["usuarios_totales"]
        medicos = stats["medicos"]
        pacientes = stats["pacientes"]
        instituciones = stats["instituciones"]
        admins = stats["admins"]

        # Análisis general del sistema
        if total == 0:
            analysis.append("Sistema sin usuarios registrados")
        elif total < 10:
            analysis.append("Sistema en fase inicial (menos de 10 usuarios)")
        else:
            analysis.append(f"Sistema activo con {total} usuarios registrados")

        # Análisis de distribución
        if medicos > 0 and pacientes > 0:
            ratio = round(pacientes / medicos, 1)
            if ratio < 5:
                analysis.append(f"Ratio pacientes/médicos: {ratio}:1 (Excelente cobertura)")
            elif ratio < 15:
                analysis.append(f"Ratio pacientes/médicos: {ratio}:1 (Buena cobertura)")
            else:
                analysis.append(f"Ratio pacientes/médicos: {ratio}:1 (Considerar más médicos)")
        elif medicos == 0 and pacientes > 0:
            analysis.append("Hay pacientes registrados pero no médicos")
        elif medicos > 0 and pacientes == 0:
            analysis.append("Hay médicos registrados pero no pacientes")

        # Análisis de instituciones
        if instituciones > 0 and medicos > 0:
            med_por_inst = round(medicos / instituciones, 1)
            analysis.append(f"Promedio de {med_por_inst} médicos por institución")
        elif instituciones == 0 and medicos > 0:
            analysis.append("Médicos registrados sin instituciones asociadas")

        # Análisis de administración
        if admins == 0:
            analysis.append("⚠️ No hay administradores además del actual")
        elif admins == 1:
            analysis.append("Sistema con un solo administrador")

        # Si no hay suficientes datos
        if len(analysis) == 0:
            analysis.append("Datos insuficientes para análisis")

        return analysis[:5]  # Máximo 5 puntos

    # ===========================================
    #  FUNCIONES AUXILIARES
    # ===========================================

    def refresh_data(self):
        """Refresca todos los datos mostrados"""
        for widget in self.winfo_children():
            widget.destroy()
        self.setup_ui()