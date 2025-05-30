import tkinter as tk
from tkinter import ttk, messagebox
from controllers import inst_controller

class HorariosDisponiblesManager(tk.Toplevel):
    def __init__(self, parent, institucion_id):
        super().__init__(parent)
        self.title("Gestión de Horarios")
        self.geometry("800x500")
        self.institucion_id = institucion_id

        # Configuración de la ventana
        self.configure(bg='#f0f0f0')
        self.resizable(False, False)

        # Frame principal
        self.main_frame = ttk.Frame(self, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Crear widgets
        self.crear_widgets()

    def crear_widgets(self):
        # Frame para horarios actuales
        horarios_frame = ttk.LabelFrame(self.main_frame, text="Horarios de la Institución", padding="10")
        horarios_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        # Mostrar horarios actuales
        self.mostrar_horarios_actuales(horarios_frame)

        # Frame para edición
        edicion_frame = ttk.LabelFrame(self.main_frame, text="Editar Horarios", padding="10")
        edicion_frame.pack(fill=tk.X, pady=(0, 10))

        # Campos de edición
        self.crear_campos_edicion(edicion_frame)

    def mostrar_horarios_actuales(self, frame):
        # Crear Treeview
        columns = ("dia", "apertura", "cierre")
        self.tree = ttk.Treeview(frame, columns=columns, show='headings')
        
        # Configurar columnas
        self.tree.heading('dia', text='Día')
        self.tree.heading('apertura', text='Horario Apertura')
        self.tree.heading('cierre', text='Horario Cierre')
        
        # Configurar anchos
        for col in columns:
            self.tree.column(col, width=150, anchor='center')
        
        self.tree.pack(fill=tk.BOTH, expand=True, pady=5)

        # Cargar datos
        self.cargar_horarios()

    def crear_campos_edicion(self, frame):
        # Frame para entrada de datos
        entrada_frame = ttk.Frame(frame)
        entrada_frame.pack(fill=tk.X, pady=5)

        # Horario de apertura
        ttk.Label(entrada_frame, text="Horario Apertura:").pack(side=tk.LEFT, padx=5)
        self.apertura_var = tk.StringVar(value="08:00")
        self.apertura_entry = ttk.Entry(entrada_frame, textvariable=self.apertura_var, width=10)
        self.apertura_entry.pack(side=tk.LEFT, padx=5)

        # Horario de cierre
        ttk.Label(entrada_frame, text="Horario Cierre:").pack(side=tk.LEFT, padx=5)
        self.cierre_var = tk.StringVar(value="17:00")
        self.cierre_entry = ttk.Entry(entrada_frame, textvariable=self.cierre_var, width=10)
        self.cierre_entry.pack(side=tk.LEFT, padx=5)

        # Botones
        ttk.Button(
            entrada_frame,
            text="Guardar Cambios",
            command=self.guardar_cambios
        ).pack(side=tk.RIGHT, padx=5)

    def cargar_horarios(self):
        try:
            horarios = inst_controller.obtener_horarios(self.institucion_id)
            if horarios:
                self.apertura_var.set(horarios["apertura"])
                self.cierre_var.set(horarios["cierre"])
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar horarios: {str(e)}")

    def guardar_cambios(self):
        try:
            apertura = self.apertura_var.get()
            cierre = self.cierre_var.get()

            if not self.validar_formato_hora(apertura) or not self.validar_formato_hora(cierre):
                messagebox.showerror("Error", "Formato de hora inválido. Use HH:MM")
                return

            inst_controller.actualizar_horarios(
                self.institucion_id,
                apertura,
                cierre
            )
            messagebox.showinfo("Éxito", "Horarios actualizados correctamente")
            self.cargar_horarios()
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar cambios: {str(e)}")

    @staticmethod
    def validar_formato_hora(hora):
        try:
            hora = hora.strip()
            horas, minutos = map(int, hora.split(":"))
            return 0 <= horas < 24 and 0 <= minutos < 60
        except:
            return False