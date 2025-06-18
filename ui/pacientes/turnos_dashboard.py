from tkinter import *
from tkinter import messagebox

from controllers.pac_controller import obtener_historial_turnos, confirmar_turno, cancelar_turno, reservar_turno, buscar_turnos_disponibles
from ui.pacientes.buscar_turnos import BuscarTurnosFrame
from ui.pacientes.historial_turnos import HistorialTurnosFrame
from ui.pacientes.reservar_turnos import ReservarTurnosFrame
from ui.pacientes.confirmar_turnos import ConfirmarTurnoFrame
from ui.pacientes.cancelar_turnos import CancelarTurnosFrame
from controllers.pac_controller import obtener_paciente_id_por_usuario
class TurnosPacienteFrame(Frame):
    def __init__(self, parent, paciente_id, volver_callback):
        super().__init__(parent)
        self.current_subframe = None
        self.parent = parent
        self.paciente_id = paciente_id["id"]
        self.volver_callback = volver_callback

        Label(self, text="Gestión de Turnos", font=("Arial", 18, "bold")).pack(pady=10)

        # Botones de acciones
        Button(self, text="Historial de Turnos", width=30, command=self.ver_historial).pack(pady=5)
        Button(self, text="Buscar Turnos Disponibles", width=30, command=self.buscar_turnos).pack(pady=5)
        Button(self, text="Reservar Turno", width=30, command=self.reservar_turno).pack(pady=5)
        Button(self, text="Confirmar Turno", width=30, command=self.confirmar_turno).pack(pady=5)
        Button(self, text="Cancelar Turno", width=30, command=self.cancelar_turno).pack(pady=5)
        Button(self, text="Atrás", width=30, command=self.volver_callback).pack(pady=20)


        # Contenedor para los subframes dinámicos
        self.subframe_container = Frame(self)
        self.subframe_container.pack(fill=BOTH, expand=True, padx=10, pady=10)

        self.current_subframe = None

    def limpiar_subframe(self):
        if self.current_subframe is not None:
            self.current_subframe.destroy()
            self.current_subframe = None

    def ver_historial(self):
        self.limpiar_subframe()
        self.current_subframe = HistorialTurnosFrame(self.subframe_container, self.paciente_id, volver_callback=self.mostrar_dashboard)
        self.current_subframe.pack(fill=BOTH, expand=True)

    def reservar_turno(self):
        self.limpiar_subframe()
        self.current_subframe = ReservarTurnosFrame(self.subframe_container, self.paciente_id)
        self.current_subframe.pack(fill=BOTH, expand=True)

    def confirmar_turno(self):
        self.limpiar_subframe()
        self.current_subframe = ConfirmarTurnoFrame(self.subframe_container, self.paciente_id, volver_callback=self.mostrar_dashboard)
        self.current_subframe.pack(fill=BOTH, expand=True)

    def cancelar_turno(self):
        self.limpiar_subframe()

        # Obtener el paciente_id a partir del usuario_id
        paciente_id = obtener_paciente_id_por_usuario(self.paciente_id)  # self.paciente_id en realidad es usuario_id

        if paciente_id:
            self.current_subframe = CancelarTurnosFrame(self.subframe_container, paciente_id)
            self.current_subframe.pack(fill=BOTH, expand=True)
        else:
            messagebox.showerror("Error", "No se encontró un paciente asociado a este usuario.")

    def buscar_turnos(self):
        self.limpiar_subframe()
        self.current_subframe = BuscarTurnosFrame(self.subframe_container, self.paciente_id)
        self.current_subframe.pack(fill=BOTH, expand=True)

    def mostrar_turnos(self):
        self.limpiar_subframe()
        frame = TurnosPacienteFrame(self.subframe_container, self.paciente_id, volver_callback=self.mostrar_dashboard)
        frame.pack(fill=BOTH, expand=True)
        self.current_subframe = frame

    def mostrar_dashboard(self):
        self.limpiar_subframe()







