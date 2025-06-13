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
        user_id = self.get_selected_user_id()
        if not user_id:
            messagebox.showwarning("Aviso", "Selecciona un usuario para editar.")
            return

        values = self.tree.item(self.tree.selection()[0])["values"]
        user_data = dict(zip(["nombre", "email", "tipo"], values))
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
        form = tk.Toplevel(self)
        form.title("Usuario")
        form.geometry("300x280")

        # Campos
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

        # Tipo de usuario
        tk.Label(form, text="Tipo").pack(pady=2)
        tipo_var = tk.StringVar()
        tipo_combo = ttk.Combobox(
            form, textvariable=tipo_var,
            values=["paciente", "medico", "institucion", "admin"],
            state="readonly"
        )
        tipo_combo.pack(pady=2)

        # Prellenar si es edición
        if user_data:
            for field in ["nombre", "apellido", "email"]:
                if field in fields:
                    fields[field].insert(0, user_data.get(field, ""))
            tipo_var.set(user_data.get("tipo", ""))
            fields["password"].configure(state="disabled")

        def submit():
            data = {field: entry.get().strip() for field, entry in fields.items()}
            data["tipo"] = tipo_var.get().strip()

            required = ["nombre", "apellido", "email", "tipo"]
            if not user_id:
                required.append("password")

            if not all(data.get(field) for field in required):
                messagebox.showwarning("Error", "Completa todos los campos obligatorios.")
                return

            if user_id:
                del data["password"]  # No enviar password en edición
                self.controller.actualizar_usuario(user_id, data)
            else:
                self.controller.crear_usuario(data["email"], data["password"], data["tipo"], data["nombre"], data["apellido"])

            form.destroy()
            self.load_users()

        tk.Button(form, text="Guardar", command=submit).pack(pady=15)

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

        # Información básica
        info_frame = tk.LabelFrame(detail, text="Información Básica", font=("Arial", 10, "bold"))
        info_frame.pack(fill=tk.X, padx=10, pady=5)

        for label, value in [("Nombre", values[0]), ("Email", values[1]), ("Tipo", values[2].capitalize())]:
            tk.Label(info_frame, text=f"{label}: {value}", anchor="w").pack(fill=tk.X, padx=5, pady=1)

        # Información específica según tipo
        content_frame = tk.Frame(detail)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        if user_tipo == "medico":
            self.show_medico_details(content_frame, user_id)
        elif user_tipo == "paciente":
            self.show_paciente_details(content_frame, user_id)
        elif user_tipo == "institucion":
            self.show_institucion_details(content_frame, user_id)

    def show_medico_details(self, parent, user_id):
        medico_info = self.controller.obtener_info_completa_medico(user_id)
        if not medico_info:
            tk.Label(parent, text="Sin información adicional", fg="gray").pack(pady=10)
            return

        # Info profesional
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

        # Horarios (simplificado)
        if medico_info.get('horarios'):
            horarios_frame = tk.LabelFrame(parent, text="Horarios")
            horarios_frame.pack(fill=tk.X, pady=5)

            horarios_text = ", ".join(medico_info['horarios'][:3])  # Solo primeros 3
            if len(medico_info['horarios']) > 3:
                horarios_text += f" (+{len(medico_info['horarios']) - 3} más)"

            tk.Label(horarios_frame, text=horarios_text, wraplength=400).pack(padx=5, pady=5)

        # Pacientes (simplificado)
        total_pacientes = medico_info.get('total_pacientes', 0)
        if total_pacientes > 0:
            pacientes_frame = tk.LabelFrame(parent, text=f"Pacientes Atendidos ({total_pacientes})")
            pacientes_frame.pack(fill=tk.X, pady=5)

            if medico_info.get('pacientes'):
                # Mostrar solo los primeros 5
                pacientes_muestra = medico_info['pacientes'][:5]
                for paciente in pacientes_muestra:
                    tk.Label(pacientes_frame, text=f"• {paciente}", anchor="w").pack(fill=tk.X, padx=10, pady=1)

                if len(medico_info['pacientes']) > 5:
                    tk.Label(pacientes_frame, text=f"... y {len(medico_info['pacientes']) - 5} más",
                             fg="gray", anchor="w").pack(fill=tk.X, padx=10)

    def show_paciente_details(self, parent, user_id):
        self._show_user_specific_details(parent, user_id, "paciente", "obtener_info_paciente",
                                         [("Teléfono", "telefono"), ("Fecha nacimiento", "fecha_nacimiento"),
                                          ("Dirección", "direccion")])

    def show_institucion_details(self, parent, user_id):
        self._show_user_specific_details(parent, user_id, "institución", "obtener_info_institucion",
                                         [("Dirección", "direccion"), ("Teléfono", "telefono"),
                                          ("Tipo", "tipo_institucion")])

    def _show_user_specific_details(self, parent, user_id, tipo_label, method_name, fields):
        """Método helper para mostrar detalles específicos de usuario"""
        info = getattr(self.controller, method_name)(user_id)

        if not info:
            tk.Label(parent, text=f"Sin información adicional del {tipo_label}", fg="gray").pack(pady=10)
            return

        # Manejar formato de datos
        data = info[0] if isinstance(info, list) and info else info
        if not isinstance(data, dict):
            tk.Label(parent, text=f"Sin información adicional del {tipo_label}", fg="gray").pack(pady=10)
            return

        # Mostrar campos
        info_frame = tk.LabelFrame(parent, text=f"Información del {tipo_label.title()}")
        info_frame.pack(fill=tk.X, pady=5)

        for label, field_key in fields:
            value = data.get(field_key)
            if value:
                tk.Label(info_frame, text=f"{label}: {value}", anchor="w").pack(fill=tk.X, padx=5, pady=1)