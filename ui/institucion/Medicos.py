import tkinter as tk
from tkinter import ttk, messagebox
from controllers import inst_controller
from datetime import datetime

class MedicosDashboard(tk.Frame):
    def __init__(self, parent, institucion_id):
        super().__init__(parent)
        self.parent = parent
        self.institucion_id = institucion_id
        
        # Frame principal
        self.main_frame = ttk.Frame(self, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Crear widgets
        self.crear_widgets()
        
        # Cargar datos
        self.cargar_datos()
        
    def crear_widgets(self):
        # Título
        ttk.Label(
            self.main_frame,
            text="Gestión de Médicos",
            font=('Helvetica', 14, 'bold')
        ).pack(pady=(0, 20))
        
        # Frame para lista de médicos
        self.lista_frame = ttk.LabelFrame(
            self.main_frame,
            text="Médicos Registrados",
            padding="10"
        )
        self.lista_frame.pack(fill=tk.BOTH, expand=True)
        
        # TreeView para médicos
        columns = ("id", "usuario_id", "especialidad", "matricula", "duracion_turno")
        self.tree = ttk.Treeview(
            self.lista_frame,
            columns=columns,
            show='headings'
        )
        
        # Configurar columnas
        self.tree.heading('id', text='ID')
        self.tree.heading('usuario_id', text='Usuario ID')
        self.tree.heading('especialidad', text='Especialidad')
        self.tree.heading('matricula', text='Matrícula')
        self.tree.heading('duracion_turno', text='Duración Turno')
        
        # Ajustar anchos de columna
        self.tree.column('id', width=50)
        self.tree.column('usuario_id', width=100)
        self.tree.column('especialidad', width=150)
        self.tree.column('matricula', width=100)
        self.tree.column('duracion_turno', width=100)
        
        self.tree.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self.lista_frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Frame para botones
        btn_frame = ttk.Frame(self.main_frame)
        btn_frame.pack(fill=tk.X, pady=10)
        
        # Botones
        ttk.Button(
            btn_frame,
            text="Gestionar Horarios",
            command=self.gestionar_horarios
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            btn_frame,
            text="Agregar Médico",
            command=self.agregar_medico
        ).pack(side=tk.RIGHT, padx=5)
        
        ttk.Button(
            btn_frame,
            text="Eliminar Médico",
            command=self.eliminar_medico
        ).pack(side=tk.RIGHT, padx=5)
        
    def cargar_datos(self):
        try:
            # Limpiar TreeView
            for item in self.tree.get_children():
                self.tree.delete(item)
                
            # Obtener médicos
            medicos = inst_controller.obtenerMedicos()
            
            # Filtrar por institución
            medicos_institucion = [
                m for m in medicos 
                if m["institucion_id"] == self.institucion_id
            ]
            
            # Insertar en TreeView
            for medico in medicos_institucion:
                self.tree.insert("", tk.END, values=(
                    medico["id"],
                    medico["usuario_id"],
                    medico["especialidad"],
                    medico["matricula"],
                    medico["duracion_turno"]
                ))
                
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Error al cargar médicos: {str(e)}"
            )
            
    def gestionar_horarios(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning(
                "Advertencia",
                "Por favor seleccione un médico"
            )
            return
            
        medico_id = self.tree.item(seleccion[0])["values"][0]
        from .horarios import HorariosDisponiblesManager
        ventana_horarios = HorariosDisponiblesManager(self, medico_id)
        ventana_horarios.grab_set()
        
    def agregar_medico(self):
        # Esta función se implementará más adelante
        messagebox.showinfo(
            "Info",
            "Función de agregar médico en desarrollo"
        )
        
    def eliminar_medico(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning(
                "Advertencia",
                "Por favor seleccione un médico"
            )
            return
            
        if messagebox.askyesno(
            "Confirmar",
            "¿Está seguro que desea eliminar el médico seleccionado?"
        ):
            try:
                medico_id = self.tree.item(seleccion[0])["values"][0]
                # Implementar función de eliminación en inst_controller
                # inst_controller.eliminarMedico(medico_id)
                self.cargar_datos()
                messagebox.showinfo(
                    "Éxito",
                    "Médico eliminado correctamente"
                )
            except Exception as e:
                messagebox.showerror(
                    "Error",
                    f"Error al eliminar médico: {str(e)}"
                )