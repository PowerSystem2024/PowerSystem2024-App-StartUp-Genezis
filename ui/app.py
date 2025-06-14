import tkinter as tk
from tkinter import ttk, messagebox
from ui.loginInterface import LoginInterface
from ui.register import RegisterFrame

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Sistema de Turnos Médicos")

        window_width = 895
        window_height = 587
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_height / 2 - window_height / 2)
        self.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        self.resizable(False, False)

        self.current_user = None
        self.current_frame = None

        self.show_login()

    def show_register(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = RegisterFrame(self, self.on_register_success)
        self.current_frame.pack(fill=tk.BOTH, expand=True)

    def on_register_success(self):
        messagebox.showinfo("Registro exitoso", "Usuario registrado correctamente. Por favor, inicie sesión.")
        self.show_login()

    def show_login(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = LoginInterface(self, self.on_login_success)
        self.current_frame.pack(fill=tk.BOTH, expand=True)

    def on_login_success(self, user):
        self.current_user = user
        self.show_dashboard(user["tipo"])

    def show_dashboard(self, user_type):
        if self.current_frame:
            self.current_frame.destroy()

        if user_type == "admin":
            from ui.admin.dashboard import AdminDashboard
            self.current_frame = AdminDashboard(self, self.current_user)

        elif user_type == "medico":
            from ui.medicos.dashboard import MedicoDashboard
            from controllers.med_controller import obtener_medico_por_usuario

            medico = obtener_medico_por_usuario(self.current_user["id"])
            if medico:
                self.current_frame = MedicoDashboard(self, medico["id"])
            else:
                messagebox.showerror("Error", "No se encontró un médico asociado a este usuario.")
                return

        elif user_type == "paciente":
            from ui.pacientes.dashboard import PacienteDashboard
            self.current_frame = PacienteDashboard(self, self.current_user)

        elif user_type == "institucion":
            from ui.institucion.dashboard import InstitucionDashboard
            self.current_frame = InstitucionDashboard(self, self.current_user)

        self.current_frame.pack(fill=tk.BOTH, expand=True)

    def logout(self):
        self.current_user = None
        self.show_login()
