import tkinter as tk
from tkinter import ttk, messagebox
from controllers.auth_controller import AuthController

class RegisterFrame(ttk.Frame):
    """Pantalla de registro de usuario"""
    
    def __init__(self, parent, on_register_success):
        super().__init__(parent)
        self.parent = parent
        self.on_register_success = on_register_success
        self.auth_controller = AuthController()
        
        self.setup_ui()
    
    def setup_ui(self):
        """Configurar interfaz de usuario"""
        # Configurar estilo
        style = ttk.Style()
        style.configure("TLabel", font=("Arial", 12))
        style.configure("TButton", font=("Arial", 12))
        style.configure("TEntry", font=("Arial", 12))
        
        # Frame principal centrado
        main_frame = ttk.Frame(self, padding=20)
        main_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # Título
        title_label = ttk.Label(main_frame, text="Registro de Usuario", font=("Arial", 18, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Campos de entrada
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
        
        ttk.Label(main_frame, text="Tipo de Usuario:").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.user_type_var = tk.StringVar()
        ttk.Combobox(main_frame, textvariable=self.user_type_var, values=["admin", "medico", "paciente", "institucion"], state="readonly", width=28).grid(row=5, column=1, pady=5)
        
        # Botón de registro
        register_button = ttk.Button(main_frame, text="Registrar", command=self.register)
        register_button.grid(row=6, column=0, columnspan=2, pady=(20, 0))
    
    def register(self):
        """Procesar registro"""
        name = self.name_var.get()
        apellido = self.apellido_var.get()
        email = self.email_var.get()
        password = self.password_var.get()
        user_type = self.user_type_var.get()
        
        if not name or not email or not password or not user_type or not apellido:
            messagebox.showerror("Error", "Por favor, complete todos los campos")
            return
        
        # Intentar registrar usuario
        user_data = {
            "nombre": name,
            "email": email,
            "password": password,
            "tipo": user_type,
            "apellido": apellido
        }
        
        user = self.auth_controller.register(user_data)
        
        if user:
            # Registro exitoso
            messagebox.showinfo("Éxito", "Usuario registrado correctamente")
            self.on_register_success()
        else:
            # Registro fallido
            messagebox.showerror("Error", "No se pudo registrar el usuario")