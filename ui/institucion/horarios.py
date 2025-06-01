import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar
from controllers import inst_controller
from datetime import datetime

class HorariosDisponiblesManager(tk.Toplevel):
    def __init__(self, parent, institucion_id):
        super().__init__(parent)
        self.title("Gestión de Horarios")
        self.geometry("800x600")
        self.institucion_id = institucion_id

        # Configuración de la ventana
        self.configure(bg='#f0f0f0')
        self.resizable(False, False)
        self.grab_set()  # Hacer la ventana modal

        # Frame principal
        self.main_frame = ttk.Frame(self, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Crear widgets
        self.crear_widgets()

    def crear_widgets(self):
        # Frame para calendario
        calendar_frame = ttk.LabelFrame(
            self.main_frame, 
            text="Selección de Fecha", 
            padding="10"
        )
        calendar_frame.pack(fill=tk.X, pady=(0, 10))

        # Agregar calendario
        self.calendar = Calendar(
            calendar_frame,
            selectmode='day',
            date_pattern='y-mm-dd',
            locale='es_ES',
            showweeknumbers=False
        )
        self.calendar.pack(pady=5)
        self.calendar.bind("<<CalendarSelected>>", self.on_fecha_seleccionada)

        # Frame para horarios
        horarios_frame = ttk.LabelFrame(
            self.main_frame, 
            text="Horarios Disponibles", 
            padding="10"
        )
        horarios_frame.pack(fill=tk.BOTH, expand=True)

        # TreeView con nuevas columnas
        columns = ("medico", "hora", "paciente", "estado")
        self.tree = ttk.Treeview(
            horarios_frame, 
            columns=columns, 
            show='headings'
        )
        
        # Configurar columnas
        self.tree.heading('medico', text='Médico')
        self.tree.heading('hora', text='Hora')
        self.tree.heading('paciente', text='Paciente')
        self.tree.heading('estado', text='Estado')
        
        self.tree.column('medico', width=200)
        self.tree.column('hora', width=150)
        self.tree.column('paciente', width=200)
        self.tree.column('estado', width=100)
        
        self.tree.pack(fill=tk.BOTH, expand=True)

    def on_fecha_seleccionada(self, event=None):
        try:
            fecha = self.calendar.get_date()
            self.cargar_horarios_fecha(fecha)
            
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Error al procesar la fecha: {str(e)}"
            )

    def cargar_horarios_fecha(self, fecha):
        try:
            # Limpiar TreeView
            for item in self.tree.get_children():
                self.tree.delete(item)

            # Obtener turnos
            turnos = inst_controller.obtener_turnos_fecha(
                self.institucion_id, 
                fecha
            )

            if not turnos:
                self.tree.insert("", tk.END, values=(
                    "-",
                    "-",
                    "-",
                    "Sin turnos disponibles"
                ))
                return

            # Insertar turnos
            for turno in turnos:
                # Obtener datos del médico
                medico = turno.get('medicos', {})
                medico_usuario = medico.get('usuarios', {})
            
                # Obtener datos del paciente
                paciente = turno.get('pacientes', {})
                paciente_usuario = paciente.get('usuarios', {})
            
                # Formatear datos
                nombre_medico = f"{medico_usuario.get('nombre', '')} {medico_usuario.get('apellido', '')}"
                nombre_paciente = f"{paciente_usuario.get('nombre', '')} {paciente_usuario.get('apellido', '')}"
            
                self.tree.insert("", tk.END, values=(
                    nombre_medico,
                    f"{turno.get('hora_inicio', '')} - {turno.get('hora_fin', '')}",
                    nombre_paciente if nombre_paciente.strip() else "Sin asignar",
                    'Ocupado' if paciente else 'Disponible'
                ))

        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Error al cargar horarios: {str(e)}"
            )
            print(f"Error detallado: {str(e)}")