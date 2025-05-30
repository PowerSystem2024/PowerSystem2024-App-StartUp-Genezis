from tkinter import *
from tkinter import messagebox
from controllers import inst_controller


class ConfigInstitucionFrame(Frame):
    def __init__(self, parent, institucion_data, callback_actualizar=None):
        super().__init__(parent)
        self.parent = parent
        self.institucion_data = institucion_data
        self.callback_actualizar = callback_actualizar  # Callback para actualizar el dashboard

        # Variables para los campos principales
        self.nombre_var = StringVar(value=institucion_data.get("nombre", ""))
        self.direccion_var = StringVar(value=institucion_data.get("direccion", ""))
        self.telefono_var = StringVar(value=institucion_data.get("telefono", ""))
        self.email_var = StringVar(value=institucion_data.get("email", ""))
        self.horario_apertura_var = StringVar(value=institucion_data.get("horario_apertura", ""))
        self.horario_cierre_var = StringVar(value=institucion_data.get("horario_cierre", ""))

        self.crear_interfaz()

    def crear_interfaz(self):
        # Frame del formulario
        form_frame = LabelFrame(self, text="Datos Principales", font=('Helvetica', 10, 'bold'))
        form_frame.pack(fill=X, padx=20, pady=10)

        # Campos en 2 columnas para mejor aprovechamiento del espacio
        # Columna izquierda
        left_frame = Frame(form_frame)
        left_frame.grid(row=0, column=0, padx=10, pady=10, sticky='nw')

        Label(left_frame, text="Nombre:", font=('Helvetica', 9, 'bold')).grid(row=0, column=0, sticky='w', pady=5)
        Entry(left_frame, textvariable=self.nombre_var, width=25).grid(row=0, column=1, padx=(5, 0), pady=5)

        Label(left_frame, text="Dirección:", font=('Helvetica', 9, 'bold')).grid(row=1, column=0, sticky='w', pady=5)
        Entry(left_frame, textvariable=self.direccion_var, width=25).grid(row=1, column=1, padx=(5, 0), pady=5)

        Label(left_frame, text="Teléfono:", font=('Helvetica', 9, 'bold')).grid(row=2, column=0, sticky='w', pady=5)
        Entry(left_frame, textvariable=self.telefono_var, width=25).grid(row=2, column=1, padx=(5, 0), pady=5)

        # Columna derecha
        right_frame = Frame(form_frame)
        right_frame.grid(row=0, column=1, padx=10, pady=10, sticky='nw')

        Label(right_frame, text="Email:", font=('Helvetica', 9, 'bold')).grid(row=0, column=0, sticky='w', pady=5)
        Entry(right_frame, textvariable=self.email_var, width=25).grid(row=0, column=1, padx=(5, 0), pady=5)

        Label(right_frame, text="Horario Apertura:", font=('Helvetica', 9, 'bold')).grid(row=1, column=0, sticky='w',
                                                                                         pady=5)
        Entry(right_frame, textvariable=self.horario_apertura_var, width=25).grid(row=1, column=1, padx=(5, 0), pady=5)

        Label(right_frame, text="Horario Cierre:", font=('Helvetica', 9, 'bold')).grid(row=2, column=0, sticky='w',
                                                                                       pady=5)
        Entry(right_frame, textvariable=self.horario_cierre_var, width=25).grid(row=2, column=1, padx=(5, 0), pady=5)

        # Botones
        btn_frame = Frame(self)
        btn_frame.pack(fill=X, pady=20)

        Button(
            btn_frame,
            text="Guardar",
            command=self.guardar_cambios,
            bg='#4CAF50',
            fg='white',
            font=('Helvetica', 9, 'bold'),
            width=12
        ).pack(side=LEFT, padx=(20, 10))

        Button(
            btn_frame,
            text="Cancelar",
            command=self.cancelar,
            bg='#f44336',
            fg='white',
            font=('Helvetica', 9, 'bold'),
            width=12
        ).pack(side=LEFT, padx=10)

    def guardar_cambios(self):
        """Guarda los cambios en la base de datos"""
        # Validación simple
        if not self.nombre_var.get().strip():
            messagebox.showerror("Error", "El nombre es obligatorio")
            return

        if not self.email_var.get().strip():
            messagebox.showerror("Error", "El email es obligatorio")
            return

        try:
            # Preparar datos para actualización
            datos_actualizados = {
                "nombre": self.nombre_var.get().strip(),
                "direccion": self.direccion_var.get().strip(),
                "telefono": self.telefono_var.get().strip(),
                "email": self.email_var.get().strip(),
                "horario_apertura": self.horario_apertura_var.get().strip(),
                "horario_cierre": self.horario_cierre_var.get().strip()
            }

            # Actualizar en la base de datos
            resultado = inst_controller.ActualizarInstitucion(
                self.institucion_data["id"],
                datos_actualizados
            )

            if resultado:
                messagebox.showinfo("Éxito", "Información actualizada correctamente")

                # Llamar al callback para actualizar el dashboard
                if self.callback_actualizar:
                    self.callback_actualizar()
                else:
                    # Si no hay callback, destruir manualmente
                    self.destroy()
            else:
                messagebox.showerror("Error", "No se pudo actualizar la información")

        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar: {str(e)}")

    def cancelar(self):
        """Cancela la edición"""
        self.destroy()