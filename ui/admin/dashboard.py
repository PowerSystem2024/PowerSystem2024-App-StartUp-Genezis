import tkinter as tk # Importa la librería principal de Tkinter.
from tkinter import ttk
from controllers.admin_controller import AdminController # Importa el controlador de la lógica de negocio administrativa.

# Define la clase AdminDashboard que hereda de tk.Frame para crear el panel.
class AdminDashboard(tk.Frame):
    def __init__(self, parent, user_data):
        super().__init__(parent) # Llama al constructor de la clase base.
        self.parent = parent # Guarda referencia al widget padre.
        self.user_data = user_data # Guarda los datos del usuario logueado.
        self.controller = AdminController() # Instancia del controlador para la lógica.

        self.setup_ui() # Configura la interfaz de usuario.

    # Configura los elementos visuales del dashboard.
    def setup_ui(self):
        # Encabezado del panel con el nombre del usuario.
        header = tk.Label(self, text=f"Panel de Administrador - {self.user_data['nombre']}", font=("Arial", 16, "bold"))
        header.pack(pady=10)

        # Contenedor principal para la estructura de sidebar y contenido.
        container = tk.Frame(self)
        container.pack(fill=tk.BOTH, expand=True)

        # Panel de navegación lateral con botones.
        sidebar = tk.Frame(container, width=200, bg="#f0f0f0")
        sidebar.pack(side=tk.LEFT, fill=tk.Y)

        btn_usuarios = tk.Button(sidebar, text="Gestionar Usuarios", command=self.show_users_panel)
        btn_usuarios.pack(fill=tk.X, padx=10, pady=5)

        btn_reportes = tk.Button(sidebar, text="Reportes y Estadísticas", command=self.show_reports_panel)
        btn_reportes.pack(fill=tk.X, padx=10, pady=5)

        btn_config = tk.Button(sidebar, text="Configuración del Sistema", command=self.show_settings_panel)
        btn_config.pack(fill=tk.X, padx=10, pady=5)

        # Área de contenido dinámico donde se cargan las vistas.
        self.content_frame = tk.Frame(container, bg="white")
        self.content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Carga la vista de bienvenida al inicio.
        self.show_welcome()

    # Limpia todos los widgets del área de contenido.
    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    # Muestra el mensaje de bienvenida.
    def show_welcome(self):
        self.clear_content()
        label = tk.Label(self.content_frame, text="Bienvenido al Panel de Administración", font=("Arial", 14))
        label.pack(pady=50)

    # Muestra el panel de gestión de usuarios.
    def show_users_panel(self):
        from ui.admin.users import UsersFrame # Importación perezosa.
        self.clear_content()
        frame = UsersFrame(self.content_frame, self.controller)
        frame.pack(fill=tk.BOTH, expand=True)

    # Muestra el panel de reportes y estadísticas.
    def show_reports_panel(self):
        from ui.admin.reports import ReportsFrame # Importación perezosa.
        self.clear_content()
        frame = ReportsFrame(self.content_frame, self.controller)
        frame.pack(fill=tk.BOTH, expand=True)

    # Muestra un panel de configuración (placeholder).
    def show_settings_panel(self):
        self.clear_content()
        label = tk.Label(self.content_frame, text="Configuración del Sistema (no se que poner acá aun)", font=("Arial", 12))
        label.pack(pady=20)