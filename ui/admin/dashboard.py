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
        self.menu_buttons = {}

        self.setup_ui()

    def setup_ui(self):
        """Configura la interfaz principal"""
        self._create_header()
        self._create_main_container()
        self._create_sidebar()
        self._create_content_area()
        self.show_users_panel()

    def _create_header(self):
        """Crea el encabezado simplificado"""
        header = tk.Frame(self, bg="#2c3e50", height=50)
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        tk.Label(header, text=f"🛠️ Panel de Administrador - {self.user_data['nombre']}",
                 font=("Arial", 14, "bold"), fg="white", bg="#2c3e50").pack(pady=12)

    def _create_main_container(self):
        """Crea el contenedor principal"""
        self.main_container = tk.Frame(self, bg="#f8f9fa")
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def _create_sidebar(self):
        """Crea la barra lateral con menú"""
        sidebar = tk.Frame(self.main_container, width=180, bg="#ffffff", relief="solid", bd=1)
        sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 5))
        sidebar.pack_propagate(False)

        # Botones del menú
        menu_items = [
            ("👥 Usuarios", self.show_users_panel, "#3498db"),
            ("📊 Reportes", self.show_reports_panel, "#27ae60"),
            ("🚪 Cerrar Sesión", self.logout, "#e74c3c")
        ]

        for text, command, color in menu_items:
            btn = self._create_menu_button(sidebar, text, command, color)
            self.menu_buttons[text] = btn

        # Activar usuarios por defecto
        self._set_active_button("👥 Usuarios")

    def _create_menu_button(self, parent, text, command, color):
        """Crea un botón del menú optimizado"""

        def on_click():
            if text != "🚪 Cerrar Sesión":
                self._reset_buttons()
                btn.configure(bg=color, fg="white")
            command()

        btn = tk.Button(parent, text=text, command=on_click,
                        font=("Arial", 10, "bold"), fg="#2c3e50", bg="#ecf0f1",
                        relief="flat", bd=0, pady=10)
        btn.pack(fill=tk.X, padx=8, pady=2)
        btn.color = color
        return btn

    def _set_active_button(self, button_text):
        """Marca un botón como activo"""
        if button_text in self.menu_buttons:
            btn = self.menu_buttons[button_text]
            btn.configure(bg=btn.color, fg="white")

    def _reset_buttons(self):
        """Resetea el estado visual de los botones del menú"""
        for text, btn in self.menu_buttons.items():
            if text != "🚪 Cerrar Sesión":
                btn.configure(bg="#ecf0f1", fg="#2c3e50")

    def _create_content_area(self):
        """Crea el área de contenido con scroll"""
        content_container = tk.Frame(self.main_container, bg="white", relief="solid", bd=1)
        content_container.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Canvas y scrollbar
        self.canvas = tk.Canvas(content_container, bg="white", highlightthickness=0)
        scrollbar = ttk.Scrollbar(content_container, orient="vertical", command=self.canvas.yview)
        self.content_frame = tk.Frame(self.canvas, bg="white")

        # Configuración del scroll
        self.content_frame.bind("<Configure>",
                                lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.canvas.create_window((0, 0), window=self.content_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        # Pack elementos
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Scroll con mouse
        self.canvas.bind('<MouseWheel>',
                         lambda e: self.canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"))

    def clear_content(self):
        """Limpia el área de contenido"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def show_users_panel(self):
        """Muestra el panel de usuarios"""
        from ui.admin.users import UsersFrame
        self.clear_content()
        self._create_section_header("👥 Gestión de Usuarios")

        frame = UsersFrame(self.content_frame, self.controller)
        frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

    def show_reports_panel(self):
        """Muestra el panel de reportes"""
        from ui.admin.reports import ReportsFrame
        self.clear_content()
        self._create_section_header("📊 Reportes y Estadísticas")

        frame = ReportsFrame(self.content_frame, self.controller)
        frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

    def _create_section_header(self, section_title):
        """Crea el encabezado de sección simplificado"""
        tk.Label(self.content_frame, text=section_title,
                 font=("Arial", 16, "bold"), fg="#2c3e50", bg="white").pack(pady=(15, 10))


        tk.Frame(self.content_frame, height=2, bg="#3498db").pack(fill=tk.X, padx=15, pady=(0, 10))

    def logout(self):
        """Cierra la sesión del usuario"""
        self.parent.logout()