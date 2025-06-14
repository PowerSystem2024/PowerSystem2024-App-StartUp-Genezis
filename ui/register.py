import tkinter as tk
from tkinter import ttk, messagebox
import datetime  # Importamos el módulo datetime para manejar la fecha

# Importamos el widget de calendario de la biblioteca tkcalendar
from tkcalendar import DateEntry

# Asumimos que tu controlador está en la carpeta 'controllers'
from controllers.auth_controller import AuthController


class RegisterFrame(ttk.Frame):
    """Pantalla de registro de usuario con selector de fecha."""

    def __init__(self, parent, on_register_success):
        super().__init__(parent)
        self.parent = parent
        self.on_register_success = on_register_success
        self.auth_controller = AuthController()

        self.setup_ui()

    def setup_ui(self):
        """Configurar la interfaz de usuario del formulario de registro."""
        # Configurar estilo
        style = ttk.Style()
        style.configure("TLabel", font=("Arial", 12))
        style.configure("TButton", font=("Arial", 12))
        style.configure("TEntry", font=("Arial", 12))

        # Frame principal centrado
        main_frame = ttk.Frame(self, padding=20)
        main_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Título
        title_label = ttk.Label(main_frame, text="Registro de Paciente", font=("Arial", 18, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # --- Campos de entrada para la tabla 'usuarios' ---
        ttk.Label(main_frame, text="Nombre:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.name_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.name_var, width=30).grid(row=1, column=1, pady=5)

        ttk.Label(main_frame, text="Apellido:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.apellido_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.apellido_var, width=30).grid(row=2, column=1, pady=5)

        ttk.Label(main_frame, text="Email:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.email_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.email_var, width=30).grid(row=3, column=1, pady=5)

        ttk.Label(main_frame, text="Contraseña:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.password_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.password_var, show="*", width=30).grid(row=4, column=1, pady=5)

        # --- Campos de entrada para la tabla 'pacientes' ---
        ttk.Label(main_frame, text="Fecha de Nacimiento:").grid(row=5, column=0, sticky=tk.W, pady=5)
        # Usamos DateEntry en lugar de un Entry normal
        self.fecha_nacimiento_entry = DateEntry(
            main_frame,
            width=28,
            date_pattern='dd/mm/yyyy',  # Formato para mostrar al usuario
            locale='es_AR',  # Calendario en español
            selectmode='day'
        )
        self.fecha_nacimiento_entry.grid(row=5, column=1, pady=5)

        ttk.Label(main_frame, text="Género:").grid(row=6, column=0, sticky=tk.W, pady=5)
        self.genero_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.genero_var, width=30).grid(row=6, column=1, pady=5)

        ttk.Label(main_frame, text="Obra Social:").grid(row=7, column=0, sticky=tk.W, pady=5)
        self.obra_social_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.obra_social_var, width=30).grid(row=7, column=1, pady=5)

        ttk.Label(main_frame, text="Número de Afiliado:").grid(row=8, column=0, sticky=tk.W, pady=5)
        self.num_afiliado_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.num_afiliado_var, width=30).grid(row=8, column=1, pady=5)

        # --- Botón de registro ---
        register_button = ttk.Button(main_frame, text="Registrar", command=self.register)
        register_button.grid(row=9, column=0, columnspan=2, pady=(20, 0))

    def register(self):
        """
        Procesa el registro, recolectando datos, formateando la fecha para la BD,
        y llamando al controlador para realizar la inserción.
        """
        # Recolectar datos de los StringVars y del DateEntry
        name = self.name_var.get()
        apellido = self.apellido_var.get()
        email = self.email_var.get()
        password = self.password_var.get()
        genero = self.genero_var.get()
        obra_social = self.obra_social_var.get()
        num_afiliado = self.num_afiliado_var.get()

        if not all([name, apellido, email, password]):
            messagebox.showerror("Error de Validación",
                                 "Por favor, complete todos los campos obligatorios (Nombre, Apellido, Email, Contraseña).")
            return

        # 1. Obtener la fecha como un objeto `datetime.date`
        fecha_seleccionada = self.fecha_nacimiento_entry.get_date()

        # 2. Formatear la fecha al string 'YYYY-MM-DD' que Supabase necesita
        fecha_para_db = fecha_seleccionada.strftime('%Y-%m-%d')

        # Preparar los diccionarios para el controlador
        user_data = {
            "nombre": name,
            "apellido": apellido,
            "email": email,
            "password": password,
            "tipo": "paciente"
        }

        user_paciente_data = {
            "fecha_nacimiento": fecha_para_db,
            "genero": genero,
            "obra_social": obra_social,
            "num_afiliado": num_afiliado
        }

        # Llamar al método del controlador que orquesta todo
        user = self.auth_controller.register_user_and_paciente(user_data, user_paciente_data)

        if user:
            messagebox.showinfo("Éxito", "Usuario y perfil de paciente registrados correctamente.")
            self.on_register_success()  # Callback para notificar el éxito
        else:
            messagebox.showerror("Error de Registro",
                                 "No se pudo completar el registro. El email podría ya estar en uso o hubo un problema con la base de datos.")