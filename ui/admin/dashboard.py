import tkinter as tk
from tkinter import ttk, Toplevel, messagebox
from controllers.admin_controller import AdminController
from tkcalendar import DateEntry  # Asegúrate de que tkcalendar esté instalado
from datetime import datetime  # Importar datetime
import traceback  # Importar para un mejor log de errores


class AdminDashboard(tk.Frame):
    def __init__(self, parent, user_data):
        super().__init__(parent)
        self.parent = parent
        self.user_data = user_data
        self.controller = AdminController()
        self.menu_buttons = {}
        # Se crean los mapas de instancias aquí para que estén disponibles en toda la clase
        self.institucion_map = {}
        self.setup_ui()

    def setup_ui(self):
        self._create_header()
        self._create_main_container()
        self._create_sidebar()
        self._create_content_area()
        self.show_users_panel()

    def _create_header(self):
        header = tk.Frame(self, bg="#2c3e50", height=50)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        tk.Label(header, text=f"Panel de Administrador - {self.user_data['nombre']}",
                 font=("Arial", 14, "bold"), fg="white", bg="#2c3e50").pack(pady=12)

    def _create_main_container(self):
        self.main_container = tk.Frame(self, bg="#f8f9fa")
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def _create_sidebar(self):
        sidebar = tk.Frame(self.main_container, width=180, bg="#ffffff", relief="solid", bd=1)
        sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 5))
        sidebar.pack_propagate(False)

        menu_items = [
            ("Usuarios", self.show_users_panel, "#3498db"),
            ("Reportes", self.show_reports_panel, "#27ae60"),
            ("Agregar Institucion", self.agregar_institucion, "#f39c12"),
            ("Agregar Paciente", self.agregar_paciente, "#8e44ad"),
            ("Agregar Médico", self.agregar_medico, "#1abc9c"),
            ("Registrar Admin", self.agregar_admin, "#FF5733"),
            ("Cerrar Sesión", self.logout, "#e74c3c")
        ]

        for text, command, color in menu_items:
            is_action_button = text in ["Agregar Institucion", "Agregar Paciente", "️Agregar Médico",
                                        "Registrar Admin", "Cerrar Sesión"]
            btn = self._create_menu_button(sidebar, text, command, color, is_action_button)
            if not is_action_button:
                self.menu_buttons[text] = btn
        self._set_active_button("Usuarios")

    def _create_menu_button(self, parent, text, command, color, is_action_button=False):
        def on_click():
            if not is_action_button:
                self._reset_buttons()
                btn.configure(bg=color, fg="white")
            command()

        btn = tk.Button(parent, text=text, command=on_click, font=("Arial", 10, "bold"), fg="#2c3e50", bg="#ecf0f1",
                        relief="flat", bd=0, pady=10)
        btn.pack(fill=tk.X, padx=8, pady=2)
        btn.color = color
        return btn

    def _set_active_button(self, button_text):
        if button_text in self.menu_buttons:
            btn = self.menu_buttons[button_text]
            btn.configure(bg=btn.color, fg="white")

    def _reset_buttons(self):
        for btn in self.menu_buttons.values():
            btn.configure(bg="#ecf0f1", fg="#2c3e50")

    def _create_content_area(self):
        content_container = tk.Frame(self.main_container, bg="white", relief="solid", bd=1)
        content_container.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.canvas = tk.Canvas(content_container, bg="white", highlightthickness=0)
        scrollbar = ttk.Scrollbar(content_container, orient="vertical", command=self.canvas.yview)
        self.content_frame = tk.Frame(self.canvas, bg="white")
        self.content_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.content_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        self.canvas.bind('<MouseWheel>', lambda e: self.canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"))

    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def show_users_panel(self):
        from ui.admin.users import UsersFrame
        self.clear_content()
        self._create_section_header("Gestión de Usuarios")
        frame = UsersFrame(self.content_frame, self.controller)
        frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

    def show_reports_panel(self):
        from ui.admin.reports import ReportsFrame
        self.clear_content()
        self._create_section_header("Reportes y Estadísticas")
        frame = ReportsFrame(self.content_frame, self.controller)
        frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

    def _create_section_header(self, section_title):
        tk.Label(self.content_frame, text=section_title, font=("Arial", 16, "bold"), fg="#2c3e50", bg="white").pack(
            pady=(15, 10))
        tk.Frame(self.content_frame, height=2, bg="#3498db").pack(fill=tk.X, padx=15, pady=(0, 10))

    def agregar_institucion(self):
        self.popup = Toplevel(self.parent)
        self.popup.title("Agregar Nueva Institución")
        parent_x, parent_y = self.parent.winfo_x(), self.parent.winfo_y()
        parent_w, parent_h = self.parent.winfo_width(), self.parent.winfo_height()
        w, h = 450, 480
        x = parent_x + (parent_w // 2) - (w // 2)
        y = parent_y + (parent_h // 2) - (h // 2)
        self.popup.geometry(f'{w}x{h}+{x}+{y}')
        self.popup.resizable(False, False)
        self.popup.configure(bg="#f0f0f0")
        self.popup.grab_set()
        self._crear_formulario_institucion(self.popup)

    def _crear_formulario_institucion(self, parent_popup):
        frame = tk.Frame(parent_popup, bg="#f0f0f0", padx=20, pady=20)
        frame.pack(fill=tk.BOTH, expand=True)
        frame.columnconfigure(1, weight=1)

        tk.Label(frame, text="Datos de la Institución", font=("Arial", 14, "bold"), bg="#f0f0f0").grid(row=0, column=0,
                                                                                                       columnspan=2,
                                                                                                       pady=(0, 20))

        tk.Label(frame, text="Nombre:", font=("Arial", 10), bg="#f0f0f0").grid(row=1, column=0, sticky="w", padx=5,
                                                                               pady=5)
        self.nombre_inst_entry = ttk.Entry(frame, font=("Arial", 10))
        self.nombre_inst_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

        tk.Label(frame, text="Dirección:", font=("Arial", 10), bg="#f0f0f0").grid(row=2, column=0, sticky="w", padx=5,
                                                                                  pady=5)
        self.direccion_inst_entry = ttk.Entry(frame, font=("Arial", 10))
        self.direccion_inst_entry.grid(row=2, column=1, sticky="ew", padx=5, pady=5)

        tk.Label(frame, text="Email (Login):", font=("Arial", 10), bg="#f0f0f0").grid(row=3, column=0, sticky="w",
                                                                                      padx=5, pady=5)
        self.email_inst_entry = ttk.Entry(frame, font=("Arial", 10))
        self.email_inst_entry.grid(row=3, column=1, sticky="ew", padx=5, pady=5)

        tk.Label(frame, text="Contraseña:", font=("Arial", 10), bg="#f0f0f0").grid(row=4, column=0, sticky="w", padx=5,
                                                                                   pady=5)
        self.password_inst_entry = ttk.Entry(frame, font=("Arial", 10), show="*")
        self.password_inst_entry.grid(row=4, column=1, sticky="ew", padx=5, pady=5)

        tk.Label(frame, text="Confirmar Contraseña:", font=("Arial", 10), bg="#f0f0f0").grid(row=5, column=0,
                                                                                             sticky="w", padx=5, pady=5)
        self.confirm_password_inst_entry = ttk.Entry(frame, font=("Arial", 10), show="*")
        self.confirm_password_inst_entry.grid(row=5, column=1, sticky="ew", padx=5, pady=5)

        tk.Label(frame, text="Teléfono (Opcional):", font=("Arial", 10), bg="#f0f0f0").grid(row=6, column=0, sticky="w",
                                                                                            padx=5, pady=5)
        self.telefono_inst_entry = ttk.Entry(frame, font=("Arial", 10))
        self.telefono_inst_entry.grid(row=6, column=1, sticky="ew", padx=5, pady=5)

        tk.Label(frame, text="Descripción (Opcional):", font=("Arial", 10), bg="#f0f0f0").grid(row=7, column=0,
                                                                                               sticky="w", padx=5,
                                                                                               pady=5)
        self.descripcion_inst_entry = ttk.Entry(frame, font=("Arial", 10))
        self.descripcion_inst_entry.grid(row=7, column=1, sticky="ew", padx=5, pady=5)

        tk.Label(frame, text="Horario Apertura (Opcional):", font=("Arial", 10), bg="#f0f0f0").grid(row=8, column=0,
                                                                                                    sticky="w", padx=5,
                                                                                                    pady=5)
        self.horario_apertura_inst_entry = ttk.Entry(frame, font=("Arial", 10))
        self.horario_apertura_inst_entry.grid(row=8, column=1, sticky="ew", padx=5, pady=5)

        tk.Label(frame, text="Horario Cierre (Opcional):", font=("Arial", 10), bg="#f0f0f0").grid(row=9, column=0,
                                                                                                  sticky="w", padx=5,
                                                                                                  pady=5)
        self.horario_cierre_inst_entry = ttk.Entry(frame, font=("Arial", 10))
        self.horario_cierre_inst_entry.grid(row=9, column=1, sticky="ew", padx=5, pady=5)

        button_frame = tk.Frame(frame, bg="#f0f0f0")
        button_frame.grid(row=10, column=0, columnspan=2, pady=(25, 0))

        guardar_btn = tk.Button(button_frame, text="Guardar Institución", command=self._guardar_institucion,
                                font=("Arial", 10, "bold"), bg="#27ae60", fg="white", relief="flat", padx=10, pady=5)
        guardar_btn.pack(side=tk.LEFT, padx=10)

        cancelar_btn = tk.Button(button_frame, text="Cancelar", command=parent_popup.destroy,
                                 font=("Arial", 10, "bold"), bg="#e74c3c", fg="white", relief="flat", padx=10, pady=5)
        cancelar_btn.pack(side=tk.LEFT, padx=10)

    def _guardar_institucion(self):
        # --- BLOQUE CORREGIDO ---
        nombre = self.nombre_inst_entry.get().strip()
        direccion = self.direccion_inst_entry.get().strip()
        email = self.email_inst_entry.get().strip()
        password = self.password_inst_entry.get().strip()
        confirm_password = self.confirm_password_inst_entry.get().strip()

        # Corrección: Convertir strings vacíos a None para que la DB los acepte como NULL
        telefono = self.telefono_inst_entry.get().strip() or None
        descripcion = self.descripcion_inst_entry.get().strip() or None
        horario_apertura = self.horario_apertura_inst_entry.get().strip() or None
        horario_cierre = self.horario_cierre_inst_entry.get().strip() or None

        if not all([nombre, direccion, email, password, confirm_password]):
            messagebox.showwarning("Campos Requeridos", "Por favor, completa todos los campos obligatorios.",
                                   parent=self.popup)
            return

        if password != confirm_password:
            messagebox.showwarning("Contraseña no coincide", "Las contraseñas no coinciden.", parent=self.popup)
            return

        try:
            self.controller.registrar_nueva_institucion(
                nombre=nombre, password=password, direccion=direccion,
                email=email, telefono=telefono, descripcion=descripcion,
                horario_apertura=horario_apertura,
                horario_cierre=horario_cierre
            )
            messagebox.showinfo("Éxito", "Institución registrada correctamente.", parent=self.popup)
            self.popup.destroy()
            self.show_users_panel()
        except Exception as e:
            # Manejo de errores mejorado para facilitar la depuración
            print("--- ERROR DETALLADO AL REGISTRAR INSTITUCIÓN ---")
            traceback.print_exc()
            print("-------------------------------------------------")
            messagebox.showerror("Error de Registro", f"No se pudo registrar la institución.\n\nError: {e}",
                                 parent=self.popup)

    # ... El resto del código de la clase permanece igual ...
    def agregar_paciente(self):
        self.popup_paciente = Toplevel(self)
        self.popup_paciente.title("Agregar Nuevo Paciente")
        parent_x, parent_y = self.parent.winfo_x(), self.parent.winfo_y()
        parent_w, parent_h = self.parent.winfo_width(), self.parent.winfo_height()
        w, h = 450, 530
        x = parent_x + (parent_w // 2) - (w // 2)
        y = parent_y + (parent_h // 2) - (h // 2)
        self.popup_paciente.geometry(f'{w}x{h}+{x}+{y}')
        self.popup_paciente.resizable(False, False)
        self.popup_paciente.grab_set()
        self._crear_formulario_paciente(self.popup_paciente)

    def _crear_formulario_paciente(self, parent_popup):
        frame = tk.Frame(parent_popup, padx=20, pady=20)
        frame.pack(fill=tk.BOTH, expand=True)
        frame.columnconfigure(1, weight=1)

        tk.Label(frame, text="Datos del Paciente", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2,
                                                                                    pady=(0, 20))

        self.nombre_pac_entry = self._create_label_entry(frame, "Nombre:", 1)
        self.apellido_pac_entry = self._create_label_entry(frame, "Apellido:", 2)
        self.email_pac_entry = self._create_label_entry(frame, "Email (Login):", 3)

        tk.Label(frame, text="Contraseña:", font=("Arial", 10)).grid(row=4, column=0, sticky="w", padx=5, pady=5)
        self.password_pac_entry = ttk.Entry(frame, font=("Arial", 10), show="*")
        self.password_pac_entry.grid(row=4, column=1, sticky="ew", padx=5, pady=5)

        tk.Label(frame, text="Confirmar Contraseña:", font=("Arial", 10)).grid(row=5, column=0, sticky="w", padx=5,
                                                                               pady=5)
        self.confirm_password_pac_entry = ttk.Entry(frame, font=("Arial", 10), show="*")
        self.confirm_password_pac_entry.grid(row=5, column=1, sticky="ew", padx=5, pady=5)

        self.telefono_pac_entry = self._create_label_entry(frame, "Teléfono (Opcional):", 6)

        tk.Label(frame, text="Fecha Nac. (YYYY-MM-DD):", font=("Arial", 10)).grid(row=7, column=0, sticky="w", padx=5,
                                                                                  pady=5)
        self.fecha_nac_pac_entry = DateEntry(frame, width=12, background='darkblue', foreground='white', borderwidth=2,
                                             year=2000, date_pattern='yyyy-mm-dd')
        self.fecha_nac_pac_entry.grid(row=7, column=1, sticky="ew", padx=5, pady=5)

        tk.Label(frame, text="Género:", font=("Arial", 10)).grid(row=8, column=0, sticky="w", padx=5, pady=5)
        self.genero_pac_var = tk.StringVar(value="Masculino")
        self.genero_pac_combo = ttk.Combobox(frame, textvariable=self.genero_pac_var,
                                             values=["Masculino", "Femenino", "Otro"], state="readonly")
        self.genero_pac_combo.grid(row=8, column=1, sticky="ew", padx=5, pady=5)

        obras_sociales_lista = [
            "(Ninguna)", "UPCN", "OSECAC", "AMRA", "OSPECON",
            "Bancarios", "OSPANA", "Osep", "Ospesan",
            "Ossset", "Medifé"
        ]
        tk.Label(frame, text="Obra Social (Opcional):", font=("Arial", 10)).grid(row=9, column=0, sticky="w", padx=5,
                                                                                 pady=5)
        self.obra_social_pac_var = tk.StringVar()
        self.obra_social_pac_combo = ttk.Combobox(frame, textvariable=self.obra_social_pac_var,
                                                  values=obras_sociales_lista, state="readonly")
        self.obra_social_pac_combo.grid(row=9, column=1, sticky="ew", padx=5, pady=5)
        self.obra_social_pac_combo.set(obras_sociales_lista[0])

        self.num_afiliado_pac_entry = self._create_label_entry(frame, "N° Afiliado (Opcional):", 10)
        ttk.Button(frame, text="Guardar Paciente", command=self._guardar_paciente).grid(row=11, column=0, columnspan=2,
                                                                                        pady=20)

    def _create_label_entry(self, parent_frame, label_text, row, show=""):
        tk.Label(parent_frame, text=label_text, font=("Arial", 10)).grid(row=row, column=0, sticky="w", padx=5, pady=5)
        entry = ttk.Entry(parent_frame, font=("Arial", 10), show=show)
        entry.grid(row=row, column=1, sticky="ew", padx=5, pady=5)
        return entry

    def _guardar_paciente(self):
        nombre = self.nombre_pac_entry.get().strip()
        apellido = self.apellido_pac_entry.get().strip()
        email = self.email_pac_entry.get().strip()
        password = self.password_pac_entry.get().strip()
        confirm_password = self.confirm_password_pac_entry.get().strip()
        telefono = self.telefono_pac_entry.get().strip()
        fecha_nacimiento = self.fecha_nac_pac_entry.get_date().strftime('%Y-%m-%d')
        genero = self.genero_pac_var.get().strip()

        obra_social = self.obra_social_pac_var.get().strip()
        if obra_social == "(Ninguna)":
            obra_social = ""

        num_afiliado = self.num_afiliado_pac_entry.get().strip()

        if not all([nombre, apellido, email, password, confirm_password]):
            messagebox.showwarning("Campos Requeridos", "Por favor, completa los campos obligatorios.",
                                   parent=self.popup_paciente)
            return

        if password != confirm_password:
            messagebox.showwarning("Contraseña no coincide", "Las contraseñas no coinciden.",
                                   parent=self.popup_paciente)
            return

        try:
            self.controller.registrar_nuevo_paciente(
                nombre=nombre, apellido=apellido, email=email, password=password,
                telefono=telefono, fecha_nacimiento=fecha_nacimiento, genero=genero,
                obra_social=obra_social, num_afiliado=num_afiliado
            )
            messagebox.showinfo("Éxito", "Paciente registrado correctamente.", parent=self.popup_paciente)
            self.popup_paciente.destroy()
            self.show_users_panel()
        except Exception as e:
            messagebox.showerror("Error de Registro", f"Error al registrar el paciente: {e}",
                                 parent=self.popup_paciente)

    def agregar_medico(self):
        self.popup_medico = Toplevel(self)
        self.popup_medico.title("Agregar Nuevo Médico")
        parent_x, parent_y = self.parent.winfo_x(), self.parent.winfo_y()
        parent_w, parent_h = self.parent.winfo_width(), self.parent.winfo_height()
        w, h = 450, 630
        x = parent_x + (parent_w // 2) - (w // 2)
        y = parent_y + (parent_h // 2) - (h // 2)
        self.popup_medico.geometry(f'{w}x{h}+{x}+{y}')
        self.popup_medico.resizable(False, False)
        self.popup_medico.grab_set()
        self._crear_formulario_medico(self.popup_medico)

    def _crear_formulario_medico(self, parent_popup):
        especialidades = [
            "Cardiología", "Dermatología", "Endocrinología", "Gastroenterología", "Ginecología",
            "Medicina General", "Medicina Interna", "Neurología", "Oftalmología", "Oncología",
            "Ortopedia", "Otorrinolaringología", "Pediatría", "Psiquiatría", "Radiología",
            "Traumatología", "Urología"
        ]
        frame = tk.Frame(parent_popup, padx=20, pady=20)
        frame.pack(fill=tk.BOTH, expand=True)
        frame.columnconfigure(1, weight=1)

        tk.Label(frame, text="Datos del Médico", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2,
                                                                                  pady=(0, 20))

        self.nombre_med_entry = self._create_label_entry(frame, "Nombre:", 1)
        self.apellido_med_entry = self._create_label_entry(frame, "Apellido:", 2)
        self.email_med_entry = self._create_label_entry(frame, "Email (Login):", 3)

        tk.Label(frame, text="Contraseña:", font=("Arial", 10)).grid(row=4, column=0, sticky="w", padx=5, pady=5)
        self.password_med_entry = ttk.Entry(frame, font=("Arial", 10), show="*")
        self.password_med_entry.grid(row=4, column=1, sticky="ew", padx=5, pady=5)
        tk.Label(frame, text="Confirmar Contraseña:", font=("Arial", 10)).grid(row=5, column=0, sticky="w", padx=5,
                                                                               pady=5)
        self.confirm_password_med_entry = ttk.Entry(frame, font=("Arial", 10), show="*")
        self.confirm_password_med_entry.grid(row=5, column=1, sticky="ew", padx=5, pady=5)

        tk.Label(frame, text="Especialidad:", font=("Arial", 10)).grid(row=6, column=0, sticky="w", padx=5, pady=5)
        self.especialidad_med_var = tk.StringVar()
        self.especialidad_med_combo = ttk.Combobox(frame, textvariable=self.especialidad_med_var, values=especialidades,
                                                   state="readonly")
        self.especialidad_med_combo.grid(row=6, column=1, sticky="ew", padx=5, pady=5)
        self.especialidad_med_combo.set("Medicina General")

        self.matricula_med_entry = self._create_label_entry(frame, "Matrícula:", 7)

        instituciones = self.controller.obtener_instituciones()
        institucion_options = ["(Ninguna)"]
        self.institucion_map = {"(Ninguna)": None}
        if instituciones:
            for inst in instituciones:
                institucion_options.append(inst.get("nombre"))
                self.institucion_map[inst.get("nombre")] = inst.get("id")

        tk.Label(frame, text="Institución (Opcional):", font=("Arial", 10)).grid(row=8, column=0, sticky="w", padx=5,
                                                                                 pady=5)
        self.institucion_med_var = tk.StringVar(value="(Ninguna)")
        self.institucion_med_combo = ttk.Combobox(frame, textvariable=self.institucion_med_var,
                                                  values=institucion_options, state="readonly")
        self.institucion_med_combo.grid(row=8, column=1, sticky="ew", padx=5, pady=5)

        self.duracion_turno_med_entry = self._create_label_entry(frame, "Duración Turno (min):", 9)
        ttk.Button(frame, text="Guardar Médico", command=self._guardar_medico).grid(row=10, column=0, columnspan=2,
                                                                                    pady=20)

    def _guardar_medico(self):
        nombre = self.nombre_med_entry.get().strip()
        apellido = self.apellido_med_entry.get().strip()
        email = self.email_med_entry.get().strip()
        password = self.password_med_entry.get().strip()
        confirm_password = self.confirm_password_med_entry.get().strip()
        especialidad = self.especialidad_med_var.get().strip()
        matricula = self.matricula_med_entry.get().strip()
        duracion_turno = self.duracion_turno_med_entry.get().strip()
        institucion_nombre_seleccionada = self.institucion_med_var.get()
        institucion_id = self.institucion_map.get(institucion_nombre_seleccionada)

        try:
            duracion_turno = int(duracion_turno) if duracion_turno else None
        except ValueError:
            messagebox.showwarning("Formato Inválido", "La duración del turno debe ser un número entero.",
                                   parent=self.popup_medico)
            return

        if not all([nombre, apellido, email, password, confirm_password, especialidad, matricula]):
            messagebox.showwarning("Campos Requeridos", "Por favor, completa los campos obligatorios.",
                                   parent=self.popup_medico)
            return

        if password != confirm_password:
            messagebox.showwarning("Contraseña no coincide", "Las contraseñas no coinciden.", parent=self.popup_medico)
            return

        try:
            self.controller.registrar_nuevo_medico(
                nombre=nombre, apellido=apellido, email=email, password=password,
                especialidad=especialidad, matricula=matricula, institucion_id=institucion_id,
                duracion_turno=duracion_turno
            )
            messagebox.showinfo("Éxito", "Médico registrado correctamente.", parent=self.popup_medico)
            self.popup_medico.destroy()
            self.show_users_panel()
        except Exception as e:
            messagebox.showerror("Error de Registro", f"Error al registrar el médico: {e}", parent=self.popup_medico)

    def agregar_admin(self):
        self.popup_admin = Toplevel(self)
        self.popup_admin.title("Registrar Nuevo Administrador")
        parent_x, parent_y = self.parent.winfo_x(), self.parent.winfo_y()
        parent_w, parent_h = self.parent.winfo_width(), self.parent.winfo_height()
        w, h = 450, 350
        x = parent_x + (parent_w // 2) - (w // 2)
        y = parent_y + (parent_h // 2) - (h // 2)
        self.popup_admin.geometry(f'{w}x{h}+{x}+{y}')
        self.popup_admin.resizable(False, False)
        self.popup_admin.grab_set()
        self._crear_formulario_admin(self.popup_admin)

    def _crear_formulario_admin(self, parent_popup):
        frame = tk.Frame(parent_popup, padx=20, pady=20)
        frame.pack(fill=tk.BOTH, expand=True)
        frame.columnconfigure(1, weight=1)

        tk.Label(frame, text="Datos del Administrador", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2,
                                                                                         pady=(0, 20))

        self.nombre_admin_entry = self._create_label_entry(frame, "Nombre:", 1)
        self.apellido_admin_entry = self._create_label_entry(frame, "Apellido:", 2)
        self.email_admin_entry = self._create_label_entry(frame, "Email (Login):", 3)

        tk.Label(frame, text="Contraseña:", font=("Arial", 10)).grid(row=4, column=0, sticky="w", padx=5, pady=5)
        self.password_admin_entry = ttk.Entry(frame, font=("Arial", 10), show="*")
        self.password_admin_entry.grid(row=4, column=1, sticky="ew", padx=5, pady=5)
        tk.Label(frame, text="Confirmar Contraseña:", font=("Arial", 10)).grid(row=5, column=0, sticky="w", padx=5,
                                                                               pady=5)
        self.confirm_password_admin_entry = ttk.Entry(frame, font=("Arial", 10), show="*")
        self.confirm_password_admin_entry.grid(row=5, column=1, sticky="ew", padx=5, pady=5)

        ttk.Button(frame, text="Registrar Administrador", command=self._guardar_admin).grid(row=6, column=0,
                                                                                            columnspan=2, pady=20)

    def _guardar_admin(self):
        nombre = self.nombre_admin_entry.get().strip()
        apellido = self.apellido_admin_entry.get().strip()
        email = self.email_admin_entry.get().strip()
        password = self.password_admin_entry.get().strip()
        confirm_password = self.confirm_password_admin_entry.get().strip()

        if not all([nombre, apellido, email, password, confirm_password]):
            messagebox.showwarning("Campos Requeridos", "Por favor, completa todos los campos obligatorios.",
                                   parent=self.popup_admin)
            return

        if password != confirm_password:
            messagebox.showwarning("Contraseña no coincide", "Las contraseñas no coinciden.", parent=self.popup_admin)
            return

        try:
            self.controller.crear_usuario(
                email=email, password=password, tipo='admin',
                nombre=nombre, apellido=apellido
            )
            messagebox.showinfo("Éxito", "Administrador registrado correctamente.", parent=self.popup_admin)
            self.popup_admin.destroy()
            self.show_users_panel()
        except Exception as e:
            messagebox.showerror("Error de Registro", f"Error al registrar el administrador: {e}",
                                 parent=self.popup_admin)

    def logout(self):
        self.parent.logout()