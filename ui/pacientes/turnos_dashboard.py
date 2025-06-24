from tkinter import *
from tkinter import messagebox
from ui.pacientes.buscar_turnos import BuscarTurnosFrame
from ui.pacientes.historial_turnos import HistorialTurnosFrame
from ui.pacientes.reservar_turnos import ReservarTurnosFrame
from ui.pacientes.confirmar_turnos import ConfirmarTurnoFrame
from ui.pacientes.cancelar_turnos import CancelarTurnosFrame
from controllers.pac_controller import obtener_paciente_id_por_usuario

class TurnosPacienteFrame(Frame):
    def __init__(self, parent, paciente_id, volver_callback):
        super().__init__(parent)
        self.parent = parent
        self.usuario_id = paciente_id  # usuario_id
        self.volver_callback = volver_callback
        self.current_subframe = None

        # Contenedor del menú principal
        self.menu_container = Frame(self)
        self.menu_container.pack(side=TOP, anchor=N, pady=50)

        Label(self.menu_container, text="Gestión de Turnos", font=("Arial", 18, "bold")).pack(pady=10)
        Button(self.menu_container, text="Agendar un turno", width=30, command=self.buscar_turnos).pack(pady=5)
        Button(self.menu_container, text="Historial de Turnos", width=30, command=self.ver_historial).pack(pady=5)
        Button(self.menu_container, text="Cancelar Turno", width=30, command=self.cancelar_turno).pack(pady=5)
        Button(self.menu_container, text="Atrás", width=30, command=self.volver_callback).pack(pady=20)

        # Contenedor para subframes (como buscar_turnos, historial, etc.)
        self.subframe_container = Frame(self)
        self.subframe_container.pack(fill=BOTH, expand=True)

    def limpiar_subframe(self):
        if self.current_subframe is not None:
            self.current_subframe.destroy()
            self.current_subframe = None

    def ocultar_dashboard(self):
        self.menu_container.pack_forget()

    def mostrar_dashboard(self):
        self.limpiar_subframe()

        # Reempacar contenedores para asegurarse que se restablece el layout
        self.menu_container.pack_forget()
        self.subframe_container.pack_forget()

        self.menu_container.pack(side=TOP, anchor=N, pady=50)
        self.subframe_container.pack(fill=BOTH, expand=True)

    def buscar_turnos(self):
        self.ocultar_dashboard()
        self.limpiar_subframe()
        self.current_subframe = BuscarTurnosFrame(
            self.subframe_container,
            self.usuario_id,
            volver_callback=self.mostrar_dashboard
        )
        self.current_subframe.pack(fill=BOTH, expand=True)

    def confirmar_turno(self):
        self.ocultar_dashboard()
        self.limpiar_subframe()
        self.current_subframe = ConfirmarTurnoFrame(
            self.subframe_container,
            self.usuario_id,
            volver_callback=self.mostrar_dashboard
        )
        self.current_subframe.pack(fill=BOTH, expand=True)

    def cancelar_turno(self):
        self.ocultar_dashboard()
        self.limpiar_subframe()
        paciente_id = obtener_paciente_id_por_usuario(self.usuario_id)

        if paciente_id:
            self.current_subframe = CancelarTurnosFrame(
                self.subframe_container,
                paciente_id,
                volver_callback=self.mostrar_dashboard  # ✅ ESTA LÍNEA ES CLAVE
            )
            self.current_subframe.pack(fill=BOTH, expand=True)
        else:
            messagebox.showerror("Error", "No se encontró un paciente asociado a este usuario.")

    def ver_historial(self):
        self.ocultar_dashboard()
        self.limpiar_subframe()
        paciente_id = obtener_paciente_id_por_usuario(self.usuario_id)

        if not paciente_id:
            messagebox.showerror("Error", "No se encontró el paciente asociado al usuario.")
            return

        self.current_subframe = HistorialTurnosFrame(
            self.subframe_container,
            paciente_id,
            volver_callback=self.mostrar_dashboard
        )
        self.current_subframe.pack(fill=BOTH, expand=True)
