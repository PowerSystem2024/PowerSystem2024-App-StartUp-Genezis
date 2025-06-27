from tkinter import *
from ui.medicos.agenda import AgendaMedicoFrame
from ui.medicos.horarios import HorariosFrame
from ui.medicos.pacientes import PacientesFrame

# Reemplaza el contenido de tu archivo de dashboard de médico con esto

from tkinter import *
from tkinter import messagebox
from ui.medicos.agenda import AgendaMedicoFrame
from ui.medicos.horarios import HorariosFrame
from ui.medicos.pacientes import PacientesFrame
from ui.medicos.datosMedico import DatosMedicoWindow  # <-- IMPORTANTE: importar la nueva ventana
import controllers.med_controller as med_controller  # <-- IMPORTANTE: importar el controller


class MedicoDashboard(Frame):
    # --- MODIFICACIÓN: Ahora recibe user_data ---
    def __init__(self, parent, user_data):
        super().__init__(parent)
        self.parent = parent
        self.user_data = user_data  # Guardamos los datos del usuario (incluye el id de la tabla 'usuarios')

        # Obtenemos el ID de la tabla 'medicos' a partir del 'usuario_id'
        self.medico_id = med_controller.obtener_medico_id_por_usuario_id(self.user_data['id'])

        if not self.medico_id:
            # Esto es un caso de error grave, el usuario médico no tiene un perfil de médico asociado.
            Label(self, text="Error: No se encontró el perfil del médico.", font=("Arial", 18, "bold"), fg="red").pack(
                pady=20)
            Button(self, text="Cerrar Sesión", width=25, command=self.parent.logout).pack(pady=5)
            return

        # --- Interfaz de usuario ---
        Label(self, text=f"Panel Médico - Dr(a). {self.user_data.get('apellido')}", font=("Arial", 18, "bold")).pack(
            pady=10)

        Button(self, text="Ver Agenda", width=25, command=self.mostrar_agenda).pack(pady=5)
        Button(self, text="Configurar Horarios", width=25, command=self.mostrar_horarios).pack(pady=5)
        Button(self, text="Ver Pacientes", width=25, command=self.mostrar_pacientes).pack(pady=5)

        # --- NUEVO BOTÓN ---
        Button(self, text="Editar Mis Datos", width=25, command=self.mostrar_ventana_datos).pack(pady=5)

        Button(self, text="Cerrar Sesión", width=25, command=self.parent.logout).pack(pady=5)

        self.subframe_container = Frame(self)
        self.subframe_container.pack(fill=BOTH, expand=True, padx=10, pady=10)
        self.current_subframe = None

        self.mostrar_agenda()  # Mostrar la agenda por defecto al iniciar

    def limpiar_subframe(self):
        if self.current_subframe:
            self.current_subframe.destroy()
            self.current_subframe = None

    # --- NUEVA FUNCIÓN ---
    def mostrar_ventana_datos(self):
        """Obtiene la información completa del médico y abre la ventana de edición."""
        try:
            # Usamos el usuario_id para obtener la info completa
            info_medico_lista = med_controller.obtener_info_completa_medico(self.user_data['id'])

            if not info_medico_lista:
                messagebox.showerror("Error", "No se pudo cargar tu información de perfil.")
                return

            info_medico = info_medico_lista[0]

            # Abrimos la ventana de edición, pasando los datos necesarios
            DatosMedicoWindow(self, self.user_data, info_medico)

        except Exception as e:
            messagebox.showerror("Error Inesperado", f"Ocurrió un error al intentar abrir el perfil: {e}")

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