from tkinter import *
from ui.pacientes.perfil import PerfilFrame
from ui.pacientes.turnos import TurnosPacienteFrame

class PacienteDashboard(Frame):
    def __init__(self, parent, paciente_id, volver_callback=None):
        super().__init__(parent)
        self.parent = parent
        self.paciente_id = paciente_id
        self.volver_callback = volver_callback

        self.main_container = Frame(self)
        self.main_container.pack(side=TOP, anchor=N, pady=50)

        Label(self.main_container, text="Panel del Paciente", font=("Arial", 18, "bold")).pack(pady=10)

        Button(self.main_container, text="Ver / Editar Perfil", width=25, command=self.mostrar_perfil).pack(pady=5)
        Button(self.main_container, text="Mis Turnos", width=25, command=self.mostrar_turnos).pack(pady=5)

        self.current_subframe = None

    def limpiar_subframe(self):
        if self.current_subframe is not None:
            self.current_subframe.destroy()
            self.current_subframe = None

    def mostrar_perfil(self):
        self.ocultar_dashboard()
        self.limpiar_subframe()
        self.current_subframe = PerfilFrame(self, self.paciente_id, volver_callback=self.mostrar_dashboard)
        self.current_subframe.pack(fill=BOTH, expand=True)

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
