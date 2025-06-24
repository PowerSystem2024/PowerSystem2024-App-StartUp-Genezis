# ui/admin/dashboard.py

import tkinter as tk
from tkinter import ttk, Toplevel, messagebox
from controllers.admin_controller import AdminController

# =============================================================================
# === REEMPLAZA TODA TU CLASE CON ESTE BLOQUE DE CÓDIGO CORREGIDO Y COMPLETO ===
# =============================================================================

class AdminDashboard(tk.Frame):
    def __init__(self, parent, user_data):
        super().__init__(parent)
        self.parent = parent
        self.user_data = user_data
        self.controller = AdminController()
        self.menu_buttons = {}
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
        tk.Label(header, text=f"🛠️ Panel de Administrador - {self.user_data['nombre']}",
                 font=("Arial", 14, "bold"), fg="white", bg="#2c3e50").pack(pady=12)

    def _create_main_container(self):
        self.main_container = tk.Frame(self, bg="#f8f9fa")
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def _create_sidebar(self):
        sidebar = tk.Frame(self.main_container, width=180, bg="#ffffff", relief="solid", bd=1)
        sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 5))
        sidebar.pack_propagate(False)

        menu_items = [
            ("👥 Usuarios", self.show_users_panel, "#3498db"),
            ("📊 Reportes", self.show_reports_panel, "#27ae60"),
            ("🏥 Agregar Institucion", self.agregar_institucion, "#f39c12"),
            ("🚪 Cerrar Sesión", self.logout, "#e74c3c")
        ]

        for text, command, color in menu_items:
            is_action_button = text in ["🏥 Agregar Institucion", "🚪 Cerrar Sesión"]
            btn = self._create_menu_button(sidebar, text, command, color, is_action_button)
            if not is_action_button:
                self.menu_buttons[text] = btn
        self._set_active_button("👥 Usuarios")

    def _create_menu_button(self, parent, text, command, color, is_action_button=False):
        def on_click():
            if not is_action_button:
                self._reset_buttons()
                btn.configure(bg=color, fg="white")
            command()
        btn = tk.Button(parent, text=text, command=on_click, font=("Arial", 10, "bold"), fg="#2c3e50", bg="#ecf0f1", relief="flat", bd=0, pady=10)
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
        self._create_section_header("👥 Gestión de Usuarios")
        frame = UsersFrame(self.content_frame, self.controller)
        frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

    def show_reports_panel(self):
        from ui.admin.reports import ReportsFrame
        self.clear_content()
        self._create_section_header("📊 Reportes y Estadísticas")
        frame = ReportsFrame(self.content_frame, self.controller)
        frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

    def _create_section_header(self, section_title):
        tk.Label(self.content_frame, text=section_title, font=("Arial", 16, "bold"), fg="#2c3e50", bg="white").pack(pady=(15, 10))
        tk.Frame(self.content_frame, height=2, bg="#3498db").pack(fill=tk.X, padx=15, pady=(0, 10))

    def agregar_institucion(self):
        self.popup = Toplevel(self)
        self.popup.title("Agregar Nueva Institución")
        parent_x = self.parent.winfo_x()
        parent_y = self.parent.winfo_y()
        parent_w = self.parent.winfo_width()
        parent_h = self.parent.winfo_height()
        w, h = 450, 400
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
        tk.Label(frame, text="Datos de la Institución", font=("Arial", 14, "bold"), bg="#f0f0f0").grid(row=0, column=0, columnspan=2, pady=(0, 20))
        tk.Label(frame, text="Nombre:", font=("Arial", 10), bg="#f0f0f0").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.nombre_entry = ttk.Entry(frame, font=("Arial", 10))
        self.nombre_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=5)
        tk.Label(frame, text="Dirección:", font=("Arial", 10), bg="#f0f0f0").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.direccion_entry = ttk.Entry(frame, font=("Arial", 10))
        self.direccion_entry.grid(row=2, column=1, sticky="ew", padx=5, pady=5)
        tk.Label(frame, text="Email (Login):", font=("Arial", 10), bg="#f0f0f0").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.email_entry = ttk.Entry(frame, font=("Arial", 10))
        self.email_entry.grid(row=3, column=1, sticky="ew", padx=5, pady=5)
        tk.Label(frame, text="Contraseña:", font=("Arial", 10), bg="#f0f0f0").grid(row=4, column=0, sticky="w", padx=5, pady=5)
        self.password_entry = ttk.Entry(frame, font=("Arial", 10), show="*")
        self.password_entry.grid(row=4, column=1, sticky="ew", padx=5, pady=5)
        tk.Label(frame, text="Teléfono:", font=("Arial", 10), bg="#f0f0f0").grid(row=5, column=0, sticky="w", padx=5, pady=5)
        self.telefono_entry = ttk.Entry(frame, font=("Arial", 10))
        self.telefono_entry.grid(row=5, column=1, sticky="ew", padx=5, pady=5)
        tk.Label(frame, text="Descripción:", font=("Arial", 10), bg="#f0f0f0").grid(row=6, column=0, sticky="w", padx=5, pady=5)
        self.descripcion_entry = ttk.Entry(frame, font=("Arial", 10))
        self.descripcion_entry.grid(row=6, column=1, sticky="ew", padx=5, pady=5)
        button_frame = tk.Frame(frame, bg="#f0f0f0")
        button_frame.grid(row=7, column=0, columnspan=2, pady=(25, 0))
        guardar_btn = tk.Button(button_frame, text="Guardar Institución", command=self._guardar_nueva_institucion, font=("Arial", 10, "bold"), bg="#27ae60", fg="white", relief="flat", padx=10, pady=5)
        guardar_btn.pack(side=tk.LEFT, padx=10)
        cancelar_btn = tk.Button(button_frame, text="Cancelar", command=self.popup.destroy, font=("Arial", 10, "bold"), bg="#e74c3c", fg="white", relief="flat", padx=10, pady=5)
        cancelar_btn.pack(side=tk.LEFT, padx=10)

    def _guardar_nueva_institucion(self):
        nombre = self.nombre_entry.get().strip()
        direccion = self.direccion_entry.get().strip()
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()
        telefono = self.telefono_entry.get().strip()
        descripcion = self.descripcion_entry.get().strip()
        if not all([nombre, direccion, email, password]):
            messagebox.showerror("Error de Validación", "Los campos Nombre, Dirección, Email y Contraseña son obligatorios.", parent=self.popup)
            return
        try:
            self.controller.registrar_nueva_institucion(nombre=nombre, password=password, direccion=direccion, email=email, telefono=telefono, descripcion=descripcion)
            messagebox.showinfo("Éxito", f"Institución '{nombre}' registrada correctamente.", parent=self.popup)
            self.popup.destroy()
        except Exception as e:
            messagebox.showerror("Error al Guardar", f"Ocurrió un error al registrar:\n{e}", parent=self.popup)

    def logout(self):
        self.parent.logout()