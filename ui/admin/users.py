# ui/admin/users.py

import tkinter as tk
from tkinter import ttk, messagebox


class UsersFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.tipo_usuario_filtro = tk.StringVar(value="todos")
        self.setup_ui()
        self.load_users()

    def setup_ui(self):
        # Título
        tk.Label(self, text="Gestión de Usuarios", font=("Arial", 14, "bold")).pack(pady=10)

        # Filtro
        filtro_frame = tk.Frame(self)
        filtro_frame.pack()
        tk.Label(filtro_frame, text="Filtrar por tipo:").pack(side=tk.LEFT, padx=5)

        tipo_combo = ttk.Combobox(
            filtro_frame, textvariable=self.tipo_usuario_filtro,
            values=["todos", "paciente", "medico", "institucion", "admin"],
            state="readonly", width=15
        )
        tipo_combo.pack(side=tk.LEFT)
        tipo_combo.bind("<<ComboboxSelected>>", lambda e: self.load_users())

        # Tabla
        self.tree = ttk.Treeview(self, columns=("nombre", "email", "tipo"), show="headings")
        for col, text in [("nombre", "Nombre"), ("email", "Email"), ("tipo", "Tipo")]:
            self.tree.heading(col, text=text)

        self.tree.bind("<Double-1>", self.show_user_detail)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Botones
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)

        for text, cmd in [("Crear Usuario", self.create_user),
                          ("Editar Usuario", self.edit_user),
                          ("Eliminar Usuario", self.delete_user)]:

            tk.Button(btn_frame, text=text, command=cmd).pack(side=tk.LEFT, padx=5)

    def load_users(self):
        self.tree.delete(*self.tree.get_children())
        usuarios = self.controller.obtener_usuarios()

        if usuarios:
            tipo_filtro = self.tipo_usuario_filtro.get()
            for user in usuarios:
                if tipo_filtro == "todos" or user.get("tipo") == tipo_filtro:
                    values = (user.get("nombre"), user.get("email"), user.get("tipo"))
                    self.tree.insert("", "end", values=values, tags=(user.get("id"),))

    def get_selected_user_id(self):
        selected = self.tree.selection()
        return self.tree.item(selected[0])["tags"][0] if selected else None

    def create_user(self):
        self.open_user_form()

    def edit_user(self):
        """
        Método 'despachador'. Revisa el tipo de usuario y llama al formulario correcto.
        """
        user_id = self.get_selected_user_id()
        if not user_id:
            messagebox.showwarning("Aviso", "Selecciona un usuario para editar.")
            return

        values = self.tree.item(self.tree.selection()[0])["values"]
        user_tipo = values[2]

        user_data = {
            "id": user_id,
            "nombre": values[0],
            "email": values[1],
            "tipo": user_tipo
        }

        if user_tipo == "institucion":
            self.open_institution_edit_form(user_data)
        else:
            self.open_user_form(user_id, user_data)

    def delete_user(self):
        user_id = self.get_selected_user_id()
        if not user_id:
            messagebox.showwarning("Aviso", "Selecciona un usuario para eliminar.")
            return

        if messagebox.askyesno("Confirmar", "¿Eliminar este usuario?"):
            self.controller.borrar_usuario(user_id)
            self.load_users()

    def open_user_form(self, user_id=None, user_data=None):
        """
        # MÉTODO REESTRUCTURADO: Ahora solo maneja usuarios genéricos (paciente, medico, admin).
        # Su lógica está completamente separada de la de instituciones.
        """
        form = tk.Toplevel(self)
        form.title("Formulario de Usuario")
        form.geometry("300x280")

        fields = {}
        field_configs = [
            ("nombre", "Nombre", False),
            ("apellido", "Apellido", False),
            ("email", "Email", False),
            ("password", "Contraseña", True)
        ]

        for field, label, is_password in field_configs:
            tk.Label(form, text=label).pack(pady=2)
            entry = tk.Entry(form, show="*" if is_password else "")
            entry.pack(pady=2)
            fields[field] = entry

        tk.Label(form, text="Tipo").pack(pady=2)
        tipo_var = tk.StringVar()
        tipo_combo = ttk.Combobox(
            form, textvariable=tipo_var,
            values=["paciente", "medico", "admin"], # Quitamos 'institucion' para evitar confusiones
            state="readonly"
        )
        tipo_combo.pack(pady=2)

        if user_data:
            for field in ["nombre", "apellido", "email"]:
                if field in fields and user_data.get(field):
                    fields[field].insert(0, user_data.get(field))
            tipo_var.set(user_data.get("tipo", ""))
            fields["password"].configure(state="disabled")

        def submit():
            data = {field: entry.get().strip() for field, entry in fields.items()}
            data["tipo"] = tipo_var.get().strip()

            required = ["nombre", "apellido", "email", "tipo"]
            if not user_id: required.append("password")

            if not all(data.get(field) for field in required):
                messagebox.showwarning("Error", "Completa todos los campos obligatorios.", parent=form)
                return

            if user_id:
                del data["password"]
                self.controller.actualizar_usuario(user_id, data)
            else:
                self.controller.crear_usuario(data["email"], data["password"], data["tipo"], data["nombre"], data["apellido"])

            form.destroy()
            self.load_users()

        tk.Button(form, text="Guardar", command=submit).pack(pady=15)

    def open_institution_edit_form(self, user_data):
        """
        # MÉTODO NUEVO Y CORREGIDO: Ahora es un método de la clase, no está anidado.
        # Se dedica exclusivamente a editar una institución.
        # NOTA: La indentación aquí es crucial. Está al mismo nivel que los otros métodos.
        """
        info_institucion = self.controller.obtener_info_institucion(user_data['id'])
        if not info_institucion or not isinstance(info_institucion, list):
            messagebox.showerror("Error", "No se pudo cargar la información detallada de la institución.")
            return

        detalle_institucion = info_institucion[0]
        institucion_id_db = detalle_institucion.get("id")

        form = tk.Toplevel(self)
        form.title(f"Editando Institución: {user_data.get('nombre', '')}")
        form.geometry("400x450")

        fields = {}
        field_configs = [
            ("nombre", "Nombre", detalle_institucion.get("nombre")),
            ("direccion", "Dirección", detalle_institucion.get("direccion")),
            ("telefono", "Teléfono", detalle_institucion.get("telefono")),
            ("email", "Email", detalle_institucion.get("email")),
            ("descripcion", "Descripción", detalle_institucion.get("descripcion")),
            ("horario_apertura", "Apertura (HH:MM)", detalle_institucion.get("horario_apertura")),
            ("horario_cierre", "Cierre (HH:MM)", detalle_institucion.get("horario_cierre"))
        ]

        for field, label, initial_value in field_configs:
            frame = tk.Frame(form)
            frame.pack(fill=tk.X, padx=10, pady=5)
            tk.Label(frame, text=label, width=15, anchor='w').pack(side=tk.LEFT)
            entry = tk.Entry(frame)
            entry.pack(side=tk.RIGHT, expand=True, fill=tk.X)
            if initial_value:
                entry.insert(0, initial_value)
            fields[field] = entry

        def submit():
            """La lógica de guardado específica para este formulario."""
            nuevos_datos = {field: entry.get().strip() for field, entry in fields.items()}

            if not all([nuevos_datos.get("nombre"), nuevos_datos.get("email"), nuevos_datos.get("direccion")]):
                messagebox.showwarning("Campos incompletos", "Nombre, Email y Dirección son obligatorios.", parent=form)
                return

            try:
                self.controller.actualizar_institucion(institucion_id_db, nuevos_datos)
                messagebox.showinfo("Éxito", "Institución actualizada correctamente.", parent=form)
                form.destroy()
                self.load_users()
            except Exception as e:
                messagebox.showerror("Error de Actualización", f"No se pudo guardar la institución:\n{e}", parent=form)

        tk.Button(form, text="Guardar Cambios", command=submit).pack(pady=20)


    def show_user_detail(self, event=None):
        selected = self.tree.selection()
        if not selected:
            return

        values = self.tree.item(selected[0])["values"]
        user_id = self.tree.item(selected[0])["tags"][0]
        user_tipo = values[2]

        detail = tk.Toplevel(self)
        detail.title("Detalles del Usuario")
        detail.geometry("500x400")

        info_frame = tk.LabelFrame(detail, text="Información Básica", font=("Arial", 10, "bold"))
        info_frame.pack(fill=tk.X, padx=10, pady=5)
        for label, value in [("Nombre", values[0]), ("Email", values[1]), ("Tipo", values[2].capitalize())]:
            tk.Label(info_frame, text=f"{label}: {value}", anchor="w").pack(fill=tk.X, padx=5, pady=1)

        content_frame = tk.Frame(detail)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        if user_tipo == "medico":
            self.show_medico_details(content_frame, user_id)
        elif user_tipo == "paciente":
            self.show_paciente_details(content_frame, user_id)
        elif user_tipo == "institucion":
            self.show_institucion_details(content_frame, user_id)

    # --- MÉTODOS PARA MOSTRAR DETALLES (sin cambios) ---

    def show_medico_details(self, parent, user_id):
        medico_info = self.controller.obtener_info_completa_medico(user_id)
        if not medico_info:
            tk.Label(parent, text="Sin información adicional", fg="gray").pack(pady=10)
            return

        prof_frame = tk.LabelFrame(parent, text="Información Profesional")
        prof_frame.pack(fill=tk.X, pady=5)
        prof_data = [
            ("Especialidad", medico_info.get('especialidad')),
            ("Matrícula", medico_info.get('matricula')),
            ("Institución", medico_info.get('institucion')),
            ("Duración turno", medico_info.get('duracion_turno'))
        ]
        for label, value in prof_data:
            if value:
                tk.Label(prof_frame, text=f"{label}: {value}", anchor="w").pack(fill=tk.X, padx=5, pady=1)

    def show_paciente_details(self, parent, user_id):
        self._show_user_specific_details(parent, user_id, "paciente", "obtener_info_paciente",
                                         [("Teléfono", "telefono"), ("Fecha nacimiento", "fecha_nacimiento"),
                                          ("Dirección", "direccion")])

    def show_institucion_details(self, parent, user_id):
        self._show_user_specific_details(parent, user_id, "institución", "obtener_info_institucion",
                                         [("Dirección", "direccion"), ("Teléfono", "telefono"),
                                          ("Tipo", "tipo_institucion")])

    def _show_user_specific_details(self, parent, user_id, tipo_label, method_name, fields):
        info = getattr(self.controller, method_name)(user_id)
        if not info:
            tk.Label(parent, text=f"Sin información adicional del {tipo_label}", fg="gray").pack(pady=10)
            return

        data = info[0] if isinstance(info, list) and info else info
        if not isinstance(data, dict):
            tk.Label(parent, text=f"Sin información adicional del {tipo_label}", fg="gray").pack(pady=10)
            return

        info_frame = tk.LabelFrame(parent, text=f"Información del {tipo_label.title()}")
        info_frame.pack(fill=tk.X, pady=5)
        for label, field_key in fields:
            value = data.get(field_key)
            if value:
                tk.Label(info_frame, text=f"{label}: {value}", anchor="w").pack(fill=tk.X, padx=5, pady=1)