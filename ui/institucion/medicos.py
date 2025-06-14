
import tkinter as tk
from tkinter import ttk, messagebox
from controllers import inst_controller
from controllers.auth_controller import AuthController


class MedicosDashboard(tk.Frame):
    def __init__(self, parent, institucion):
        super().__init__(parent)
        self.parent = parent
        self.institucion = institucion

        # Frame principal
        self.main_frame = ttk.Frame(self, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Crear widgets
        self.crear_widgets()

        # Cargar datos
        self.cargar_datos()

    def crear_widgets(self):
        # Frame para botones
        btn_frame = ttk.Frame(self.main_frame)
        btn_frame.pack(fill=tk.X, pady=10)

        # Botones dentro del btn_frame
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

        # Frame para lista de médicos
        self.lista_frame = ttk.LabelFrame(
            self.main_frame,
            text="Médicos Registrados",
            padding="10"
        )
        self.lista_frame.pack(fill=tk.BOTH, expand=True)

        # TreeView para médicos
        columns = ("#id", "nombre", "apellido", "especialidad", "matricula", "duracion_turno")
        self.tree = ttk.Treeview(
            self.lista_frame,
            columns=columns,
            show='headings'
        )

        # Configurar columnas
        self.tree.heading('nombre', text='Nombre')
        self.tree.heading('apellido', text='Apellido')
        self.tree.heading('especialidad', text='Especialidad')
        self.tree.heading('matricula', text='Matrícula')
        self.tree.heading('duracion_turno', text='Duración Turno')

        # Ocultar la columna del ID
        self.tree.column("#id", width=0, stretch=tk.NO)

        # Ajustar anchos de columna
        self.tree.column('nombre', width=120)
        self.tree.column('apellido', width=120)
        self.tree.column('especialidad', width=150)
        self.tree.column('matricula', width=100)
        self.tree.column('duracion_turno', width=100)

        self.tree.pack(fill=tk.BOTH, expand=True, pady=5)

    def cargar_datos(self):
        try:
            # Limpiar TreeView
            for item in self.tree.get_children():
                self.tree.delete(item)

            # Obtener médicos con información del usuario
            medicos = inst_controller.obtenerMedicosConUsuarios()

            # Filtrar por institución
            medicos_institucion = [
                m for m in medicos
                if m["institucion_id"] == self.institucion["id"]
            ]

            # Insertar en TreeView
            for medico in medicos_institucion:
                usuario = medico.get("usuarios", {})
                nombre = usuario.get("nombre", "N/A") if usuario else "N/A"
                apellido = usuario.get("apellido", "N/A") if usuario else "N/A"

                self.tree.insert("", tk.END, iid=medico["id"], values=(
                    medico["id"],  # El ID se almacena en la primera columna oculta
                    nombre,
                    apellido,
                    medico["especialidad"],
                    medico["matricula"],
                    medico["duracion_turno"]
                ))

        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Error al cargar médicos: {str(e)}"
            )

    def agregar_medico(self):
        dialogo = AgregarMedicoDialog(self.winfo_toplevel())
        self.winfo_toplevel().wait_window(dialogo.dialog)

        if dialogo.resultado:
            try:
                auth_controller = AuthController()
                user_data = {
                    "nombre": dialogo.resultado["nombre"],
                    "apellido": dialogo.resultado["apellido"],
                    "email": dialogo.resultado["email"],
                    "password": dialogo.resultado["password"],
                    "tipo": "medico"
                }

                nuevo_usuario = auth_controller.register(user_data)

                if nuevo_usuario:
                    inst_controller.crearMedico(
                        usuario_id=nuevo_usuario["id"],
                        institucion_id=self.institucion["id"],
                        especialidad=dialogo.resultado["especialidad"],
                        matricula=dialogo.resultado["matricula"],
                        duracion_turno=dialogo.resultado["duracion_turno"]
                    )

                    messagebox.showinfo("Éxito", "Médico agregado correctamente")
                    self.cargar_datos()
                else:
                    messagebox.showerror("Error", "Error al crear el usuario")

            except Exception as e:
                messagebox.showerror("Error", f"Error al agregar médico: {str(e)}")

    def eliminar_medico(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning(
                "Advertencia",
                "Por favor seleccione un médico para eliminar."
            )
            return

        try:
            # Obtener el ID del médico seleccionado
            valores = self.tree.item(seleccion[0], "values")
            medico_id_to_delete = valores[0]

            # Verificar si el médico tiene turnos pendientes
            turnos_pendientes = inst_controller.obtenerTurnosPorMedico(medico_id_to_delete)

            if turnos_pendientes:
                # Si tiene turnos pendientes, mostrar ventana emergente con opciones
                respuesta = messagebox.askyesnocancel(
                    "Médico con turnos pendientes",
                    f"El médico tiene {len(turnos_pendientes)} turno(s) pendiente(s).\n\n"
                    "¿Desea eliminar también todos los turnos asociados?\n\n"
                )

                if respuesta is True:  # Usuario eligió "Sí"
                    # Eliminar primero los turnos del médico
                    inst_controller.eliminarTurnosPorMedico(medico_id_to_delete)
                    # Luego eliminar el médico
                    inst_controller.eliminarMedico(medico_id_to_delete)
                    self.cargar_datos()
                    messagebox.showinfo(
                        "Éxito",
                        "Médico y todos sus turnos eliminados correctamente."
                    )
                elif respuesta is False:  # Usuario eligió "No"
                    messagebox.showinfo(
                        "Operación cancelada",
                        "La eliminación del médico ha sido cancelada."
                    )

            else:
                # Si no tiene turnos pendientes, proceder con eliminación normal
                if messagebox.askyesno(
                        "Confirmar",
                        "¿Está seguro que desea eliminar el médico seleccionado?"
                ):
                    inst_controller.eliminarMedico(medico_id_to_delete)
                    self.cargar_datos()
                    messagebox.showinfo(
                        "Éxito",
                        "Médico eliminado correctamente."
                    )

        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Error al eliminar médico: {str(e)}"
            )


