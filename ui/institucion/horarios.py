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

        # TreeView para horarios
        columns = ("hora", "estado")
        self.tree = ttk.Treeview(
            horarios_frame, 
            columns=columns, 
            show='headings'
        )
        
        # Configurar columnas
        self.tree.heading('hora', text='Hora')
        self.tree.heading('estado', text='Estado')
        
        self.tree.column('hora', width=150)
        self.tree.column('estado', width=150)
        
        self.tree.pack(fill=tk.BOTH, expand=True)

    def on_fecha_seleccionada(self, event=None):
        try:
            fecha = self.calendar.get_date()
            # Limpiar TreeView
            for item in self.tree.get_children():
                self.tree.delete(item)
            
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Error al procesar la fecha: {str(e)}"
            )