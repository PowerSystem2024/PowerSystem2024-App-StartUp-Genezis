from tkinter import *
from tkinter import ttk, messagebox
from tkcalendar import Calendar
from controllers import inst_controller
import json
from datetime import datetime

class AgendaMedicoFrame(Frame):
    def __init__(self, parent, institucion_id):
        super().__init__(parent)
        self.parent = parent
        self.institucion_id = institucion_id
        
        # Frame principal
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)
        
        # Crear widgets
        self.crear_widgets()
        
    def crear_widgets(self):
        # Frame para calendario
        calendar_frame = ttk.LabelFrame(
            self.main_frame,
            text="Calendario",
            padding="10"
        )
        calendar_frame.pack(fill=X, pady=(0, 10))
        
        # Agregar calendario
        self.calendar = Calendar(
            calendar_frame,
            selectmode='day',
            date_pattern='y-mm-dd',
            locale='es_ES'
        )
        self.calendar.pack(pady=5)
        self.calendar.bind("<<CalendarSelected>>", self.on_fecha_seleccionada)
        
        # Frame para horarios
        horarios_frame = ttk.LabelFrame(
            self.main_frame,
            text="Horarios del Día",
            padding="10"
        )
        horarios_frame.pack(fill=BOTH, expand=True)
        
        # TreeView para horarios
        columns = ("medico", "hora", "paciente", "estado")
        self.tree = ttk.Treeview(
            horarios_frame,
            columns=columns,
            show='headings',
            height=10
        )
    
        # Configurar columnas
        self.tree.heading('medico', text='Médico')
        self.tree.heading('hora', text='Hora')
        self.tree.heading('paciente', text='Paciente')
        self.tree.heading('estado', text='Estado')
    
        self.tree.column('medico', width=200, anchor=W)
        self.tree.column('hora', width=150, anchor=CENTER)
        self.tree.column('paciente', width=200, anchor=W)
        self.tree.column('estado', width=100, anchor=CENTER)
    
        self.tree.pack(fill=BOTH, expand=True)

    def cargar_horarios_fecha(self, fecha):
        try:
            # Limpiar TreeView
            for item in self.tree.get_children():
                self.tree.delete(item)

            all_turnos_detallados = inst_controller.obtenerTurnosConDetalles()

            turnos_filtrados = []
            if all_turnos_detallados:
                for turno in all_turnos_detallados:
                    if turno.get('institucion_id') == self.institucion_id and \
                            turno.get('fecha') == fecha:
                        turnos_filtrados.append(turno)

            # Debugging (el JSON de aquí debería ser el que queremos ahora)
            print("\n--- Datos de Turnos Filtrados (para debugging) ---")
            if turnos_filtrados:
                for i, t in enumerate(turnos_filtrados):
                    print(f"Turno {i + 1}:")
                    print(json.dumps(t, indent=2))
            else:
                print("No se encontraron turnos para la fecha y institución seleccionadas.")
            print("---------------------------------------------------\n")

            if not turnos_filtrados:
                self.tree.insert("", END, values=(
                    "-",
                    "-",
                    "-",
                    "Sin turnos agendados para esta fecha en esta institución"
                ))
                return

            for turno in turnos_filtrados:
                # Acceso a los datos del médico
                nombre_medico = "Médico (no disponible)"
                medico_data = turno.get('medicos', {})  # Obtiene el objeto 'medicos'

                # Accede al objeto 'usuarios' (no 'usuario') ya que es la forma estándar cuando es una sola FK a 'usuarios'
                medico_usuario_data = medico_data.get('usuarios', {})

                if medico_usuario_data and isinstance(medico_usuario_data, dict):
                    nombre = medico_usuario_data.get('nombre', '')
                    apellido = medico_usuario_data.get('apellido', '')
                    nombre_medico = f"{nombre} {apellido}".strip()
                    if not nombre_medico:
                        nombre_medico = "Médico (nombre no especificado)"

                # Acceso a los datos del paciente
                nombre_paciente = "No asignado"
                paciente_data = turno.get('pacientes', {})  # Obtiene el objeto 'pacientes'

                # Accede al objeto 'usuarios' (no 'usuario')
                paciente_usuario_data = paciente_data.get('usuarios', {})

                if paciente_usuario_data and isinstance(paciente_usuario_data, dict):
                    nombre = paciente_usuario_data.get('nombre', '')
                    apellido = paciente_usuario_data.get('apellido', '')
                    nombre_paciente = f"{nombre} {apellido}".strip()
                    if not nombre_paciente:
                        if turno.get('paciente_id'):
                            nombre_paciente = "Paciente (nombre no especificado)"
                        else:
                            nombre_paciente = "No asignado"
                elif turno.get('paciente_id'):
                    nombre_paciente = "Paciente (nombre no especificado)"

                estado_turno = turno.get('estado', 'Estado Desconocido')

                self.tree.insert("", END, values=(
                    nombre_medico,
                    f"{turno.get('hora_inicio', 'HH:MM')} - {turno.get('hora_fin', 'HH:MM')}",
                    nombre_paciente,
                    estado_turno
                ))

        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Error al cargar horarios: {str(e)}"
            )
            print(f"Error detallado en cargar_horarios_fecha: {str(e)}")  # Para debug