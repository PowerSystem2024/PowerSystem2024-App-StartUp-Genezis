import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime  # Importar datetime


class UsersFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.tipo_usuario_filtro = tk.StringVar(value="todos")
        self.setup_ui()
        self.load_users()

    def setup_ui(self):
        # Marco para barra busqueda
        search_frame = tk.Frame(self)
        search_frame.pack(fill=tk.X, padx=10, pady=5)

        # Barra de Busqueda
        search_label = tk.Label(search_frame, text="Buscar:", font=("Arial", 10,))
        search_label.pack(side=tk.LEFT, padx=(0, 5))
        self.search_entry = tk.Entry(search_frame, width=20)
        self.search_entry.pack(side=tk.LEFT, padx=(5))

        # Botón de búsqueda (con lupa)
        search_button = ttk.Button(search_frame, text="🔍 Buscar", command=self.search_users)
        search_button.pack(side=tk.LEFT, padx=5)

        # Filtro
        filtro_frame = tk.Frame(self)
        filtro_frame.pack()
        tk.Label(filtro_frame, text="Filtrar por tipo:").pack(side=tk.LEFT, padx=(20, 5))

        tipo_combo = ttk.Combobox(
            filtro_frame, textvariable=self.tipo_usuario_filtro,
            values=["todos", "paciente", "medico", "institucion", "admin"],
            state="readonly", width=15
        )
        tipo_combo.pack(side=tk.LEFT)
        tipo_combo.bind("<<ComboboxSelected>>", lambda e: self.load_users())

        # Etiqueta para el indicador de carga
        self.loading_label = tk.Label(self, text="Cargando usuarios...", fg="gray", font=("Arial", 10, "italic"))
        # Se packea temporalmente, se mostrará/ocultará en load_users

        # Tabla
        self.tree = ttk.Treeview(self, columns=("nombre", "apellido", "email", "tipo"), show="headings")
        for col, text in [("nombre", "Nombre"), ("apellido", "Apellido"), ("email", "Email"), ("tipo", "Tipo")]:
            self.tree.heading(col, text=text)

        self.tree.bind("<Double-1>", self.show_user_detail)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Botones
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)

        for text, cmd in [("Editar Usuario", self.edit_user),
                           ("Eliminar Usuario", self.delete_user)]:
            tk.Button(btn_frame, text=text, command=cmd).pack(side=tk.LEFT, padx=5)

        self.search_entry.bind("<Return>", lambda e: self.search_users())

    def search_users(self):
        """Método para buscar usuarios según el texto ingresado"""
        search_text = self.search_entry.get().lower().strip()
        tipo_filtro = self.tipo_usuario_filtro.get()

        self.tree.delete(*self.tree.get_children())
        self.loading_label.pack(pady=5)  # Mostrar indicador de carga
        self.update_idletasks()  # Actualizar la UI para que se vea el label

        usuarios = self.controller.obtener_usuarios()

        self.loading_label.pack_forget()  # Ocultar indicador de carga

        if usuarios:
            for user in usuarios:
                matches_search = (
                        search_text in user.get("nombre", "").lower() or
                        search_text in user.get("apellido", "").lower() or
                        search_text in user.get("email", "").lower()
                )

                matches_filter = (
                        tipo_filtro == "todos" or
                        user.get("tipo") == tipo_filtro
                )

                if matches_search and matches_filter:
                    values = (
                        user.get("nombre"),
                        user.get("apellido"),
                        user.get("email"),
                        user.get("tipo")
                    )
                    self.tree.insert("", "end", values=values, tags=(user.get("id"),))

    def load_users(self):
        """Carga los usuarios en el Treeview, aplicando el filtro de tipo."""
        self.tree.delete(*self.tree.get_children())
        self.loading_label.pack(pady=5)  # Mostrar indicador de carga
        self.update_idletasks()  # Actualizar la UI para que se vea el label

        usuarios = self.controller.obtener_usuarios()

        self.loading_label.pack_forget()  # Ocultar indicador de carga

        if usuarios:
            tipo_filtro = self.tipo_usuario_filtro.get()
            for user in usuarios:
                if tipo_filtro == "todos" or user.get("tipo") == tipo_filtro:
                    values = (user.get("nombre"), user.get("apellido"), user.get("email"), user.get("tipo"))
                    self.tree.insert("", "end", values=values, tags=(user.get("id"),))

    def get_selected_user_id(self):
        selected = self.tree.selection()
        return self.tree.item(selected[0])["tags"][0] if selected else None

    def edit_user(self):
        """
        Método 'despachador'. Revisa el tipo de usuario y llama al formulario correcto.
        """
        user_id = self.get_selected_user_id()
        if not user_id:
            messagebox.showwarning("Aviso", "Selecciona un usuario para editar.")
            return

        values = self.tree.item(self.tree.selection()[0])["values"]
        user_tipo = values[3]  # El tipo ahora está en el índice 3, ya que se agregó 'apellido' en el índice 1

        user_data = {
            "id": user_id,
            "nombre": values[0],
            "apellido": values[1],
            "email": values[2],
            "tipo": user_tipo
        }

        if user_tipo == "institucion":
            self.open_institution_edit_form(user_data)
        elif user_tipo == "paciente":
            self.editar_paciente(user_data)  # Cambiado a usar editar_paciente
        elif user_tipo == "medico":
            self.editar_medico(user_data)  # Usando el método existente
        else:
            # Para tipos de usuario genéricos como 'admin'
            messagebox.showinfo("Información", "La edición de este tipo de usuario no está implementada.")

    def delete_user(self):
        user_id = self.get_selected_user_id()
        if not user_id:
            messagebox.showwarning("Aviso", "Selecciona un usuario para eliminar.")
            return

        if messagebox.askyesno("Confirmar", "¿Eliminar este usuario?"):
            try:
                self.controller.borrar_usuario(user_id)
                messagebox.showinfo("Éxito", "Usuario eliminado correctamente.", parent=self)
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar el usuario: {e}", parent=self)
            self.load_users()

    def open_institution_edit_form(self, user_data):
        info_institucion = self.controller.obtener_info_institucion(user_data['id'])
        if not info_institucion or not isinstance(info_institucion, list) or not info_institucion[0]:
            messagebox.showerror("Error",
                                 "No se pudo cargar la información detallada de la institución o los datos son inválidos.")
            return

        detalle_institucion = info_institucion[0]
        institucion_id_db = detalle_institucion.get("id")

        form = tk.Toplevel(self)
        form.title(f"Editando Institución: {user_data.get('nombre', '')}")
        form.geometry("450x480")
        form.resizable(False, False)
        form.configure(padx=15, pady=15)

     #contenedor principal
        main_frame = ttk.Frame(form)
        main_frame.pack(fill=tk.BOTH, expand=True)

        datos_frame = ttk.LabelFrame(main_frame, text=" Datos de la Institución ", padding=(10, 5))
        datos_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        datos_frame.columnconfigure(1, weight=1)

        fields = {}
        field_configs = [
            ("nombre", "Nombre:", detalle_institucion.get("nombre")),
            ("direccion", "Dirección:", detalle_institucion.get("direccion")),
            ("telefono", "Teléfono:", detalle_institucion.get("telefono")),
            ("email", "Email:", detalle_institucion.get("email")),
            ("descripcion", "Descripción:", detalle_institucion.get("descripcion")),
            ("horario_apertura", "Apertura:", detalle_institucion.get("horario_apertura")),
            ("horario_cierre", "Cierre:", detalle_institucion.get("horario_cierre"))
        ]

        for i, (field, label, initial_value) in enumerate(field_configs):
            ttk.Label(datos_frame, text=label).grid(row=i, column=0, sticky="w", padx=5, pady=5)
            entry = ttk.Entry(datos_frame)
            entry.grid(row=i, column=1, sticky="ew", padx=5, pady=5)
            if initial_value:
                entry.insert(0, initial_value)
            fields[field] = entry

        # --- Sección 2: Cambiar Contraseña ---
        pass_frame = ttk.LabelFrame(main_frame, text=" Cambiar Contraseña (Opcional) ", padding=(10, 5))
        pass_frame.grid(row=1, column=0, sticky="ew")
        pass_frame.columnconfigure(1, weight=1)

        password_fields = {}
        password_configs = [
            ("nueva_password", "Nueva Contraseña:"),
            ("confirmar_password", "Confirmar Contraseña:")
        ]

        for i, (field, label) in enumerate(password_configs):
            ttk.Label(pass_frame, text=label).grid(row=i, column=0, sticky="w", padx=5, pady=5)
            entry = ttk.Entry(pass_frame, show="*")
            entry.grid(row=i, column=1, sticky="ew", padx=5, pady=5)
            password_fields[field] = entry

        # --- Botón de Guardado ---
        save_button = ttk.Button(main_frame, text="Guardar Cambios")
        save_button.grid(row=2, column=0, pady=(20, 0))

        def submit():
            # 1. Guardar datos de la institución
            nuevos_datos = {field: entry.get().strip() for field, entry in fields.items()}
            try:
                self.controller.actualizar_institucion(institucion_id_db, nuevos_datos)
            except Exception as e:
                messagebox.showerror("Error de Actualización", f"No se pudo guardar los datos de la institución:\n{e}",
                                     parent=form)
                return

            # 2. Manejar la actualización de contraseña
            nueva_pass = password_fields["nueva_password"].get().strip()
            confirmar_pass = password_fields["confirmar_password"].get().strip()
            password_updated_successfully = False

            if nueva_pass:
                if nueva_pass != confirmar_pass:
                    messagebox.showwarning("Contraseñas no coinciden", "Las contraseñas ingresadas no son iguales.",
                                           parent=form)
                    return

                try:
                    usuario_id = user_data['id']
                    self.controller.admin_actualizar_password_usuario(usuario_id, nueva_pass)
                    password_updated_successfully = True
                except Exception as e:
                    messagebox.showerror("Error de Contraseña", f"No se pudo actualizar la contraseña:\n{e}",
                                         parent=form)
                    return

            # 3. Mostrar mensaje final y cerrar
            if password_updated_successfully:
                messagebox.showinfo("Éxito", "Datos de la institución y contraseña actualizados correctamente.",
                                     parent=form)
            else:
                messagebox.showinfo("Éxito", "Datos de la institución actualizados.", parent=form)

            form.destroy()
            self.load_users()

        save_button.config(command=submit)

    def editar_paciente(self, user_data):
        info_paciente = self.controller.obtener_info_paciente(user_data['id'])
        if not info_paciente or not isinstance(info_paciente, list) or not info_paciente[0]:
            messagebox.showerror("Error",
                                 "No se pudo cargar la información detallada del paciente o los datos son inválidos.")
            return

        detalle_paciente = info_paciente[0]
        paciente_id_db = detalle_paciente.get("id")

        form = tk.Toplevel(self)
        form.title(f"Editando Paciente: {user_data.get('nombre', '')}")
        form.geometry("450x500")
        form.resizable(False, False)
        form.configure(padx=15, pady=15)

        main_frame = ttk.Frame(form)
        main_frame.pack(fill=tk.BOTH, expand=True)

        datos_frame = ttk.LabelFrame(main_frame, text=" Datos del Paciente ", padding=(10, 5))
        datos_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        datos_frame.columnconfigure(1, weight=1)

        fields = {}
        field_configs = [
            ("nombre", "Nombre:", user_data.get("nombre"), "entry"),
            ("apellido", "Apellido:", user_data.get("apellido"), "entry"),
            ("email", "Email:", user_data.get("email"), "entry"),
            ("telefono", "Teléfono:", detalle_paciente.get("telefono"), "entry"),
            ("fecha_nacimiento", "F. Nacimiento (YYYY-MM-DD):", detalle_paciente.get("fecha_nacimiento"), "dateentry"),
            ("genero", "Género:", detalle_paciente.get("genero"), "combobox", ["Masculino", "Femenino", "Otro"]),
            ("obra_social", "Obra Social:", detalle_paciente.get("obra_social"), "entry"),
            ("num_afiliado", "N° Afiliado:", detalle_paciente.get("num_afiliado"), "entry")
        ]

        for i, (field, label, initial_value, widget_type, *args) in enumerate(field_configs):
            ttk.Label(datos_frame, text=label).grid(row=i, column=0, sticky="w", padx=5, pady=5)
            if widget_type == "dateentry":
                entry = DateEntry(datos_frame, width=12, background='darkblue',
                                  foreground='white', borderwidth=2, year=2000, date_pattern='yyyy-mm-dd')
                entry.grid(row=i, column=1, sticky="ew", padx=5, pady=5)
                if initial_value:
                    try:
                        entry.set_date(datetime.strptime(initial_value, '%Y-%m-%d').date())
                    except ValueError:
                        pass
            elif widget_type == "combobox":
                combo_values = args[0]
                entry_var = tk.StringVar(value=initial_value if initial_value else "")
                entry = ttk.Combobox(datos_frame, textvariable=entry_var, values=combo_values, state="readonly")
                entry.grid(row=i, column=1, sticky="ew", padx=5, pady=5)
                fields[f"{field}_var"] = entry_var
            else:  # "entry"
                entry = ttk.Entry(datos_frame)
                entry.grid(row=i, column=1, sticky="ew", padx=5, pady=5)
                if initial_value:
                    entry.insert(0, initial_value)
            fields[field] = entry

        pass_frame = ttk.LabelFrame(main_frame, text=" Cambiar Contraseña (Opcional) ", padding=(10, 5))
        pass_frame.grid(row=1, column=0, sticky="ew")
        pass_frame.columnconfigure(1, weight=1)

        password_fields = {}
        password_configs = [
            ("nueva_password", "Nueva Contraseña:"),
            ("confirmar_password", "Confirmar Contraseña:")
        ]

        for i, (field, label) in enumerate(password_configs):
            ttk.Label(pass_frame, text=label).grid(row=i, column=0, sticky="w", padx=5, pady=5)
            entry = ttk.Entry(pass_frame, show="*")
            entry.grid(row=i, column=1, sticky="ew", padx=5, pady=5)
            password_fields[field] = entry

        save_button = ttk.Button(main_frame, text="Guardar Cambios")
        save_button.grid(row=2, column=0, pady=(20, 0))

        def submit():
            nuevos_datos_usuario = {
                "nombre": fields["nombre"].get().strip(),
                "apellido": fields["apellido"].get().strip(),
                "email": fields["email"].get().strip()
            }
            fecha_nacimiento_val = fields["fecha_nacimiento"].get_date().strftime('%Y-%m-%d') if isinstance(
                fields["fecha_nacimiento"], DateEntry) else fields["fecha_nacimiento"].get().strip()

            nuevos_datos_paciente = {
                "telefono": fields["telefono"].get().strip(),
                "fecha_nacimiento": fecha_nacimiento_val,
                "genero": fields["genero_var"].get().strip() if "genero_var" in fields else "",
                "obra_social": fields["obra_social"].get().strip(),
                "num_afiliado": fields["num_afiliado"].get().strip(),
            }

            try:
                self.controller.actualizar_usuario(user_data['id'], nuevos_datos_usuario)
                self.controller.actualizar_paciente(paciente_id_db, nuevos_datos_paciente)
            except Exception as e:
                messagebox.showerror("Error de Actualización", f"No se pudo guardar los datos del paciente:\n{e}",
                                     parent=form)
                return

            nueva_pass = password_fields["nueva_password"].get().strip()
            confirmar_pass = password_fields["confirmar_password"].get().strip()
            password_updated_successfully = False

            if nueva_pass:
                if nueva_pass != confirmar_pass:
                    messagebox.showwarning("Contraseñas no coinciden", "Las contraseñas ingresadas no son iguales.",
                                           parent=form)
                    return

                try:
                    usuario_id = user_data['id']
                    self.controller.admin_actualizar_password_usuario(usuario_id, nueva_pass)
                    password_updated_successfully = True
                except Exception as e:
                    messagebox.showerror("Error de Contraseña", f"No se pudo actualizar la contraseña:\n{e}",
                                         parent=form)
                    return

            if password_updated_successfully:
                messagebox.showinfo("Éxito", "Datos del paciente y contraseña actualizados correctamente.",
                                     parent=form)
            else:
                messagebox.showinfo("Éxito", "Datos del paciente actualizados.", parent=form)

            form.destroy()
            self.load_users()

        save_button.config(command=submit)

    def editar_medico(self, user_data):
        # Lista de especialidades médicas hardcodeadas
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

        info_medico = self.controller.obtener_info_completa_medico(user_data['id'])
        if not info_medico or not isinstance(info_medico, list) or not info_medico[0]:
            messagebox.showerror("Error",
                                 "No se pudo cargar la información detallada del médico o los datos son inválidos.")
            return

        detalle_medico = info_medico[0]
        medico_id_db = detalle_medico.get("id")

        form = tk.Toplevel(self)
        form.title(f"Editando Médico: {user_data.get('nombre', '')}")
        form.geometry("450x600")
        form.resizable(False, False)
        form.configure(padx=15, pady=15)

        main_frame = ttk.Frame(form)
        main_frame.pack(fill=tk.BOTH, expand=True)

        datos_frame = ttk.LabelFrame(main_frame, text=" Datos del Médico ", padding=(10, 5))
        datos_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        datos_frame.columnconfigure(1, weight=1)

        fields = {}
        # field_configs para los campos de entrada de texto
        field_configs_entries = [
            ("nombre", "Nombre:", user_data.get("nombre")),
            ("apellido", "Apellido:", user_data.get("apellido")),
            ("email", "Email:", user_data.get("email")),
            ("matricula", "Matrícula:", detalle_medico.get("matricula")),
            ("duracion_turno", "Duración Turno (min):", detalle_medico.get("duracion_turno")),
        ]

        # Agregar los campos de entrada de texto
        for i, (field, label, initial_value) in enumerate(field_configs_entries):
            ttk.Label(datos_frame, text=label).grid(row=i, column=0, sticky="w", padx=5, pady=5)
            entry = ttk.Entry(datos_frame)
            entry.grid(row=i, column=1, sticky="ew", padx=5, pady=5)
            if initial_value is not None:
                entry.insert(0, initial_value)
            fields[field] = entry

        # Campo de Especialidad (Combobox)
        row_especialidad = len(field_configs_entries) # Determinar la fila para la especialidad
        ttk.Label(datos_frame, text="Especialidad:").grid(row=row_especialidad, column=0, sticky="w", padx=5, pady=5)
        especialidad_var = tk.StringVar(value=detalle_medico.get("especialidad", ""))
        especialidad_combo = ttk.Combobox(datos_frame, textvariable=especialidad_var, values=especialidades, state="readonly")
        especialidad_combo.grid(row=row_especialidad, column=1, sticky="ew", padx=5, pady=5)
        fields["especialidad_var"] = especialidad_var


        # Campo de institución (combobox)
        instituciones = self.controller.obtener_instituciones()
        institucion_options = ["(Ninguna)"]
        institucion_map = {"(Ninguna)": None}
        current_institucion_id = detalle_medico.get("institucion_id")
        current_institucion_name = "(Ninguna)"

        if instituciones:
            for inst in instituciones:
                institucion_options.append(inst.get("nombre"))
                institucion_map[inst.get("nombre")] = inst.get("id")
                if inst.get("id") == current_institucion_id:
                    current_institucion_name = inst.get("nombre")

        tk.Label(datos_frame, text="Institución (Opcional):", font=("Arial", 10)).grid(row=row_especialidad + 1, column=0,
                                                                                       sticky="w", padx=5, pady=5)
        institucion_med_var = tk.StringVar(value=current_institucion_name)
        institucion_med_combo = ttk.Combobox(datos_frame, textvariable=institucion_med_var, values=institucion_options,
                                              state="readonly")
        institucion_med_combo.grid(row=row_especialidad + 1, column=1, sticky="ew", padx=5, pady=5)
        fields["institucion_id_var"] = institucion_med_var  # Almacenar para obtener el valor
        fields["institucion_map"] = institucion_map  # Necesario para la conversión de nombre a ID

        pass_frame = ttk.LabelFrame(main_frame, text=" Cambiar Contraseña (Opcional) ", padding=(10, 5))
        pass_frame.grid(row=1, column=0, sticky="ew")
        pass_frame.columnconfigure(1, weight=1)

        password_fields = {}
        password_configs = [
            ("nueva_password", "Nueva Contraseña:"),
            ("confirmar_password", "Confirmar Contraseña:")
        ]

        for i, (field, label) in enumerate(password_configs):
            ttk.Label(pass_frame, text=label).grid(row=i, column=0, sticky="w", padx=5, pady=5)
            entry = ttk.Entry(pass_frame, show="*")
            entry.grid(row=i, column=1, sticky="ew", padx=5, pady=5)
            password_fields[field] = entry

        save_button = ttk.Button(main_frame, text="Guardar Cambios")
        save_button.grid(row=2, column=0, pady=(20, 0))

        def submit():
            nuevos_datos_usuario = {
                "nombre": fields["nombre"].get().strip(),
                "apellido": fields["apellido"].get().strip(),
                "email": fields["email"].get().strip()
            }

            institucion_nombre_seleccionada = fields["institucion_id_var"].get()
            institucion_id_para_db = fields["institucion_map"].get(institucion_nombre_seleccionada)

            duracion_turno_val = fields["duracion_turno"].get().strip()
            try:
                duracion_turno_val = int(duracion_turno_val) if duracion_turno_val else None
            except ValueError:
                messagebox.showwarning("Formato Inválido", "La duración del turno debe ser un número entero.",
                                       parent=form)
                return

            nuevos_datos_medico = {
                "especialidad": fields["especialidad_var"].get().strip(), # Obtener valor del Combobox
                "matricula": fields["matricula"].get().strip(),
                "institucion_id": institucion_id_para_db,
                "duracion_turno": duracion_turno_val,
            }

            try:
                self.controller.actualizar_usuario(user_data['id'], nuevos_datos_usuario)
                self.controller.actualizar_medico(medico_id_db, nuevos_datos_medico)
            except Exception as e:
                messagebox.showerror("Error de Actualización", f"No se pudo guardar los datos del médico:\n{e}",
                                     parent=form)
                return

            nueva_pass = password_fields["nueva_password"].get().strip()
            confirmar_pass = password_fields["confirmar_password"].get().strip()
            password_updated_successfully = False

            if nueva_pass:
                if nueva_pass != confirmar_pass:
                    messagebox.showwarning("Contraseñas no coinciden", "Las contraseñas ingresadas no son iguales.",
                                           parent=form)
                    return

                try:
                    usuario_id = user_data['id']
                    self.controller.admin_actualizar_password_usuario(usuario_id, nueva_pass)
                    password_updated_successfully = True
                except Exception as e:
                    messagebox.showerror("Error de Contraseña", f"No se pudo actualizar la contraseña:\n{e}",
                                         parent=form)
                    return

            if password_updated_successfully:
                messagebox.showinfo("Éxito", "Datos del médico y contraseña actualizados correctamente.",
                                     parent=form)
            else:
                messagebox.showinfo("Éxito", "Datos del médico actualizados.", parent=form)

            form.destroy()
            self.load_users()

        save_button.config(command=submit)

    def show_user_detail(self, event=None):
        selected = self.tree.selection()
        if not selected:
            return

        values = self.tree.item(selected[0])["values"]
        user_id = self.tree.item(selected[0])["tags"][0]
        user_tipo = values[3]

        detail = tk.Toplevel(self)
        detail.title("Detalles del Usuario")
        detail.geometry("500x400")

        info_frame = tk.LabelFrame(detail, text="Información Básica", font=("Arial", 10, "bold"))
        info_frame.pack(fill=tk.X, padx=10, pady=5)
        for label, value in [("Nombre", values[0]), ("Apellido", values[1]), ("Email", values[2]),
                             ("Tipo", values[3].capitalize())]:
            tk.Label(info_frame, text=f"{label}: {value}", anchor="w").pack(fill=tk.X, padx=5, pady=1)

        content_frame = tk.Frame(detail)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        if user_tipo == "medico":
            self.show_medico_details(content_frame, user_id)
        elif user_tipo == "paciente":
            self.show_paciente_details(content_frame, user_id)
        elif user_tipo == "institucion":
            self.show_institucion_details(content_frame, user_id)

    # --- MÉTODOS PARA MOSTRAR DETALLES ---

    def show_medico_details(self, parent, user_id):
        medico_info = self.controller.obtener_info_completa_medico(user_id)
        if not medico_info:
            tk.Label(parent, text="Sin información adicional del médico.", fg="gray").pack(pady=10)
            return
        medico_data = medico_info[0] if medico_info and isinstance(medico_info, list) and isinstance(medico_info[0],
                                                                                                     dict) else {}

        if not medico_data:
            tk.Label(parent, text="No se pudieron cargar los detalles del médico o el formato es incorrecto.",
                     fg="red").pack(pady=10)
            return

        prof_frame = tk.LabelFrame(parent, text="Información Profesional")
        prof_frame.pack(fill=tk.X, pady=5)

        prof_data = [
            ("Especialidad", medico_data.get('especialidad')),
            ("Matrícula", medico_data.get('matricula')),
            # Acceder de forma segura a 'nombre' de 'institucion'
            ("Institución", medico_data.get('institucion', {}).get('nombre', "N/A")),
            ("Duración turno", medico_data.get('duracion_turno'))
        ]
        for label, value in prof_data:
            if value is not None:
                tk.Label(prof_frame, text=f"{label}: {value}", anchor="w").pack(fill=tk.X, padx=5, pady=1)

    def show_paciente_details(self, parent, user_id):
        self._show_user_specific_details(parent, user_id, "paciente", "obtener_info_paciente",
                                         [("Teléfono", "telefono"),
                                          ("Fecha nacimiento", "fecha_nacimiento"),
                                          ("Género", "genero"),
                                          ("Obra Social", "obra_social"),
                                          ("N° Afiliado", "num_afiliado")])

    def show_institucion_details(self, parent, user_id):
        self._show_user_specific_details(parent, user_id, "institución", "obtener_info_institucion",
                                         [("Dirección", "direccion"),
                                          ("Teléfono", "telefono"),
                                          ("Tipo", "tipo_institucion")])

    def _show_user_specific_details(self, parent, user_id, tipo_label, method_name, fields):
        info = getattr(self.controller, method_name)(user_id)

        # Validación mejorada de los datos recibidos
        if not info or not isinstance(info, list) or not info[0] or not isinstance(info[0], dict):
            tk.Label(parent, text=f"Sin información adicional del {tipo_label} o los datos son inválidos.",
                     fg="gray").pack(pady=10)
            return

        data = info[0]

        info_frame = tk.LabelFrame(parent, text=f"Información del {tipo_label.title()}")
        info_frame.pack(fill=tk.X, pady=5)
        for label, field_key in fields:
            value = data.get(field_key)
            if value is not None and value != '':
                tk.Label(info_frame, text=f"{label}: {value}", anchor="w").pack(fill=tk.X, padx=5, pady=1)