from tkinter import *
from tkinter import messagebox
from controllers import inst_controller
from ui.institucion.config import ConfigInstitucionFrame

class InstitucionMainDashboard(Frame):
    def __init__(self, parent, user):
        super().__init__(parent)
        self.parent = parent
        self.user = user

        # Frame principal
        self.main_frame = Frame(self)
        self.main_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)

        #frame Subpantallas
        self.subframe_container = Frame(self)
        self.subframe_container.pack(fill=BOTH, expand=True, padx=10, pady=10)
        self.current_subframe = None

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
        # Aquí iría la lógica para actualizar datos
        messagebox.showinfo("Info", "Función de actualización en desarrollo")

    def editar_info(self):
        self.limpiar_subframe()
        self.current_subframe = ConfigInstitucionFrame(self.subframe_container, self.institucion)
        self.current_subframe.pack(fill=BOTH, expand=True)

    def mostrar_calendario(self):
        messagebox.showinfo(
            title="Calendario",
            message= "Panel de control de la institución\n\n"
            "Aquí puede ver el calendario de su institución médica"
        )