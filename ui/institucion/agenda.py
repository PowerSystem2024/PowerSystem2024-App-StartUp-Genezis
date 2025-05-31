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
        columns = ("hora", "medico", "estado")
        self.tree = ttk.Treeview(
            horarios_frame,
            columns=columns,
            show='headings'
        )
        
        # Configurar columnas
        self.tree.heading('hora', text='Hora')
        self.tree.heading('medico', text='Médico')
        self.tree.heading('estado', text='Estado')
        
        self.tree.column('hora', width=100)
        self.tree.column('medico', width=200)
        self.tree.column('estado', width=100)
        
        self.tree.pack(fill=BOTH, expand=True)
        
    def on_fecha_seleccionada(self, event=None):
        fecha = self.calendar.get_date()
        self.cargar_horarios_fecha(fecha)
        
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
            
            # Mostrar horarios en el TreeView
            for horario in horarios:
                self.tree.insert("", END, values=(
                    f"{horario['hora_inicio']} - {horario['hora_fin']}",
                    horario.get('medico_nombre', 'Sin asignar'),
                    'Disponible' if horario['activo'] else 'No disponible'
                ))
                
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Error al cargar horarios: {str(e)}"
            )