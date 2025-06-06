from tkinter import *
from tkcalendar import Calendar, dateentry
from controllers.pac_controller import obtener_historial_turnos
from datetime import datetime
from tkinter import messagebox


class HistorialTurnosFrame(Frame):
    def __init__(self, parent, paciente_id, volver_callback):
        super().__init__(parent)
        self.paciente_id = paciente_id
        self.volver_callback = volver_callback

        Label(self, text="Historial de Turnos", font=("Arial", 16, "bold")).pack(pady=10)

        # Calendario
        self.calendario = Calendar(self, selectmode='day', date_pattern='yyyy-mm-dd')
        self.calendario.pack(pady=10)

        Button(self, text="Ver Turnos del Día", command=self.mostrar_turnos_por_fecha).pack(pady=5)

        # Lista de turnos
        self.lista_turnos = Listbox(self, width=80, height=10)
        self.lista_turnos.pack(pady=10)

        # Botón atrás
        Button(self, text="Atrás", command=self.volver_callback).pack(pady=10)

    def mostrar_turnos_por_fecha(self):
        fecha_seleccionada = self.calendario.get_date()

        # Simulación de turnos: reemplazar con lógica real
        turnos_simulados = self.obtener_turnos_para_fecha(fecha_seleccionada)

        self.lista_turnos.delete(0, END)  # Limpiar lista

        if not turnos_simulados:
            self.lista_turnos.insert(END, "No hay turnos en esta fecha.")
        else:
            for turno in turnos_simulados:
                self.lista_turnos.insert(END, f"{turno['fecha']} - {turno['especialidad']} con {turno['medico']}")

    def obtener_turnos_para_fecha(self, fecha):
        """Simula obtención de turnos por fecha. Reemplazar por consulta real."""
        todos_los_turnos = [
            {"fecha": "2025-05-10", "especialidad": "Cardiología", "medico": "Dr. Gómez"},
            {"fecha": "2025-05-28", "especialidad": "Odontología", "medico": "Dra. Pérez"},
            {"fecha": "2025-05-28", "especialidad": "Clínica Médica", "medico": "Dr. Salas"},
            {"fecha": "2025-06-01", "especialidad": "Dermatología", "medico": "Dra. López"},
        ]

        return [turno for turno in todos_los_turnos if turno["fecha"] == fecha]
