from tkinter import *
from tkinter import messagebox
from controllers import inst_controller
from ui.institucion.config import ConfigInstitucionFrame
from ui.institucion.Medicos import MedicosDashboard  # Asegúrate de que esta importación sea correcta


class InstitucionMainDashboard(Frame):
    def __init__(self, parent, user):
        super().__init__(parent)
        self.parent = parent
        self.user = user

        self.top_frame = Frame(self, padx=20, pady=20)
        self.top_frame.pack(side=TOP, fill=X)

        self.subframe_container = Frame(self)
        self.subframe_container.pack(fill=BOTH, expand=True, padx=10, pady=10)
        self.current_subframe = None

        # La variable para la ventana de horarios
        self.horarios_window = None  # Inicializamos a None

        # Título
        Label(
            self.top_frame,
            text="Panel de Control - Institución",
            font=('Helvetica', 16, 'bold')
        ).pack(pady=10)

        # Información de la institución
        self.info_frame = LabelFrame(self.top_frame, text="Información de la Institución")
        self.info_frame.pack(fill=X, pady=10)

        # Botones de acción
        self.crear_botones()

        # Frame para mostrar datos (de la institución)
        self.data_display_frame = Frame(self.top_frame)
        self.data_display_frame.pack(fill=BOTH, expand=True)

        # Cargar datos iniciales
        self.cargar_datos_institucion()

    def cargar_datos_institucion(self):
        """Método separado para cargar/recargar datos de la institución"""
        try:
            instituciones = inst_controller.obtenerInstitucion()

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
        btn_frame = Frame(self.top_frame)
        btn_frame.pack(fill=X, pady=10)

        Button(
            btn_frame,
            text="Médicos",
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
        for widget in self.data_display_frame.winfo_children():
            widget.destroy()

        campos = [
            ("Nombre:", institucion["nombre"]),
            ("Dirección:", institucion["direccion"]),
            ("Teléfono:", institucion["telefono"]),
            ("Email:", institucion["email"]),
            ("Horario:", f"{institucion['horario_apertura']} - {institucion['horario_cierre']}")
        ]

        for i, (label, valor) in enumerate(campos):
            Label(self.data_display_frame, text=label, font=('Helvetica', 10, 'bold')).grid(
                row=i, column=0, padx=5, pady=2, sticky='e'
            )
            Label(self.data_display_frame, text=valor).grid(
                row=i, column=1, padx=5, pady=2, sticky='w'
            )

    def limpiar_subframe(self):
        if self.current_subframe is not None:
            self.current_subframe.destroy()
            self.current_subframe = None

    def medicosButton(self):
        self.limpiar_subframe()
        self.current_subframe = MedicosDashboard(self.subframe_container, self.institucion)
        self.current_subframe.pack(fill=BOTH, expand=True)

    def editar_info(self):
        self.limpiar_subframe()
        self.current_subframe = ConfigInstitucionFrame(
            self.subframe_container,
            self.institucion,
            self.actualizar_datos_dashboard
        )
        self.current_subframe.pack(fill=BOTH, expand=True)

    def mostrar_calendario(self):
        try:
            # Revisa si la ventana ya existe y está abierta, si es así la trae al frente
            # self.horarios_window es ahora la instancia de HorariosDisponiblesManager (que es un Toplevel)
            if self.horarios_window and self.horarios_window.winfo_exists():
                self.horarios_window.lift()
                self.horarios_window.focus_force()
                return

            # Importación local (para evitar problemas de dependencias circulares)
            from ui.institucion.horarios import HorariosDisponiblesManager

            # ¡LA CORRECCIÓN CLAVE AQUÍ!
            # Instanciamos directamente HorariosDisponiblesManager, ya que es un Toplevel.
            # El 'parent' debe ser la ventana principal de la aplicación (self.parent, que es tk.Tk).
            self.horarios_window = HorariosDisponiblesManager(
                self.parent,  # Pasa el main Tk() root como el parent
                self.institucion["id"]
            )
            # NO se llama a .pack() sobre self.horarios_window porque ya es una ventana Toplevel
            # Sus elementos internos se empaquetan dentro de su propia clase __init__

        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Error al mostrar calendario: {str(e)}"
            )