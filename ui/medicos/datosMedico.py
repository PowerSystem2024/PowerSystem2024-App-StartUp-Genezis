# file: ui/medicos/datosMedico.py

import tkinter as tk
from tkinter import ttk, messagebox
import controllers.med_controller as med_controller
import controllers.auth_controller as auth_controller  # Import the auth_controller


class DatosMedicoWindow(tk.Toplevel):
    def __init__(self, parent, user_data, medico_info):
        super().__init__(parent)
        self.title(f"Editar Mi Perfil - Dr(a). {user_data.get('apellido')}")
        self.geometry("450x450")  # Adjusted geometry
        self.resizable(False, False)
        self.configure(padx=15, pady=15)
        self.grab_set()  # Para hacer la ventana modal

        self.user_data = user_data
        self.medico_info = medico_info
        self.medico_id_db = self.medico_info.get("id")
        self.auth_controller = auth_controller.AuthController()  # Initialize AuthController

        self.setup_ui()
        self.populate_fields()

    def setup_ui(self):
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True)

        datos_frame = ttk.LabelFrame(main_frame, text=" Mis Datos Personales ", padding=(10, 5))  # Changed label
        datos_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        datos_frame.columnconfigure(1, weight=1)

        self.fields = {}

        # Configuración de campos (solo nombre, apellido, email)
        field_configs = [
            ("nombre", "Nombre:"),
            ("apellido", "Apellido:"),
            ("email", "Email:")
        ]

        for i, (field, label) in enumerate(field_configs):
            ttk.Label(datos_frame, text=label).grid(row=i, column=0, sticky="w", padx=5, pady=5)
            entry = ttk.Entry(datos_frame)
            entry.grid(row=i, column=1, sticky="ew", padx=5, pady=5)
            self.fields[field] = entry

        # Sección de contraseña
        pass_frame = ttk.LabelFrame(main_frame, text=" Cambiar Contraseña (Opcional) ", padding=(10, 5))
        pass_frame.grid(row=1, column=0, sticky="ew")
        pass_frame.columnconfigure(1, weight=1)

        self.password_fields = {}
        password_configs = [
            ("current_password", "Contraseña Actual:"),  # New field
            ("nueva_password", "Nueva Contraseña:"),
            ("confirmar_password", "Confirmar Contraseña:")
        ]
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

    def submit(self):
        nuevos_datos_usuario = {
            "nombre": self.fields["nombre"].get().strip(),
            "apellido": self.fields["apellido"].get().strip(),
            "email": self.fields["email"].get().strip()
        }

        try:
            med_controller.actualizar_usuario(self.user_data['id'], nuevos_datos_usuario)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron guardar los cambios de usuario:\n{e}", parent=self)
            return

        # Manejo de contraseña
        password_updated = False
        current_pass = self.password_fields["current_password"].get().strip()
        nueva_pass = self.password_fields["nueva_password"].get().strip()
        confirm_pass = self.password_fields["confirmar_password"].get().strip()

        if current_pass or nueva_pass or confirm_pass:  # Only proceed if any password field is touched
            if not current_pass:
                messagebox.showwarning("Faltan datos",
                                       "Para cambiar la contraseña, debe introducir la contraseña actual.", parent=self)
                return

            # Verify current password
            # We need to re-fetch the user data to get the latest hashed password
            # or pass the hashed password from the initial login.
            # For simplicity, I'm using the login function from auth_controller.
            # In a real app, you might have the hashed password readily available in self.user_data
            # and use security_utils.verify_password directly.

            # Temporary user dict for login verification
            temp_user = self.auth_controller.login(self.user_data['email'], current_pass)

            if not temp_user:
                messagebox.showwarning("Contraseña incorrecta", "La contraseña actual introducida no es correcta.",
                                       parent=self)
                return

            if not nueva_pass:
                messagebox.showwarning("Faltan datos", "La nueva contraseña no puede estar vacía.", parent=self)
                return

            if nueva_pass != confirm_pass:
                messagebox.showwarning("Contraseñas no coinciden", "Las nuevas contraseñas no son iguales.",
                                       parent=self)
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