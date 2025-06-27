# file: ui/medicos/datosMedico.py

import tkinter as tk
from tkinter import ttk, messagebox
import controllers.med_controller as med_controller


class DatosMedicoWindow(tk.Toplevel):
    def __init__(self, parent, user_data, medico_info):
        super().__init__(parent)
        self.title(f"Editar Mi Perfil - Dr(a). {user_data.get('apellido')}")
        self.geometry("450x550")
        self.resizable(False, False)
        self.configure(padx=15, pady=15)
        self.grab_set()  # Para hacer la ventana modal

        self.user_data = user_data
        self.medico_info = medico_info
        self.medico_id_db = self.medico_info.get("id")

        self.setup_ui()
        self.populate_fields()

    def setup_ui(self):
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True)

        datos_frame = ttk.LabelFrame(main_frame, text=" Mis Datos Personales y Profesionales ", padding=(10, 5))
        datos_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        datos_frame.columnconfigure(1, weight=1)

        self.fields = {}
        especialidades = [
            "Cardiología", "Dermatología", "Endocrinología", "Gastroenterología", "Ginecología",
            "Medicina General", "Medicina Interna", "Neurología", "Oftalmología", "Oncología",
            "Ortopedia", "Otorrinolaringología", "Pediatría", "Psiquiatría", "Urología"
        ]

        # Configuración de campos
        field_configs = [
            ("nombre", "Nombre:"), ("apellido", "Apellido:"), ("email", "Email:"),
            ("matricula", "Matrícula:"), ("duracion_turno", "Duración Turno (min):")
        ]

        for i, (field, label) in enumerate(field_configs):
            ttk.Label(datos_frame, text=label).grid(row=i, column=0, sticky="w", padx=5, pady=5)
            entry = ttk.Entry(datos_frame)
            entry.grid(row=i, column=1, sticky="ew", padx=5, pady=5)
            self.fields[field] = entry

        # Combobox Especialidad
        row_especialidad = len(field_configs)
        ttk.Label(datos_frame, text="Especialidad:").grid(row=row_especialidad, column=0, sticky="w", padx=5, pady=5)
        self.fields["especialidad_var"] = tk.StringVar()
        especialidad_combo = ttk.Combobox(datos_frame, textvariable=self.fields["especialidad_var"],
                                          values=especialidades, state="readonly")
        especialidad_combo.grid(row=row_especialidad, column=1, sticky="ew", padx=5, pady=5)

        # Combobox Institución
        instituciones = med_controller.obtener_instituciones()
        self.institucion_map = {"(Ninguna)": None}
        institucion_options = ["(Ninguna)"]
        if instituciones:
            for inst in instituciones:
                institucion_options.append(inst.get("nombre"))
                self.institucion_map[inst.get("nombre")] = inst.get("id")

        ttk.Label(datos_frame, text="Institución (Opcional):").grid(row=row_especialidad + 1, column=0, sticky="w",
                                                                    padx=5, pady=5)
        self.fields["institucion_id_var"] = tk.StringVar()
        institucion_combo = ttk.Combobox(datos_frame, textvariable=self.fields["institucion_id_var"],
                                         values=institucion_options, state="readonly")
        institucion_combo.grid(row=row_especialidad + 1, column=1, sticky="ew", padx=5, pady=5)

        # Sección de contraseña
        pass_frame = ttk.LabelFrame(main_frame, text=" Cambiar Contraseña (Opcional) ", padding=(10, 5))
        pass_frame.grid(row=1, column=0, sticky="ew")
        pass_frame.columnconfigure(1, weight=1)

        self.password_fields = {}
        password_configs = [("nueva_password", "Nueva Contraseña:"), ("confirmar_password", "Confirmar Contraseña:")]
        for i, (field, label) in enumerate(password_configs):
            ttk.Label(pass_frame, text=label).grid(row=i, column=0, sticky="w", padx=5, pady=5)
            entry = ttk.Entry(pass_frame, show="*")
            entry.grid(row=i, column=1, sticky="ew", padx=5, pady=5)
            self.password_fields[field] = entry

        save_button = ttk.Button(main_frame, text="Guardar Cambios", command=self.submit)
        save_button.grid(row=2, column=0, pady=(20, 0))

    def populate_fields(self):
        # Poblar campos de texto
        self.fields["nombre"].insert(0, self.user_data.get("nombre", ""))
        self.fields["apellido"].insert(0, self.user_data.get("apellido", ""))
        self.fields["email"].insert(0, self.user_data.get("email", ""))
        self.fields["matricula"].insert(0, self.medico_info.get("matricula", ""))
        duracion_turno = self.medico_info.get("duracion_turno")
        if duracion_turno is not None:
            self.fields["duracion_turno"].insert(0, str(duracion_turno))

        # Poblar combobox
        self.fields["especialidad_var"].set(self.medico_info.get("especialidad", ""))

        current_institucion_id = self.medico_info.get("institucion_id")
        current_institucion_name = "(Ninguna)"
        for name, id_ in self.institucion_map.items():
            if id_ == current_institucion_id:
                current_institucion_name = name
                break
        self.fields["institucion_id_var"].set(current_institucion_name)

    def submit(self):
        nuevos_datos_usuario = {
            "nombre": self.fields["nombre"].get().strip(),
            "apellido": self.fields["apellido"].get().strip(),
            "email": self.fields["email"].get().strip()
        }

        institucion_nombre_sel = self.fields["institucion_id_var"].get()
        institucion_id_db = self.institucion_map.get(institucion_nombre_sel)

        duracion_val = self.fields["duracion_turno"].get().strip()
        try:
            duracion_int = int(duracion_val) if duracion_val else None
        except ValueError:
            messagebox.showwarning("Dato Inválido", "La duración del turno debe ser un número entero.", parent=self)
            return

        nuevos_datos_medico = {
            "especialidad": self.fields["especialidad_var"].get().strip(),
            "matricula": self.fields["matricula"].get().strip(),
            "institucion_id": institucion_id_db,
            "duracion_turno": duracion_int
        }

        try:
            med_controller.actualizar_usuario(self.user_data['id'], nuevos_datos_usuario)
            med_controller.actualizar_medico(self.medico_id_db, nuevos_datos_medico)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron guardar los cambios:\n{e}", parent=self)
            return

        # Manejo de contraseña
        password_updated = False
        nueva_pass = self.password_fields["nueva_password"].get().strip()
        if nueva_pass:
            if nueva_pass != self.password_fields["confirmar_password"].get().strip():
                messagebox.showwarning("Contraseñas no coinciden", "Las contraseñas no son iguales.", parent=self)
                return
            try:
                med_controller.admin_actualizar_password_usuario(self.user_data['id'], nueva_pass)
                password_updated = True
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo actualizar la contraseña:\n{e}", parent=self)
                return

        if password_updated:
            messagebox.showinfo("Éxito", "Tus datos y contraseña han sido actualizados.", parent=self)
        else:
            messagebox.showinfo("Éxito", "Tus datos han sido actualizados.", parent=self)

        self.destroy()