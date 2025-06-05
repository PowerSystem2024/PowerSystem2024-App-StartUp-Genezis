# ui/admin/dashboard.py

import tkinter as tk
from tkinter import ttk
from controllers.admin_controller import AdminController


class AdminDashboard(tk.Frame):
    def __init__(self, parent, user_data):
        super().__init__(parent)
        self.parent = parent
        self.user_data = user_data
        self.controller = AdminController()

        self.setup_ui()

    # ===========================================
    #  INTERFAZ
    # ===========================================

    def setup_ui(self):
        """Configura la interfaz principal"""
        self._create_header()
        self._create_main_container()
        self._create_sidebar()
        self._create_content_area()
        self.show_users_panel()  # Mostrar usuarios por defecto

    def _create_header(self):
        """Crea el encabezado"""
        header = tk.Frame(self, bg="#2c3e50", height=60)
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        # Título
        tk.Label(header,
                 text=f"🛠️ Panel de Administrador",
                 font=("Arial", 16, "bold"),
                 fg="white", bg="#2c3e50").pack(pady=10)

        # Subtítulo
        tk.Label(header,
                 text=f"Bienvenido, {self.user_data['nombre']}",
                 font=("Arial", 10),
                 fg="#ecf0f1", bg="#2c3e50").pack()

    def _create_main_container(self):
        """Crea el contenedor principal"""
        self.main_container = tk.Frame(self, bg="#ecf0f1")
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def _create_sidebar(self):
        """Crea la barra lateral con menú"""
        sidebar = tk.Frame(self.main_container, width=200, bg="#f8f9fa", relief="solid", bd=1)
        sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        sidebar.pack_propagate(False)

        # Título del menú
        tk.Label(sidebar, text="📋 Menú", font=("Arial", 12, "bold"),
                 bg="#f8f9fa").pack(pady=15)

        # Botones del menú (sin botón inicio)
        self.users_btn = self._create_menu_button(sidebar, "👥 Usuarios", self.show_users_panel, "#3498db")
        self.reports_btn = self._create_menu_button(sidebar, "📊 Reportes", self.show_reports_panel, "#27ae60")

        # Marcar usuarios como activo por defecto
        self._set_active_button(self.users_btn)

        # Espaciador
        tk.Frame(sidebar, bg="#f8f9fa").pack(expand=True, fill=tk.BOTH)

        # Botón cerrar sesión
        self._create_menu_button(sidebar, "🚪 Cerrar Sesión", self.logout, "#e74c3c")

    def _create_menu_button(self, parent, text, command, color):
        """Crea un botón del menú"""

        def button_command():
            # Resetear todos los botones
            self._reset_buttons()
            # Activar el botón actual
            btn.configure(bg=color, relief="flat")
            # Ejecutar comando
            command()

        btn = tk.Button(parent, text=text, command=button_command,
                        font=("Arial", 10, "bold"), fg="white", bg="#bdc3c7",
                        relief="flat", bd=0, padx=10, pady=8)
        btn.pack(fill=tk.X, padx=10, pady=3)
        btn.original_color = color
        return btn

    def _set_active_button(self, active_btn):
        """Marca un botón como activo"""
        active_btn.configure(bg=active_btn.original_color)

    def _reset_buttons(self):
        """Resetea el estado visual de todos los botones del menú"""
        if hasattr(self, 'users_btn'):
            self.users_btn.configure(bg="#bdc3c7")
        if hasattr(self, 'reports_btn'):
            self.reports_btn.configure(bg="#bdc3c7")

    def _create_content_area(self):
        """Crea el área de contenido con scroll"""
        content_container = tk.Frame(self.main_container, bg="white", relief="solid", bd=1)
        content_container.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Canvas para scroll
        self.canvas = tk.Canvas(content_container, bg="white")
        self.scrollbar = ttk.Scrollbar(content_container, orient="vertical", command=self.canvas.yview)
        self.content_frame = tk.Frame(self.canvas, bg="white")

        # Configurar scroll
        self.content_frame.bind("<Configure>",
                                lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.canvas.create_window((0, 0), window=self.content_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Scroll con rueda del mouse
        self.canvas.bind('<MouseWheel>', lambda e: self.canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"))

    # ===========================================
    #  GESTIÓN DE CONTENIDO
    # ===========================================

    def clear_content(self):
        """Limpia el área de contenido"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    # ===========================================
    #  NAVEGACIÓN ENTRE PANTALLAS
    # ===========================================

    def show_users_panel(self):
        """Muestra el panel de usuarios"""
        from ui.admin.users import UsersFrame
        self.clear_content()

        # Título de la sección
        self._create_section_header("👥 Gestión de Usuarios")

        # Cargar panel de usuarios
        frame = UsersFrame(self.content_frame, self.controller)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def show_reports_panel(self):
        """Muestra el panel de reportes"""
        from ui.admin.reports import ReportsFrame
        self.clear_content()

        # Título de la sección
        self._create_section_header("📊 Reportes y Estadísticas")

        # Cargar panel de reportes
        frame = ReportsFrame(self.content_frame, self.controller)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def _create_section_header(self, section_title):
        """Crea el encabezado de una sección"""
        header_frame = tk.Frame(self.content_frame, bg="white")
        header_frame.pack(fill=tk.X, padx=10, pady=10)

        # Título de la sección
        tk.Label(header_frame, text=section_title,
                 font=("Arial", 14, "bold"), fg="#2c3e50", bg="white").pack(side=tk.LEFT)

        # Línea separadora
        separator = tk.Frame(self.content_frame, height=1, bg="#ecf0f1")
        separator.pack(fill=tk.X, padx=10, pady=5)

    # ===========================================
    # FUNCIONES DEL SISTEMA
    # ===========================================

    def logout(self):
        """Cierra la sesión del usuario"""
        self.parent.logout()