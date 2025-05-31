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

        # Frame para botones
        btn_frame = ttk.Frame(self.main_frame)
        btn_frame.pack(fill=tk.X, pady=10)

        # Botones
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
                if m["institucion_id"] == self.institucion["id"]  # Usar el ID de la institución
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

    def agregar_medico(self):
        """Abre el diálogo para agregar un nuevo médico"""
        dialogo = AgregarMedicoDialog(self.parent)
        self.parent.wait_window(dialogo.dialog)

        if dialogo.resultado:
            try:
                # Crear usuario primero
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
                    # Crear médico con el ID del usuario creado
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
                "Por favor seleccione un médico"
            )
            return

        if messagebox.askyesno(
                "Confirmar",
                "¿Está seguro que desea eliminar el médico seleccionado?"
        ):
            try:
                medico_id = self.tree.item(seleccion[0])["values"][0]
                inst_controller.eliminarMedico(medico_id)
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

class AgregarMedicoDialog:
    """Diálogo para agregar un nuevo médico"""

    def __init__(self, parent):
        self.resultado = None

        # Crear ventana de diálogo
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Agregar Nuevo Médico")
        self.dialog.geometry("400x500")
        self.dialog.resizable(False, False)

        # Hacer la ventana modal
        self.dialog.transient(parent)
        self.dialog.grab_set()

        # Centrar la ventana
        self.centrar_ventana()

        # Crear widgets
        self.crear_widgets()

    def centrar_ventana(self):
        """Centrar la ventana en la pantalla"""
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (500 // 2)
        self.dialog.geometry(f"400x500+{x}+{y}")

    def crear_widgets(self):
        # Frame principal
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Título
        ttk.Label(
            main_frame,
            text="Datos del Médico",
            font=('Helvetica', 14, 'bold')
        ).pack(pady=(0, 20))

        # Frame para formulario
        form_frame = ttk.Frame(main_frame)
        form_frame.pack(fill=tk.X, pady=10)

        # Variables de entrada
        self.nombre_var = tk.StringVar()
        self.apellido_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.especialidad_var = tk.StringVar()
        self.matricula_var = tk.StringVar()
        self.duracion_turno_var = tk.StringVar(value="30")  # valor por defecto

        # Campos del formulario
        campos = [
            ("Nombre:", self.nombre_var),
            ("Apellido:", self.apellido_var),
            ("Email:", self.email_var),
            ("Contraseña:", self.password_var),
            ("Especialidad:", self.especialidad_var),
            ("Matrícula:", self.matricula_var),
            ("Duración Turno (min):", self.duracion_turno_var)
        ]

        self.entries = {}

        for i, (label_text, var) in enumerate(campos):
            # Label
            ttk.Label(form_frame, text=label_text).grid(
                row=i, column=0, sticky='e', padx=(0, 10), pady=5
            )

            # Entry
            if label_text == "Contraseña:":
                entry = ttk.Entry(form_frame, textvariable=var, show="*", width=25)
            else:
                entry = ttk.Entry(form_frame, textvariable=var, width=25)

            entry.grid(row=i, column=1, sticky='w', pady=5)
            self.entries[label_text] = entry

        # Frame para botones
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=20)

        # Botones
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

        # Enfocar el primer campo
        self.entries["Nombre:"].focus()

    def validar_datos(self):
        """Validar que todos los campos estén llenos"""
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

        # Validar que la duración del turno sea un número
        try:
            int(self.duracion_turno_var.get())
        except ValueError:
            messagebox.showerror(
                "Error de Validación",
                "La duración del turno debe ser un número válido"
            )
            return False

        return True

    def guardar(self):
        """Guardar los datos del médico"""
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
        """Cancelar la operación"""
        self.dialog.destroy()