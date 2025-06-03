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

    def setup_ui(self):
        # Encabezado con el nombre del usuario
        header = tk.Label(self, text=f"Panel de Administrador - {self.user_data['nombre']}", font=("Arial", 16, "bold"))
        header.pack(pady=10)

        # Contenedor principal
        container = tk.Frame(self)
        container.pack(fill=tk.BOTH, expand=True)

        # Sidebar con botones
        sidebar = tk.Frame(container, width=200, bg="#f0f0f0")
        sidebar.pack(side=tk.LEFT, fill=tk.Y)

        btn_usuarios = tk.Button(sidebar, text="Gestionar Usuarios", command=self.show_users_panel)
        btn_usuarios.pack(fill=tk.X, padx=10, pady=5)

        btn_reportes = tk.Button(sidebar, text="Reportes y Estadísticas", command=self.show_reports_panel)
        btn_reportes.pack(fill=tk.X, padx=10, pady=5)

        # Botón para cerrar sesión
        btn_logout = tk.Button(sidebar, text="Cerrar sesión", fg="white", bg="#d9534f", command=self.logout)
        btn_logout.pack(fill=tk.X, padx=10, pady=5)

        # Área de contenido
        self.content_frame = tk.Frame(container, bg="white")
        self.content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Vista de bienvenida inicial
        self.show_welcome()

    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def show_welcome(self):
        self.clear_content()
        label = tk.Label(self.content_frame, text="Bienvenido al Panel de Administración", font=("Arial", 14))
        label.pack(pady=50)

    def show_users_panel(self):
        from ui.admin.users import UsersFrame
        self.clear_content()
        frame = UsersFrame(self.content_frame, self.controller)
        frame.pack(fill=tk.BOTH, expand=True)

    def show_reports_panel(self):
        from ui.admin.reports import ReportsFrame
        self.clear_content()
        frame = ReportsFrame(self.content_frame, self.controller)
        frame.pack(fill=tk.BOTH, expand=True)

    def logout(self):
        self.parent.logout()  # Esto llama al método logout de la clase App