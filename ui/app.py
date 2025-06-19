import tkinter as tk
from tkinter import ttk, messagebox
from ui.loginInterface import LoginInterface
from ui.register import RegisterFrame

class App(tk.Tk):
    """Aplicación principal"""
    
    def __init__(self):
        super().__init__()
        
        # Configuración de la ventana principal
        self.title("Sistema de Turnos Médicos")

        # Establecer dimensiones de la ventana
        window_width = 895
        window_height = 587

        # Obtener dimensiones de la pantalla
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Calcular posición para centrar la ventana
        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_height / 2 - window_height / 2)

        # Establecer geometría, posición y que no se pueda redimensionar
        self.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        self.resizable(False, False)

        # Variables de estado
        self.current_user = None
        self.current_frame = None
        
        # Iniciar con pantalla de login
        self.show_login()
#---------------------------------------------------------------------------------------------------------


    def show_register(self):
        """Mostrar pantalla de registro"""
        if self.current_frame:
            self.current_frame.destroy()
        
        self.current_frame = RegisterFrame(self, self.on_register_success)
        self.current_frame.pack(fill=tk.BOTH, expand=True)
    
    def on_register_success(self):
        """Callback cuando el registro es exitoso"""
        messagebox.showinfo("Registro exitoso", "Usuario registrado correctamente. Por favor, inicie sesión.")
        self.show_login()


    def show_login(self):
        """Mostrar pantalla de login"""
        if self.current_frame:
            self.current_frame.destroy()
        
        self.current_frame = LoginInterface(self, self.on_login_success)
        self.current_frame.pack(fill=tk.BOTH, expand=True)
    
    def on_login_success(self, user):
        """Callback cuando el login es exitoso"""
        self.current_user = user
        
        # Mostrar el panel correspondiente según el tipo de usuario
        self.show_dashboard(user["tipo"])

    def show_dashboard(self, user_type):
        """Mostrar el dashboard según el tipo de usuario"""
        if self.current_frame:
            self.current_frame.destroy()
            self.current_frame = None  # Buena práctica para limpiar la referencia

        if user_type == "admin":
            from ui.admin.dashboard import AdminDashboard
            self.current_frame = AdminDashboard(self, self.current_user)

        elif user_type == "medico":
            # ====> LA SOLUCIÓN ESTÁ AQUÍ <====
            from ui.medicos.dashboard import MedicoDashboard
            from controllers.med_controller import obtener_medico_id_por_usuario_id  # 1. Importamos la función

            usuario_id = self.current_user["id"]

            # 2. Usamos la función para "traducir" el ID de usuario al ID de médico
            medico_id_real = obtener_medico_id_por_usuario_id(usuario_id)
            if medico_id_real:
                # 3. Si encontramos el ID, lo pasamos al dashboard. ¡Este es el ID correcto!
                self.current_frame = MedicoDashboard(self, medico_id_real)
            else:
                # 4. Si no, significa que algo anda mal (un usuario tipo 'medico' sin perfil de médico).
                #    Mostramos un error y no cargamos el dashboard.
                messagebox.showerror("Error de Perfil",
                                     "Este usuario no está registrado en ninguna institución, comunicarse con administración.")

                # Crear un pequeño frame con un botón "Volver al Inicio de Sesión"
                error_frame = tk.Frame(self)
                error_frame.pack(fill=tk.BOTH, expand=True)

                tk.Label(error_frame, text="Perfil inválido", font=("Arial", 14)).pack(pady=20)
                tk.Button(error_frame, text="Volver al Inicio de Sesión", font=("Arial", 12),
                          command=lambda: [error_frame.destroy(), self.show_login()]).pack(pady=10)

                # Limpiamos cualquier indicador de sesión para mayor seguridad
                self.current_user = None
                self.current_frame = error_frame


        elif user_type == "paciente":
            from ui.pacientes.dashboard import PacienteDashboard
            self.current_frame = PacienteDashboard(self, self.current_user)

        elif user_type == "institucion":
            from ui.institucion.dashboard import InstitucionMainDashboard
            self.current_frame = InstitucionMainDashboard(self, self.current_user)

        # Empaquetamos el frame solo si se creó uno
        if self.current_frame:
            self.current_frame.pack(fill=tk.BOTH, expand=True)
    
    def logout(self):
        """Cerrar sesión"""
        self.current_user = None
        self.show_login()