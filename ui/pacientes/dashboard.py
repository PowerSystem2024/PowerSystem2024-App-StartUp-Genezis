from tkinter import *
from ui.pacientes.perfil import PerfilFrame


class PacienteDashboard(Frame):
    def __init__(self, parent, paciente_id):
        super().__init__(parent)
        self.parent = parent
        self.paciente_id = paciente_id

        Label(self, text="Panel del Paciente", font=("Arial", 18, "bold")).pack(pady=10)

        Button(self, text="Ver / Editar Perfil", width=25, command=self.mostrar_perfil).pack(pady=5)


        self.subframe_container = Frame(self)
        self.subframe_container.pack(fill=BOTH, expand=True, padx=10, pady=10)

        self.current_subframe = None

    def limpiar_subframe(self):
        if self.current_subframe is not None:
            self.current_subframe.destroy()
            self.current_subframe = None

    def mostrar_perfil(self):
        self.limpiar_subframe()
        perfil = PerfilFrame(self.subframe_container, self.paciente_id)


        perfil.pack(fill=BOTH, expand=True)
        self.current_subframe = perfil


