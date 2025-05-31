from tkinter import *
from tkinter import messagebox
from controllers import inst_controller
from ui.institucion.config import ConfigInstitucionFrame
from ui.institucion.Medicos import MedicosDashboard


class InstitucionMainDashboard(Frame):
    def __init__(self, parent, user):
        super().__init__(parent)
        self.parent = parent
        self.user = user

        # Frame principal
        self.main_frame = Frame(self)
        self.main_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)

        # frame Subpantallas
        self.subframe_container = Frame(self)
        self.subframe_container.pack(fill=BOTH, expand=True, padx=10, pady=10)
        self.current_subframe = None

        # Variables para ventanas separadas
        self.medicos_window = None

        # Título
        Label(
            self.main_frame,
            text="Panel de Control - Institución",
            font=('Helvetica', 16, 'bold')
        ).pack(pady=10)

        # Información de la institución
        self.info_frame = LabelFrame(self.main_frame, text="Información de la Institución")
        self.info_frame.pack(fill=X, pady=10)

        # Botones de acción
        self.crear_botones()

        # Frame para mostrar datos
        self.data_frame = Frame(self.main_frame)
        self.data_frame.pack(fill=BOTH, expand=True)

        # Cargar datos iniciales
        self.cargar_datos_institucion()

    def cargar_datos_institucion(self):
        """Método separado para cargar/recargar datos de la institución"""
        try:
            instituciones = inst_controller.obtenerInstitucion()

            # Encontrar la institución del usuario actual
            institucion = next(
                (inst for inst in instituciones if inst["usuario_id"] == self.user["id"]),
                None
            )

            if institucion:
                self.mostrar_datos_institucion(institucion)
                self.institucion = institucion
            else:
                messagebox.showinfo("Info", "No se encontraron datos de la institución")

        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar datos: {str(e)}")

    def actualizar_datos_dashboard(self):
        """Callback para actualizar el dashboard cuando se modifiquen los datos"""
        self.cargar_datos_institucion()
        self.limpiar_subframe()

    def crear_botones(self):
        btn_frame = Frame(self.main_frame)
        btn_frame.pack(fill=X, pady=10)

        Button(
            btn_frame,
            text="Medicos",
            command=self.medicosButton
        ).pack(side=LEFT, padx=5)

        Button(
            btn_frame,
            text="Editar Información",
            command=self.editar_info
        ).pack(side=LEFT, padx=5)

        Button(
            btn_frame,
            text="Calendario",
            command=self.mostrar_calendario
        ).pack(side=LEFT, padx=5)

        Button(
            btn_frame,
            text="Cerrar Sesión",
            command=self.parent.logout
        ).pack(side=RIGHT, padx=5)

    def mostrar_datos_institucion(self, institucion):
        # Limpiar frame de datos previos
        for widget in self.data_frame.winfo_children():
            widget.destroy()

        # Mostrar datos en grid
        campos = [
            ("Nombre:", institucion["nombre"]),
            ("Dirección:", institucion["direccion"]),
            ("Teléfono:", institucion["telefono"]),
            ("Email:", institucion["email"]),
            ("Horario:", f"{institucion['horario_apertura']} - {institucion['horario_cierre']}")
        ]

        for i, (label, valor) in enumerate(campos):
            Label(self.data_frame, text=label, font=('Helvetica', 10, 'bold')).grid(
                row=i, column=0, padx=5, pady=2, sticky='e'
            )
            Label(self.data_frame, text=valor).grid(
                row=i, column=1, padx=5, pady=2, sticky='w'
            )

    def limpiar_subframe(self):
        if self.current_subframe is not None:
            self.current_subframe.destroy()
            self.current_subframe = None

    def medicosButton(self):
        # Verificar si ya existe una ventana de médicos abierta
        if self.medicos_window is not None and self.medicos_window.winfo_exists():
            # Si existe, traerla al frente
            self.medicos_window.lift()
            self.medicos_window.focus_force()
            return

        # Crear nueva ventana separada
        self.medicos_window = Toplevel(self.parent)
        self.medicos_window.title("Panel de Médicos")
        self.medicos_window.geometry("800x600")

        # Configurar el comportamiento de cierre
        self.medicos_window.protocol("WM_DELETE_WINDOW", self.cerrar_ventana_medicos)

        # Crear el dashboard de médicos en la nueva ventana
        medicos_dashboard = MedicosDashboard(self.medicos_window, self.institucion)
        medicos_dashboard.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # Hacer que la ventana sea modal (opcional)
        # self.medicos_window.transient(self.parent)
        # self.medicos_window.grab_set()

    def cerrar_ventana_medicos(self):
        """Método para limpiar la referencia cuando se cierra la ventana"""
        if self.medicos_window:
            self.medicos_window.destroy()
            self.medicos_window = None

    def editar_info(self):
        self.limpiar_subframe()
        # Pasar el callback para actualizar el dashboard
        self.current_subframe = ConfigInstitucionFrame(
            self.subframe_container,
            self.institucion,
            self.actualizar_datos_dashboard
        )
        self.current_subframe.pack(fill=BOTH, expand=True)

    def mostrar_calendario(self):
        try:
            # Cerrar ventana anterior si existe
            if hasattr(self, 'horarios_window'):
                self.horarios_window.destroy()
            
            # Crear nueva ventana
            from .horarios import HorariosDisponiblesManager
            self.horarios_window = HorariosDisponiblesManager(
                self, 
                self.institucion["id"]
            )
        
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Error al mostrar calendario: {str(e)}"
            )