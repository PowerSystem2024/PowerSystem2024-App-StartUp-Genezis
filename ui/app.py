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

    # ---------------------------------------------------------------------------------------------------------

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

    # ------------------ INICIO DE CAMBIOS Y RESTAURACIÓN DE LÓGICA ------------------
    def on_login_success(self, user):
        """Callback cuando el login es exitoso"""
        self.current_user = user  # Almacenamos el objeto 'user' completo

        # Mostrar el panel correspondiente según el tipo de usuario
        # ¡IMPORTANTE! Pasamos el objeto 'user' completo a show_dashboard
        self.show_dashboard(user)

    def show_dashboard(self, user_data):  # Ahora recibimos el objeto 'user_data' completo
        """Mostrar el dashboard según el tipo de usuario"""
        if self.current_frame:
            self.current_frame.destroy()
            self.current_frame = None  # Buena práctica para limpiar la referencia

        user_type = user_data["tipo"]  # Obtenemos el tipo de usuario del diccionario user_data

        if user_type == "admin":
            from ui.admin.dashboard import AdminDashboard
            # Para el dashboard de administrador, se sigue pasando self.current_user (el diccionario completo)
            self.current_frame = AdminDashboard(self, self.current_user)

        elif user_type == "medico":
            from ui.medicos.dashboard import MedicoDashboard
            # Importamos la función necesaria desde el controlador
            from controllers.med_controller import obtener_medico_id_por_usuario_id

            usuario_id = self.current_user["id"]  # Obtenemos el ID de usuario del diccionario current_user

            # Usamos la función para obtener el ID de médico real a partir del ID de usuario
            medico_id_real = obtener_medico_id_por_usuario_id(usuario_id)

            if medico_id_real:
                # Si se encuentra el ID de médico real, se pasa el objeto user_data completo al MedicoDashboard.
                # El MedicoDashboard ahora espera este diccionario para acceder a sus propios datos de usuario.
                self.current_frame = MedicoDashboard(self, user_data)  # Pasar user_data completo
            else:
                # Si no se encuentra un perfil de médico asociado, se muestra un mensaje de error
                # y se ofrece la opción de volver al inicio de sesión.
                messagebox.showerror("Error de Perfil",
                                     "Este usuario no está registrado como médico. Por favor, comuníquese con administración.",
                                     parent=self)  # Agregado parent=self para que el messagebox sea modal a la app

                # Crear un frame con un botón "Volver al Inicio de Sesión"
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
            # Para el dashboard de paciente, se sigue pasando el objeto user_data completo.
            self.current_frame = PacienteDashboard(self, user_data)

        elif user_type == "institucion":
            from ui.institucion.dashboard import InstitucionMainDashboard
            # Para el dashboard de institución, se sigue pasando self.current_user.
            self.current_frame = InstitucionMainDashboard(self, self.current_user)

        # Empaquetamos el frame solo si se creó uno
        if self.current_frame:
            self.current_frame.pack(fill=tk.BOTH, expand=True)

    # ------------------- FIN DE CAMBIOS Y RESTAURACIÓN DE LÓGICA -------------------

    def logout(self):
        """Cerrar sesión"""
        self.current_user = None
        self.show_login()
