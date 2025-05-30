import tkinter as tk
from tkinter import ttk, messagebox
from controllers import inst_controller

class InstitucionMainDashboard(tk.Frame):
    def __init__(self, parent, user):
        super().__init__(parent)
        self.parent = parent
        self.user = user

        # Frame principal
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Título
        ttk.Label(
            self.main_frame,
            text="Panel de Control - Institución",
            font=('Helvetica', 16, 'bold')
        ).pack(pady=10)

        # Información de la institución
        self.info_frame = ttk.LabelFrame(self.main_frame, text="Información de la Institución")
        self.info_frame.pack(fill=tk.X, pady=10)

        # Botones de acción
        self.crear_botones()

        # Frame para mostrar datos
        self.data_frame = ttk.Frame(self.main_frame)
        self.data_frame.pack(fill=tk.BOTH, expand=True)

        # Cargar datos iniciales
        self.cargar_datos()

    def crear_botones(self):
        btn_frame = ttk.Frame(self.main_frame)
        btn_frame.pack(fill=tk.X, pady=10)

        ttk.Button(
            btn_frame,
            text="Medicos",
            command=self.medicosButton
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            btn_frame,
            text="Editar Información",
            command=self.editar_info
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            btn_frame,
            text="Calendario",
            command=self.mostrar_calendario
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            btn_frame,
            text="Cerrar Sesión",
            command=self.parent.logout
        ).pack(side=tk.RIGHT, padx=5)

    def cargar_datos(self):
        try:
            instituciones = inst_controller.obtenerInstitucion()
            # Encontrar la institución del usuario actual
            institucion = next(
                (inst for inst in instituciones if inst["usuario_id"] == self.user["id"]),
                None
            )

            if institucion:
                self.mostrar_datos_institucion(institucion)
            else:
                messagebox.showinfo("Info", "No se encontraron datos de la institución")
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar datos: {str(e)}")

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
            ttk.Label(self.data_frame, text=label, font=('Helvetica', 10, 'bold')).grid(
                row=i, column=0, padx=5, pady=2, sticky='e'
            )
            ttk.Label(self.data_frame, text=valor).grid(
                row=i, column=1, padx=5, pady=2, sticky='w'
            )

    def medicosButton(self):
        # Aquí iría la lógica para actualizar datos
        messagebox.showinfo("Info", "Función de actualización en desarrollo")

    def editar_info(self):
        messagebox.showinfo(
            "Información",
            "Panel de control de la institución\n\n"
            "Aquí puede gestionar la información de su institución médica"
        )

    def mostrar_calendario(self):
        messagebox.showinfo(
            title="Calendario",
            message= "Panel de control de la institución\n\n"
            "Aquí puede ver el calendario de su institución médica"
        )