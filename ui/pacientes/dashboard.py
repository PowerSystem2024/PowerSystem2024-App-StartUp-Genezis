from tkinter import *
from ui.pacientes.perfil import PerfilFrame
from ui.pacientes.turnos_dashboard import TurnosPacienteFrame
from utils.sesion import usuario_actual

class PacienteDashboard(Frame):
    def __init__(self, parent, paciente_id, volver_callback=None):
        super().__init__(parent)
        self.parent = parent
        self.paciente_id = paciente_id
        self.volver_callback = volver_callback

        self.main_container = Frame(self)
        self.main_container.pack(side=TOP, anchor=N, pady=50)

        #Titulo dinamico
        nombre = usuario_actual.get("nombre", "Paciente")
        apellido = usuario_actual.get("apellido", "")
        titulo = f"Panel de {nombre} {apellido}"

        Label(self.main_container, text=titulo, font=("Arial", 18, "bold")).pack(pady=10)

        Button(self.main_container, text="Mis Datos", width=25, command=self.mostrar_perfil).pack(pady=5)
        Button(self.main_container, text="Mis Turnos", width=25, command=self.mostrar_turnos).pack(pady=5)
        Button(self.main_container, text="Cerrar Sesión", width=25, command=self.cerrar_sesion).pack(pady=20)

        self.current_subframe = None

    def limpiar_subframe(self):
        if self.current_subframe is not None:
            self.current_subframe.destroy()
            self.current_subframe = None

    def mostrar_perfil(self):
        self.ocultar_dashboard()
        self.limpiar_subframe()
        self.current_subframe = PerfilFrame(self, self.paciente_id, volver_callback=self.mostrar_dashboard)
        self.current_subframe.place(relx=0.5, rely=0.5, anchor=CENTER)

    def mostrar_turnos(self):
        self.ocultar_dashboard()
        self.limpiar_subframe()
        self.current_subframe = TurnosPacienteFrame(self, self.paciente_id, volver_callback=self.mostrar_dashboard)
        self.current_subframe.pack(fill=BOTH, expand=True)

    def ocultar_dashboard(self):
        self.main_container.pack_forget()

    def mostrar_dashboard(self):
        self.limpiar_subframe()
        self.main_container.pack(side=TOP, anchor=N, pady=50)  # <-- fuerza que se muestre arriba

    def cerrar_sesion(self):
        # Limpiamos el dashboard y llamamos al callback para volver al login
        self.limpiar_subframe()
        self.ocultar_dashboard()
        if self.volver_callback:
            self.volver_callback()



