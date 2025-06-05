# ui/admin/users.py

import tkinter as tk
from tkinter import ttk, messagebox


# ==========================
# Clase: UsersFrame (Interfaz de Gestión de Usuarios)
# ==========================
class UsersFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.tipo_usuario_filtro = tk.StringVar(value="todos")
        self.setup_ui()
        self.load_users()

    # ==========================
    # Sección: Configuración de la interfaz
    # ==========================
    def setup_ui(self):
        title = tk.Label(self, text="Gestión de Usuarios", font=("Arial", 14, "bold"))
        title.pack(pady=10)

        # Filtro por tipo de usuario
        filtro_frame = tk.Frame(self)
        filtro_frame.pack()
        tk.Label(filtro_frame, text="Filtrar por tipo:").pack(side=tk.LEFT, padx=5)
        tipo_combobox = ttk.Combobox(
            filtro_frame,
            textvariable=self.tipo_usuario_filtro,
            values=["todos", "paciente", "medico", "institucion", "admin"],
            state="readonly",
            width=15
        )
        tipo_combobox.pack(side=tk.LEFT)
        tipo_combobox.bind("<<ComboboxSelected>>", lambda e: self.load_users())

        # Tabla de usuarios (sin ID visible)
        self.tree = ttk.Treeview(self, columns=("nombre", "email", "tipo"), show="headings")
        self.tree.heading("nombre", text="Nombre")
        self.tree.heading("email", text="Email")
        self.tree.heading("tipo", text="Tipo")
        self.tree.bind("<Double-1>", self.show_user_detail)  # Doble clic para detalles
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Botones de acción
        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)
        tk.Button(button_frame, text="Crear Usuario", command=self.create_user).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Editar Usuario", command=self.edit_user).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Eliminar Usuario", command=self.delete_user).pack(side=tk.LEFT, padx=5)

    # ==========================
    # Sección: Operaciones con la tabla
    # ==========================
    def load_users(self):
        self.tree.delete(*self.tree.get_children())
        result = self.controller.get_all_users()
        if result and result.data:
            tipo = self.tipo_usuario_filtro.get()
            for user in result.data:
                if tipo == "todos" or user.get("tipo") == tipo:
                    self.tree.insert("", "end", values=(
                        user.get("nombre"),
                        user.get("email"),
                        user.get("tipo")
                    ), tags=(user.get("id"),))  # ID oculto en tag

    def get_selected_user_id(self):
        selected = self.tree.selection()
        if not selected:
            return None
        return self.tree.item(selected[0])["tags"][0]

    # ==========================
    # Sección: CRUD
    # ==========================
    def create_user(self):
        self.open_user_form()

    def edit_user(self):
        user_id = self.get_selected_user_id()
        if not user_id:
            messagebox.showwarning("Aviso", "Selecciona un usuario para editar.")
            return

        values = self.tree.item(self.tree.selection()[0])["values"]
        user_data = {
            "nombre": values[0],
            "email": values[1],
            "tipo": values[2]
        }
        self.open_user_form(user_id, user_data)

    def delete_user(self):
        user_id = self.get_selected_user_id()
        if not user_id:
            messagebox.showwarning("Aviso", "Selecciona un usuario para eliminar.")
            return

        confirm = messagebox.askyesno("Confirmar", "¿Estás seguro de que deseas eliminar este usuario?")
        if confirm:
            self.controller.delete_user(user_id)
            self.load_users()

    def open_user_form(self, user_id=None, user_data=None):
        form = tk.Toplevel(self)
        form.title("Formulario de Usuario")
        form.geometry("350x350")

        # Campos del formulario
        tk.Label(form, text="Nombre").pack(pady=5)
        entry_nombre = tk.Entry(form)
        entry_nombre.pack()

        tk.Label(form, text="Apellido").pack(pady=5)
        entry_apellido = tk.Entry(form)
        entry_apellido.pack()

        tk.Label(form, text="Email").pack(pady=5)
        entry_email = tk.Entry(form)
        entry_email.pack()

        tk.Label(form, text="Contraseña").pack(pady=5)
        entry_password = tk.Entry(form, show="*")
        entry_password.pack()

        tk.Label(form, text="Tipo").pack(pady=5)
        tipo_var = tk.StringVar()
        tipo_combobox = ttk.Combobox(
            form,
            textvariable=tipo_var,
            values=["paciente", "medico", "institucion", "admin"],
            state="readonly"
        )
        tipo_combobox.pack()

        # Prellenar campos si es edición
        if user_data:
            entry_nombre.insert(0, user_data.get("nombre", ""))
            entry_apellido.insert(0, user_data.get("apellido", ""))
            entry_email.insert(0, user_data.get("email", ""))
            tipo_var.set(user_data.get("tipo", ""))
            entry_password.configure(state="disabled")  # No permitir cambio de contraseña en edición

        def submit():
            nombre = entry_nombre.get().strip()
            apellido = entry_apellido.get().strip()
            email = entry_email.get().strip()
            tipo = tipo_var.get().strip()

            if not all([nombre, apellido, email, tipo]):
                messagebox.showwarning("Datos incompletos", "Por favor completa todos los campos obligatorios.")
                return

            data = {
                "nombre": nombre,
                "apellido": apellido,
                "email": email,
                "tipo": tipo,
            }

            if user_id:
                self.controller.update_user(user_id, data)
            else:
                password = entry_password.get().strip()
                if not password:
                    messagebox.showwarning("Datos incompletos", "La contraseña es obligatoria para crear el usuario.")
                    return
                data["password"] = password
                self.controller.create_user(data)

            form.destroy()
            self.load_users()

        tk.Button(form, text="Guardar", command=submit).pack(pady=15)

    # ==========================
    # Sección: Vista de detalle por usuario (mejorada)
    # ==========================
    def show_user_detail(self, event=None):
        selected = self.tree.selection()
        if not selected:
            return
        values = self.tree.item(selected[0])["values"]
        user_id = self.tree.item(selected[0])["tags"][0]
        user_tipo = values[2]

        detail = tk.Toplevel(self)
        detail.title("Detalles del Usuario")
        detail.geometry("600x500")
        detail.configure(bg="white")

        # Frame principal con scroll
        main_frame = tk.Frame(detail, bg="white")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Información básica del usuario
        info_frame = tk.LabelFrame(main_frame, text="Información Básica", font=("Arial", 12, "bold"), bg="white")
        info_frame.pack(fill=tk.X, pady=(0, 20))

        tk.Label(info_frame, text=f"Nombre: {values[0]}", font=("Arial", 11), bg="white", anchor="w").pack(fill=tk.X,
                                                                                                           padx=10,
                                                                                                           pady=2)
        tk.Label(info_frame, text=f"Email: {values[1]}", font=("Arial", 11), bg="white", anchor="w").pack(fill=tk.X,
                                                                                                          padx=10,
                                                                                                          pady=2)
        tk.Label(info_frame, text=f"Tipo: {values[2].capitalize()}", font=("Arial", 11), bg="white", anchor="w").pack(
            fill=tk.X, padx=10, pady=2)

        # Información específica según el tipo de usuario
        if user_tipo == "medico":
            self.show_medico_details(main_frame, user_id)
        elif user_tipo == "paciente":
            self.show_paciente_details(main_frame, user_id)
        elif user_tipo == "institucion":
            self.show_institucion_details(main_frame, user_id)

    def show_medico_details(self, parent, user_id):
        """Muestra detalles específicos de un médico"""
        medico_info = self.controller.get_medico_full_info(user_id)

        if not medico_info:
            tk.Label(parent, text="No se encontró información adicional del médico",
                     font=("Arial", 10), fg="red", bg="white").pack(pady=10)
            return

        # Información profesional
        prof_frame = tk.LabelFrame(parent, text="Información Profesional", font=("Arial", 12, "bold"), bg="white")
        prof_frame.pack(fill=tk.X, pady=(0, 15))

        tk.Label(prof_frame, text=f"Especialidad: {medico_info['especialidad']}",
                 font=("Arial", 11), bg="white", anchor="w").pack(fill=tk.X, padx=10, pady=2)
        tk.Label(prof_frame, text=f"Matrícula: {medico_info['matricula']}",
                 font=("Arial", 11), bg="white", anchor="w").pack(fill=tk.X, padx=10, pady=2)
        tk.Label(prof_frame, text=f"Institución: {medico_info['institucion']}",
                 font=("Arial", 11), bg="white", anchor="w").pack(fill=tk.X, padx=10, pady=2)
        tk.Label(prof_frame, text=f"Duración de turno: {medico_info['duracion_turno']}",
                 font=("Arial", 11), bg="white", anchor="w").pack(fill=tk.X, padx=10, pady=2)

        # Horarios disponibles
        horarios_frame = tk.LabelFrame(parent, text="Horarios Disponibles", font=("Arial", 12, "bold"), bg="white")
        horarios_frame.pack(fill=tk.X, pady=(0, 15))

        if medico_info['horarios']:
            for horario in medico_info['horarios']:
                tk.Label(horarios_frame, text=f"• {horario}",
                         font=("Arial", 10), bg="white", anchor="w").pack(fill=tk.X, padx=15, pady=1)
        else:
            tk.Label(horarios_frame, text="No hay horarios configurados",
                     font=("Arial", 10), fg="gray", bg="white").pack(padx=10, pady=5)

        # Pacientes atendidos
        pacientes_frame = tk.LabelFrame(parent, text=f"Pacientes Atendidos ({medico_info['total_pacientes']})",
                                        font=("Arial", 12, "bold"), bg="white")
        pacientes_frame.pack(fill=tk.BOTH, expand=True)

        # Frame con scroll para la lista de pacientes
        canvas = tk.Canvas(pacientes_frame, bg="white", height=150)
        scrollbar = ttk.Scrollbar(pacientes_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="white")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        if medico_info['pacientes']:
            for i, paciente in enumerate(medico_info['pacientes'], 1):
                tk.Label(scrollable_frame, text=f"{i}. {paciente}",
                         font=("Arial", 10), bg="white", anchor="w").pack(fill=tk.X, padx=10, pady=1)
        else:
            tk.Label(scrollable_frame, text="No ha atendido pacientes aún",
                     font=("Arial", 10), fg="gray", bg="white").pack(padx=10, pady=20)

        canvas.pack(side="left", fill="both", expand=True, padx=10, pady=5)
        scrollbar.pack(side="right", fill="y", pady=5)

    def show_paciente_details(self, parent, user_id):
        """Muestra detalles específicos de un paciente"""
        paciente_info = self.controller.get_info_paciente(user_id)

        if paciente_info and paciente_info.data:
            # Manejar si data es una lista o un diccionario
            if isinstance(paciente_info.data, list) and len(paciente_info.data) > 0:
                data = paciente_info.data[0]
            elif isinstance(paciente_info.data, dict):
                data = paciente_info.data
            else:
                data = None

            if data:
                info_frame = tk.LabelFrame(parent, text="Información del Paciente", font=("Arial", 12, "bold"),
                                           bg="white")
                info_frame.pack(fill=tk.X, pady=(0, 15))

                if data.get("telefono"):
                    tk.Label(info_frame, text=f"Teléfono: {data['telefono']}",
                             font=("Arial", 11), bg="white", anchor="w").pack(fill=tk.X, padx=10, pady=2)
                if data.get("fecha_nacimiento"):
                    tk.Label(info_frame, text=f"Fecha de nacimiento: {data['fecha_nacimiento']}",
                             font=("Arial", 11), bg="white", anchor="w").pack(fill=tk.X, padx=10, pady=2)
                if data.get("direccion"):
                    tk.Label(info_frame, text=f"Dirección: {data['direccion']}",
                             font=("Arial", 11), bg="white", anchor="w").pack(fill=tk.X, padx=10, pady=2)
            else:
                tk.Label(parent, text="No se encontró información adicional del paciente",
                         font=("Arial", 10), fg="red", bg="white").pack(pady=10)
        else:
            tk.Label(parent, text="No se encontró información adicional del paciente",
                     font=("Arial", 10), fg="red", bg="white").pack(pady=10)

    def show_institucion_details(self, parent, user_id):
        """Muestra detalles específicos de una institución"""
        institucion_info = self.controller.get_info_institucion(user_id)

        if institucion_info and institucion_info.data:
            # Manejar si data es una lista o un diccionario
            if isinstance(institucion_info.data, list) and len(institucion_info.data) > 0:
                data = institucion_info.data[0]
            elif isinstance(institucion_info.data, dict):
                data = institucion_info.data
            else:
                data = None

            if data:
                info_frame = tk.LabelFrame(parent, text="Información de la Institución", font=("Arial", 12, "bold"),
                                           bg="white")
                info_frame.pack(fill=tk.X, pady=(0, 15))

                if data.get("direccion"):
                    tk.Label(info_frame, text=f"Dirección: {data['direccion']}",
                             font=("Arial", 11), bg="white", anchor="w").pack(fill=tk.X, padx=10, pady=2)
                if data.get("telefono"):
                    tk.Label(info_frame, text=f"Teléfono: {data['telefono']}",
                             font=("Arial", 11), bg="white", anchor="w").pack(fill=tk.X, padx=10, pady=2)
                if data.get("tipo_institucion"):
                    tk.Label(info_frame, text=f"Tipo: {data['tipo_institucion']}",
                             font=("Arial", 11), bg="white", anchor="w").pack(fill=tk.X, padx=10, pady=2)
            else:
                tk.Label(parent, text="No se encontró información adicional de la institución",
                         font=("Arial", 10), fg="red", bg="white").pack(pady=10)
        else:
            tk.Label(parent, text="No se encontró información adicional de la institución",
                     font=("Arial", 10), fg="red", bg="white").pack(pady=10)