class AgregarMedicoDialog:
    """Diálogo para agregar un nuevo médico"""

    def __init__(self, parent):
        self.resultado = None

        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Agregar Nuevo Médico")
        self.dialog.geometry("400x500")
        self.dialog.resizable(False, False)

        self.dialog.transient(parent)
        self.dialog.grab_set()

        self.crear_widgets()
        self.centrar_ventana()

    def centrar_ventana(self):
        """Centrar la ventana en la pantalla"""
        self.dialog.update_idletasks()
        width = self.dialog.winfo_width()
        height = self.dialog.winfo_height()
        x = (self.dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (height // 2)
        self.dialog.geometry(f"+{x}+{y}")

    def crear_widgets(self):
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(
            main_frame,
            text="Datos del Médico",
            font=('Helvetica', 14, 'bold')
        ).pack(pady=(0, 20))

        form_frame = ttk.Frame(main_frame)
        form_frame.pack(fill=tk.X, pady=10)

        self.nombre_var = tk.StringVar()
        self.apellido_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.especialidad_var = tk.StringVar()
        self.matricula_var = tk.StringVar()
        self.duracion_turno_var = tk.StringVar(value="30")

        # Lista de especialidades médicas
        especialidades = [
            "Cardiología",
            "Dermatología",
            "Endocrinología",
            "Gastroenterología",
            "Ginecología",
            "Medicina General",
            "Medicina Interna",
            "Neurología",
            "Oftalmología",
            "Oncología",
            "Ortopedia",
            "Otorrinolaringología",
            "Pediatría",
            "Psiquiatría",
            "Radiología",
            "Traumatología",
            "Urología"
        ]

        self.entries = {}

        # Crear campos del formulario
        campos = [
            ("Nombre:", self.nombre_var, "entry"),
            ("Apellido:", self.apellido_var, "entry"),
            ("Email:", self.email_var, "entry"),
            ("Contraseña:", self.password_var, "password"),
            ("Especialidad:", self.especialidad_var, "combobox"),
            ("Matrícula:", self.matricula_var, "entry"),
            ("Duración Turno (min):", self.duracion_turno_var, "entry")
        ]

        for i, campo_info in enumerate(campos):
            label_text, var = campo_info[0], campo_info[1]
            tipo_widget = campo_info[2] if len(campo_info) > 2 else "entry"

            ttk.Label(form_frame, text=label_text).grid(
                row=i, column=0, sticky='e', padx=(0, 10), pady=5
            )

            if tipo_widget == "password":
                widget = ttk.Entry(form_frame, textvariable=var, show="*", width=25)
            elif tipo_widget == "combobox" and label_text == "Especialidad:":
                widget = ttk.Combobox(
                    form_frame,
                    textvariable=var,
                    values=especialidades,
                    state="readonly",  # Solo permite seleccionar de la lista
                    width=22
                )
                # Establecer valor por defecto
                widget.set("Medicina General")
            else:
                widget = ttk.Entry(form_frame, textvariable=var, width=25)

            widget.grid(row=i, column=1, sticky='w', pady=5)
            self.entries[label_text] = widget

        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=20)

        ttk.Button(
            btn_frame,
            text="Cancelar",
            command=self.cancelar
        ).pack(side=tk.RIGHT, padx=5)

        ttk.Button(
            btn_frame,
            text="Guardar",
            command=self.guardar
        ).pack(side=tk.RIGHT, padx=5)

        self.entries["Nombre:"].focus()

    def validar_datos(self):
        campos_vacios = []

        if not self.nombre_var.get().strip():
            campos_vacios.append("Nombre")
        if not self.apellido_var.get().strip():
            campos_vacios.append("Apellido")
        if not self.email_var.get().strip():
            campos_vacios.append("Email")
        if not self.password_var.get().strip():
            campos_vacios.append("Contraseña")
        if not self.especialidad_var.get().strip():
            campos_vacios.append("Especialidad")
        if not self.matricula_var.get().strip():
            campos_vacios.append("Matrícula")
        if not self.duracion_turno_var.get().strip():
            campos_vacios.append("Duración Turno")

        if campos_vacios:
            messagebox.showerror(
                "Error de Validación",
                f"Los siguientes campos son obligatorios:\n{', '.join(campos_vacios)}"
            )
            return False

        try:
            duration = int(self.duracion_turno_var.get())
            if duration <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror(
                "Error de Validación",
                "La duración del turno debe ser un número entero positivo."
            )
            return False

        if "@" not in self.email_var.get() or "." not in self.email_var.get():
            messagebox.showerror(
                "Error de Validación",
                "Por favor ingrese un email válido."
            )
            return False

        return True

    def guardar(self):
        if self.validar_datos():
            self.resultado = {
                "nombre": self.nombre_var.get().strip(),
                "apellido": self.apellido_var.get().strip(),
                "email": self.email_var.get().strip(),
                "password": self.password_var.get().strip(),
                "especialidad": self.especialidad_var.get().strip(),
                "matricula": self.matricula_var.get().strip(),
                "duracion_turno": int(self.duracion_turno_var.get())
            }
            self.dialog.destroy()

    def cancelar(self):
        self.dialog.destroy()