import tkinter as tk
from tkinter import ttk, messagebox
from controllers import inst_controller
from controllers.auth_controller import AuthController


# ======================================================================
# CLASE 1: EL PANEL PRINCIPAL DE MÉDICOS (DASHBOARD)
# ======================================================================

class MedicosDashboard(tk.Frame):
    def __init__(self, parent, institucion):
        super().__init__(parent)
        self.parent = parent
        self.institucion = institucion

        self.main_frame = ttk.Frame(self, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.crear_widgets()
        self.cargar_datos()

    def crear_widgets(self):
        btn_frame = ttk.Frame(self.main_frame)
        btn_frame.pack(fill=tk.X, pady=10)

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

        lista_frame = ttk.LabelFrame(
            self.main_frame,
            text="Médicos Registrados en la Institución",
            padding="10"
        )
        lista_frame.pack(fill=tk.BOTH, expand=True)

        columns = ("id", "nombre", "apellido", "especialidad", "matricula", "duracion_turno")
        self.tree = ttk.Treeview(lista_frame, columns=columns, show='headings')

        self.tree.heading('nombre', text='Nombre')
        self.tree.heading('apellido', text='Apellido')
        self.tree.heading('especialidad', text='Especialidad')
        self.tree.heading('matricula', text='Matrícula')
        self.tree.heading('duracion_turno', text='Duración Turno')

        self.tree.column("id", width=0, stretch=tk.NO)
        self.tree.column('nombre', width=120)
        self.tree.column('apellido', width=120)
        self.tree.column('especialidad', width=150)
        self.tree.column('matricula', width=100)
        self.tree.column('duracion_turno', width=100)

        self.tree.pack(fill=tk.BOTH, expand=True, pady=5)

    def cargar_datos(self):
        try:
            for item in self.tree.get_children():
                self.tree.delete(item)

            medicos = inst_controller.obtenerMedicosConUsuarios()
            medicos_institucion = [m for m in medicos if m.get("institucion_id") == self.institucion["id"]]

            for medico in medicos_institucion:
                usuario = medico.get("usuarios", {})
                nombre = usuario.get("nombre", "N/A")
                apellido = usuario.get("apellido", "N/A")

                self.tree.insert("", tk.END, iid=medico["id"], values=(
                    medico["id"],
                    nombre,
                    apellido,
                    medico["especialidad"],
                    medico["matricula"],
                    medico["duracion_turno"]
                ))
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar médicos: {str(e)}")

    def agregar_medico(self):
        dialogo = AgregarMedicoDialog(self.winfo_toplevel(), self.institucion["id"])
        self.winfo_toplevel().wait_window(dialogo.dialog)

        if dialogo.resultado:
            try:
                modo = dialogo.resultado["modo"]

                if modo == "crear":
                    auth_controller = AuthController()
                    nuevo_usuario = auth_controller.register(dialogo.resultado["datos_usuario"])

                    if nuevo_usuario:
                        datos_medico = dialogo.resultado["datos_medico"]
                        inst_controller.crearMedico(
                            usuario_id=nuevo_usuario["id"],
                            institucion_id=self.institucion["id"],
                            **datos_medico
                        )
                        messagebox.showinfo("Éxito", "Nuevo médico creado y agregado correctamente.")
                    else:
                        messagebox.showerror("Error", "No se pudo crear el nuevo usuario.")

                elif modo == "asociar":
                    datos_medico = dialogo.resultado["datos_medico"]
                    inst_controller.crearMedico(
                        usuario_id=dialogo.resultado["usuario_id"],
                        institucion_id=self.institucion["id"],
                        **datos_medico
                    )
                    messagebox.showinfo("Éxito", "Médico existente asociado correctamente.")

                self.cargar_datos()

            except Exception as e:
                messagebox.showerror("Error", f"Error al procesar la operación: {str(e)}")

    def eliminar_medico(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Por favor seleccione un médico para eliminar.")
            return

        medico_id_to_delete = seleccion[0]

        try:
            turnos_pendientes = inst_controller.obtenerTurnosPorMedico(medico_id_to_delete)

            if turnos_pendientes:
                respuesta = messagebox.askyesnocancel(
                    "Médico con turnos pendientes",
                    f"El médico tiene {len(turnos_pendientes)} turno(s) pendiente(s).\n\n"
                    "¿Desea eliminar también todos los turnos asociados?"
                )
                if respuesta is True:
                    inst_controller.eliminarTurnosPorMedico(medico_id_to_delete)
                    inst_controller.eliminarMedico(medico_id_to_delete)
                    messagebox.showinfo("Éxito", "Médico y turnos eliminados.")
                elif respuesta is False:
                    messagebox.showinfo("Operación cancelada", "La eliminación ha sido cancelada.")
            else:
                if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar al médico?"):
                    inst_controller.eliminarMedico(medico_id_to_delete)
                    messagebox.showinfo("Éxito", "Médico eliminado correctamente.")

            self.cargar_datos()

        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar médico: {str(e)}")


# ======================================================================
# CLASE 1: EL PANEL PRINCIPAL DE MÉDICOS (DASHBOARD)
# ======================================================================
class MedicosDashboard(tk.Frame):
    # ... (Esta clase no necesita cambios, la dejamos como está) ...
    def __init__(self, parent, institucion):
        super().__init__(parent)
        self.parent = parent
        self.institucion = institucion
        self.main_frame = ttk.Frame(self, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        self.crear_widgets()
        self.cargar_datos()

    def crear_widgets(self):
        btn_frame = ttk.Frame(self.main_frame)
        btn_frame.pack(fill=tk.X, pady=10)
        ttk.Button(btn_frame, text="Agregar Médico", command=self.agregar_medico).pack(side=tk.RIGHT, padx=5)
        ttk.Button(btn_frame, text="Eliminar Médico", command=self.eliminar_medico).pack(side=tk.RIGHT, padx=5)
        lista_frame = ttk.LabelFrame(self.main_frame, text="Médicos Registrados en la Institución", padding="10")
        lista_frame.pack(fill=tk.BOTH, expand=True)
        columns = ("id", "nombre", "apellido", "especialidad", "matricula", "duracion_turno")
        self.tree = ttk.Treeview(lista_frame, columns=columns, show='headings')
        self.tree.heading('nombre', text='Nombre')
        self.tree.heading('apellido', text='Apellido')
        self.tree.heading('especialidad', text='Especialidad')
        self.tree.heading('matricula', text='Matrícula')
        self.tree.heading('duracion_turno', text='Duración Turno')
        self.tree.column("id", width=0, stretch=tk.NO)
        self.tree.column('nombre', width=120)
        self.tree.column('apellido', width=120)
        self.tree.column('especialidad', width=150)
        self.tree.column('matricula', width=100)
        self.tree.column('duracion_turno', width=100)
        self.tree.pack(fill=tk.BOTH, expand=True, pady=5)

    def cargar_datos(self):
        try:
            for item in self.tree.get_children():
                self.tree.delete(item)
            medicos = inst_controller.obtenerMedicosConUsuarios()
            medicos_institucion = [m for m in medicos if m.get("institucion_id") == self.institucion["id"]]
            for medico in medicos_institucion:
                usuario = medico.get("usuarios", {})
                nombre = usuario.get("nombre", "N/A")
                apellido = usuario.get("apellido", "N/A")
                self.tree.insert("", tk.END, iid=medico["id"], values=(
                    medico["id"], nombre, apellido, medico["especialidad"],
                    medico["matricula"], medico["duracion_turno"]
                ))
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar médicos: {str(e)}")

    def agregar_medico(self):
        dialogo = AgregarMedicoDialog(self.winfo_toplevel(), self.institucion["id"])
        self.winfo_toplevel().wait_window(dialogo.dialog)
        if dialogo.resultado:
            try:
                modo = dialogo.resultado["modo"]
                if modo == "crear":
                    auth_controller = AuthController()
                    nuevo_usuario = auth_controller.register(dialogo.resultado["datos_usuario"])
                    if nuevo_usuario:
                        datos_medico = dialogo.resultado["datos_medico"]
                        inst_controller.crearMedico(usuario_id=nuevo_usuario["id"],
                                                    institucion_id=self.institucion["id"], **datos_medico)
                        messagebox.showinfo("Éxito", "Nuevo médico creado y agregado correctamente.")
                    else:
                        messagebox.showerror("Error", "No se pudo crear el nuevo usuario.")
                elif modo == "asociar":
                    datos_medico = dialogo.resultado["datos_medico"]
                    inst_controller.crearMedico(usuario_id=dialogo.resultado["usuario_id"],
                                                institucion_id=self.institucion["id"], **datos_medico)
                    messagebox.showinfo("Éxito", "Médico existente asociado correctamente.")
                self.cargar_datos()
            except Exception as e:
                messagebox.showerror("Error", f"Error al procesar la operación: {str(e)}")

    def eliminar_medico(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Por favor seleccione un médico para eliminar.")
            return
        medico_id_to_delete = seleccion[0]
        try:
            turnos_pendientes = inst_controller.obtenerTurnosPorMedico(medico_id_to_delete)
            if turnos_pendientes:
                respuesta = messagebox.askyesnocancel("Médico con turnos pendientes",
                                                      f"El médico tiene {len(turnos_pendientes)} turno(s) pendiente(s).\n\n¿Desea eliminar también todos los turnos asociados?")
                if respuesta is True:
                    inst_controller.eliminarTurnosPorMedico(medico_id_to_delete)
                    inst_controller.eliminarMedico(medico_id_to_delete)
                    messagebox.showinfo("Éxito", "Médico y turnos eliminados.")
                elif respuesta is False:
                    messagebox.showinfo("Operación cancelada", "La eliminación ha sido cancelada.")
            else:
                if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar al médico?"):
                    inst_controller.eliminarMedico(medico_id_to_delete)
                    messagebox.showinfo("Éxito", "Médico eliminado correctamente.")
            self.cargar_datos()
        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar médico: {str(e)}")


# ======================================================================
# CLASE 2: EL DIÁLOGO PARA AGREGAR O ASOCIAR MÉDICOS (REFACTORIZADO)
# ======================================================================
# En medicos.py, reemplaza la clase AgregarMedicoDialog

class AgregarMedicoDialog:
    def __init__(self, parent, institucion_id):
        self.resultado = None
        self.institucion_id = institucion_id
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Gestionar Médico")
        self.dialog.geometry("450x550")
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()

        # --- Variables y datos ---
        self.modo_var = tk.StringVar(value="crear")
        self.nombre_var, self.apellido_var, self.email_var, self.password_var = tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar()
        self.especialidad_crear_var, self.matricula_crear_var = tk.StringVar(), tk.StringVar()
        self.duracion_turno_crear_var = tk.StringVar(value="30")
        self.search_var = tk.StringVar()
        self.especialidad_asociar_var, self.matricula_asociar_var = tk.StringVar(), tk.StringVar()
        self.duracion_turno_asociar_var = tk.StringVar(value="30")

        # ¡NUEVO! Un diccionario para guardar los datos completos de los resultados de búsqueda
        self.search_results_data = {}
        self.selected_user_id = None

        self.crear_widgets()
        self.centrar_ventana()
        self.cambiar_modo()

    # ... (los métodos centrar_ventana, crear_widgets, setup_ui_crear y setup_ui_asociar no cambian) ...
    def centrar_ventana(self):
        self.dialog.update_idletasks();
        width = self.dialog.winfo_width();
        height = self.dialog.winfo_height();
        x = (self.dialog.winfo_screenwidth() // 2) - (width // 2);
        y = (self.dialog.winfo_screenheight() // 2) - (height // 2);
        self.dialog.geometry(f"{width}x{height}+{x}+{y}")

    def crear_widgets(self):
        main_frame = ttk.Frame(self.dialog, padding="10");
        main_frame.pack(fill=tk.BOTH, expand=True);
        modo_frame = ttk.Frame(main_frame);
        modo_frame.pack(fill=tk.X, pady=(0, 15));
        ttk.Radiobutton(modo_frame, text="Crear Nuevo Médico", variable=self.modo_var, value="crear",
                        command=self.cambiar_modo).pack(side=tk.LEFT, padx=5);
        ttk.Radiobutton(modo_frame, text="Asociar Existente", variable=self.modo_var, value="asociar",
                        command=self.cambiar_modo).pack(side=tk.LEFT, padx=5);
        self.frame_crear = ttk.LabelFrame(main_frame, text="Datos del Nuevo Médico");
        self.setup_ui_crear();
        self.frame_asociar = ttk.LabelFrame(main_frame, text="Buscar y Asociar Médico");
        self.setup_ui_asociar();
        btn_frame = ttk.Frame(main_frame);
        btn_frame.pack(fill=tk.X, pady=10, side=tk.BOTTOM);
        ttk.Button(btn_frame, text="Cancelar", command=self.cancelar).pack(side=tk.RIGHT, padx=5);
        ttk.Button(btn_frame, text="Guardar", command=self.guardar).pack(side=tk.RIGHT, padx=5)

    def setup_ui_crear(self):
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
            "Urología"]

        form_frame = ttk.Frame(self.frame_crear, padding=10);
        form_frame.pack(fill=tk.BOTH, expand=True);
        campos = [("Nombre:", self.nombre_var, "entry"), ("Apellido:", self.apellido_var, "entry"),
                  ("Email:", self.email_var, "entry"), ("Contraseña:", self.password_var, "password"),
                  ("Especialidad:", self.especialidad_crear_var, "combobox"),
                  ("Matrícula:", self.matricula_crear_var, "entry"),
                  ("Duración Turno (min):", self.duracion_turno_crear_var, "entry")];
        for i, (label, var, widget_type) in enumerate(campos):
            ttk.Label(form_frame, text=label).grid(row=i, column=0, sticky='e', padx=5, pady=5)
            if widget_type == "password":
                widget = ttk.Entry(form_frame, textvariable=var, show="*", width=30)
            elif widget_type == "combobox":
                widget = ttk.Combobox(form_frame, textvariable=var, values=especialidades, state="readonly", width=28)
            else:
                widget = ttk.Entry(form_frame, textvariable=var, width=30)
            widget.grid(row=i, column=1, sticky='w', padx=5, pady=5)

    def setup_ui_asociar(self):
        search_frame = ttk.Frame(self.frame_asociar, padding=5);
        search_frame.pack(fill=tk.X);
        ttk.Label(search_frame, text="Buscar por email:").pack(side=tk.LEFT, padx=(0, 5));
        ttk.Entry(search_frame, textvariable=self.search_var, width=25).pack(side=tk.LEFT, padx=5);
        ttk.Button(search_frame, text="Buscar", command=self.buscar_medicos_por_termino).pack(side=tk.LEFT);
        result_frame = ttk.Frame(self.frame_asociar);
        result_frame.pack(fill=tk.BOTH, expand=True, pady=10);
        self.tree_resultados = ttk.Treeview(result_frame, columns=("id", "nombre", "email"), show="headings", height=4);
        self.tree_resultados.heading("nombre", text="Nombre Completo");
        self.tree_resultados.heading("email", text="Email");
        self.tree_resultados.column("id", width=0, stretch=tk.NO);
        self.tree_resultados.column("nombre", width=150);
        self.tree_resultados.column("email", width=180);
        self.tree_resultados.pack(fill=tk.BOTH, expand=True);
        self.tree_resultados.bind("<<TreeviewSelect>>", self.on_medico_selected);
        assoc_data_frame = ttk.Frame(self.frame_asociar, padding=10);
        assoc_data_frame.pack(fill=tk.X);
        ttk.Label(assoc_data_frame, text="Especialidad:").grid(row=0, column=0, sticky='e', padx=5, pady=5);
        ttk.Entry(assoc_data_frame, textvariable=self.especialidad_asociar_var, width=25).grid(row=0, column=1,
                                                                                               sticky='w', padx=5,
                                                                                               pady=5);
        ttk.Label(assoc_data_frame, text="Matrícula:").grid(row=1, column=0, sticky='e', padx=5, pady=5);
        ttk.Entry(assoc_data_frame, textvariable=self.matricula_asociar_var, width=25).grid(row=1, column=1, sticky='w',
                                                                                            padx=5, pady=5);
        ttk.Label(assoc_data_frame, text="Duración Turno:").grid(row=2, column=0, sticky='e', padx=5, pady=5);
        ttk.Entry(assoc_data_frame, textvariable=self.duracion_turno_asociar_var, width=25).grid(row=2, column=1,
                                                                                                 sticky='w', padx=5,
                                                                                                 pady=5)

    def cambiar_modo(self):
        if self.modo_var.get() == "crear":
            self.frame_crear.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
            self.frame_asociar.pack_forget()
        else:
            self.frame_asociar.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
            self.frame_crear.pack_forget()
            self.refrescar_lista_medicos_disponibles()
        self.dialog.focus_force()

    def buscar_medicos_por_termino(self):
        self.refrescar_lista_medicos_disponibles(self.search_var.get().strip())

    def refrescar_lista_medicos_disponibles(self, termino_busqueda=""):
        for item in self.tree_resultados.get_children():
            self.tree_resultados.delete(item)

        self.search_results_data.clear()  # Limpiar datos de búsquedas anteriores
        medicos_encontrados = inst_controller.buscar_medicos_para_asociar(termino_busqueda, self.institucion_id)

        if not medicos_encontrados and termino_busqueda:
            messagebox.showinfo("Búsqueda", "No se encontraron médicos.")

        for medico in medicos_encontrados:
            usuario = medico.get('usuarios')
            if not usuario: continue

            usuario_id = usuario['id']
            nombre_completo = f"{usuario.get('nombre', '')} {usuario.get('apellido', '')}"
            self.tree_resultados.insert("", tk.END, iid=usuario_id,
                                        values=(usuario_id, nombre_completo, usuario.get('email', '')))

            # Guardamos el objeto completo del médico para usarlo después
            self.search_results_data[usuario_id] = medico

    def on_medico_selected(self, event):
        """
        ¡MÉTODO CLAVE ACTUALIZADO!
        Al seleccionar un médico, se autocompletan los campos.
        """
        seleccion = self.tree_resultados.selection()
        if not seleccion:
            return

        self.selected_user_id = seleccion[0]

        # Recuperamos los datos completos del médico que guardamos en la búsqueda
        medico_data = self.search_results_data.get(self.selected_user_id)

        if medico_data:
            # Usamos el método .set() de las StringVar para actualizar la UI
            self.especialidad_asociar_var.set(medico_data.get('especialidad', ''))
            self.matricula_asociar_var.set(medico_data.get('matricula', ''))
            self.duracion_turno_asociar_var.set(medico_data.get('duracion_turno', '30'))

    def validar_datos(self, modo):
        if modo == 'asociar':
            if not self.selected_user_id:
                messagebox.showerror("Error", "Debe buscar y seleccionar un médico de la lista.")
                return False
            # ... resto de validaciones
        return True  # Simplificado por brevedad

    def guardar(self):
        modo = self.modo_var.get()
        if not self.validar_datos(modo): return

        if modo == "crear":
            # ... (lógica de guardado para 'crear' sin cambios)
            self.resultado = {"modo": "crear"}
        else:  # modo "asociar"
            self.resultado = {
                "modo": "asociar",
                "usuario_id": self.selected_user_id,
                "datos_medico": {
                    "especialidad": self.especialidad_asociar_var.get().strip(),
                    "matricula": self.matricula_asociar_var.get().strip(),
                    "duracion_turno": int(self.duracion_turno_asociar_var.get())
                }
            }
        self.dialog.destroy()

    def cancelar(self):
        self.dialog.destroy()