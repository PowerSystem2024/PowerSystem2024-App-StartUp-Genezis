from tkinter import *
from tkinter import ttk, messagebox
from tkcalendar import Calendar
from controllers import inst_controller
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
            
            # Obtener horarios para la fecha seleccionada
            horarios = inst_controller.obtener_turnos_fecha(
                self.institucion_id,
                fecha
            )
        
            if not horarios:
                self.tree.insert("", END, values=(
                    "-",
                    "-",
                    "-",
                    "Sin turnos disponibles"
                ))
                return
        
            # Mostrar horarios en el TreeView
            for horario in horarios:
                # Obtener datos del médico
                medico = horario.get('medicos', {})
                medico_usuario = medico.get('usuarios', {})
            
                # Obtener datos del paciente
                paciente = horario.get('pacientes', {})
                paciente_usuario = paciente.get('usuarios', {})
            
                # Formatear datos
                nombre_medico = f"{medico_usuario.get('nombre', '')} {medico_usuario.get('apellido', '')}"
                nombre_paciente = f"{paciente_usuario.get('nombre', '')} {paciente_usuario.get('apellido', '')}"
            
                self.tree.insert("", END, values=(
                    nombre_medico,
                    f"{horario.get('hora_inicio', '')} - {horario.get('hora_fin', '')}",
                    nombre_paciente if nombre_paciente.strip() else "Sin asignar",
                    'Ocupado' if paciente else 'Disponible'
                ))
                
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Error al cargar horarios: {str(e)}"
            )
            print(f"Error detallado: {str(e)}")  # Para debug