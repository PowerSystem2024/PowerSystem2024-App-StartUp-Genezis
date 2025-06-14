import tkinter as tk
from tkinter import ttk, messagebox
import datetime

from tkcalendar import DateEntry
from controllers.auth_controller import AuthController

class RegisterFrame(ttk.Frame):
    """Pantalla de registro de usuario con widgets mejorados."""

    def __init__(self, parent, on_register_success):
        super().__init__(parent)
        self.parent = parent
        self.on_register_success = on_register_success
        self.auth_controller = AuthController()

        self.setup_ui()

    def setup_ui(self):
        """Configurar la interfaz de usuario del formulario de registro."""
        style = ttk.Style()
        style.configure("TLabel", font=("Arial", 12))
        style.configure("TButton", font=("Arial", 12))
        style.configure("TEntry", font=("Arial", 12))
        # Estilo para el nuevo Combobox
        style.configure("TCombobox", font=("Arial", 12))

        main_frame = ttk.Frame(self, padding=20)
        main_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        title_label = ttk.Label(main_frame, text="Registro de Paciente", font=("Arial", 18, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # --- Campos con numeración de filas CORREGIDA ---
        ttk.Label(main_frame, text="Nombre:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.name_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.name_var, width=30).grid(row=1, column=1, pady=5)

        ttk.Label(main_frame, text="Apellido:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.apellido_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.apellido_var, width=30).grid(row=2, column=1, pady=5)

        ttk.Label(main_frame, text="Email:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.email_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.email_var, width=30).grid(row=3, column=1, pady=5)

        # Teléfono ahora en la fila 4
        ttk.Label(main_frame, text="Teléfono:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.telefono_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.telefono_var, width=30).grid(row=4, column=1, pady=5)

        # Contraseña ahora en la fila 5
        ttk.Label(main_frame, text="Contraseña:").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.password_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.password_var, show="*", width=30).grid(row=5, column=1, pady=5)

        # Fecha de Nacimiento ahora en la fila 6
        ttk.Label(main_frame, text="Fecha de Nacimiento:").grid(row=6, column=0, sticky=tk.W, pady=5)
        self.fecha_nacimiento_entry = DateEntry(
            main_frame, width=28, date_pattern='dd/mm/yyyy', locale='es_AR', selectmode='day'
        )
        self.fecha_nacimiento_entry.grid(row=6, column=1, pady=5)

        # --- Género como Combobox en la fila 7 ---
        ttk.Label(main_frame, text="Género:").grid(row=7, column=0, sticky=tk.W, pady=5)
        self.genero_var = tk.StringVar()
        genero_combobox = ttk.Combobox(
            main_frame,
            textvariable=self.genero_var,
            values=["Masculino", "Femenino"],
            width=28,
            state='readonly'  # MUY IMPORTANTE: para que el usuario no pueda escribir otra cosa
        )
        genero_combobox.grid(row=7, column=1, pady=5)
        genero_combobox.set("Masculino") # Opcional: poner un valor por defecto

        # Obra Social ahora en la fila 8
        ttk.Label(main_frame, text="Obra Social:").grid(row=8, column=0, sticky=tk.W, pady=5)
        self.obra_social_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.obra_social_var, width=30).grid(row=8, column=1, pady=5)

        # Número de Afiliado ahora en la fila 9
        ttk.Label(main_frame, text="Número de Afiliado:").grid(row=9, column=0, sticky=tk.W, pady=5)
        self.num_afiliado_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.num_afiliado_var, width=30).grid(row=9, column=1, pady=5)

        # Botón de registro ahora en la fila 10
        register_button = ttk.Button(main_frame, text="Registrar", command=self.register)
        register_button.grid(row=10, column=0, columnspan=2, pady=(20, 0))

    def register(self):
        """Recolecta todos los datos y llama al controlador."""
        # Gracias a que usamos StringVars, obtener el dato del Combobox es igual que de un Entry
        name = self.name_var.get()
        apellido = self.apellido_var.get()
        email = self.email_var.get()
        telefono = self.telefono_var.get()
        password = self.password_var.get()
        genero = self.genero_var.get()
        obra_social = self.obra_social_var.get()
        num_afiliado = self.num_afiliado_var.get()

        if not all([name, apellido, email, password, genero]):
            messagebox.showerror("Error de Validación",
                                 "Por favor, complete todos los campos obligatorios (Nombre, Apellido, Email, Contraseña, Género).")
            return

        fecha_seleccionada = self.fecha_nacimiento_entry.get_date()
        fecha_para_db = fecha_seleccionada.strftime('%Y-%m-%d')

        user_data = {
            "nombre": name, "apellido": apellido, "email": email,
            "password": password, "tipo": "paciente"
        }

        user_paciente_data = {
            "telefono": telefono, "fecha_nacimiento": fecha_para_db,
            "genero": genero, "obra_social": obra_social,
            "num_afiliado": num_afiliado
        }

        user = self.auth_controller.register_user_and_paciente(user_data, user_paciente_data)

        if user:
            messagebox.showinfo("Éxito", "Usuario y perfil de paciente registrados correctamente.")
            self.on_register_success()
        else:
            messagebox.showerror("Error de Registro",
                                 "No se pudo completar el registro. El email podría ya estar en uso o hubo un problema con la base de datos.")