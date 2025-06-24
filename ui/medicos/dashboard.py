from tkinter import *
from ui.medicos.agenda import AgendaMedicoFrame
from ui.medicos.horarios import HorariosFrame
from ui.medicos.pacientes import PacientesFrame


class MedicoDashboard(Frame):
    def __init__(self, parent, medico_id):
        super().__init__(parent)
        self.parent = parent
        self.medico_id = medico_id

        Label(self, text="Panel Médico", font=("Arial", 18, "bold")).pack(pady=10)

        Button(self, text="Ver Agenda", width=25, command=self.mostrar_agenda).pack(pady=5)
        Button(self, text="Configurar Horarios", width=25, command=self.mostrar_horarios).pack(pady=5)
        Button(self, text="Ver Pacientes", width=25, command=self.mostrar_pacientes).pack(pady=5)
        Button(self, text="Cerrar Sesión", width=25, command=self.parent.logout).pack(pady=5)
        

        self.subframe_container = Frame(self)
        self.subframe_container.pack(fill=BOTH, expand=True, padx=10, pady=10)
        self.current_subframe = None

    def limpiar_subframe(self):
        if self.current_subframe:
            self.current_subframe.destroy()
            self.current_subframe = None

    def mostrar_agenda(self):
        self.limpiar_subframe()
        self.current_subframe = AgendaMedicoFrame(self.subframe_container, self.medico_id)
        self.current_subframe.pack(fill=BOTH, expand=True)

    def mostrar_horarios(self):
        self.limpiar_subframe()
        self.current_subframe = HorariosFrame(self.subframe_container, self.medico_id)
        self.current_subframe.pack(fill=BOTH, expand=True)

    def mostrar_pacientes(self):
        self.limpiar_subframe()
        self.current_subframe = PacientesFrame(self.subframe_container, self.medico_id)
        self.current_subframe.pack(fill=BOTH, expand=True)