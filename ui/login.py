import tkinter as tk
from tkinter import ttk, messagebox
from controllers.auth_controller import AuthController

class LoginFrame(ttk.Frame):
    """Pantalla de inicio de sesión"""
    
    def __init__(self, parent, on_login_success):
        super().__init__(parent)
        self.parent = parent
        self.on_login_success = on_login_success
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
        title_label = ttk.Label(main_frame, text="Sistema de Turnos Médicos", font=("Arial", 18, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Campos de entrada
        ttk.Label(main_frame, text="Email:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.email_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.email_var, width=30).grid(row=1, column=1, pady=5)
        
        ttk.Label(main_frame, text="Contraseña:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.password_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.password_var, show="*", width=30).grid(row=2, column=1, pady=5)
        
        # Botón de inicio de sesión
        login_button = ttk.Button(main_frame, text="Iniciar Sesión", command=self.login)
        login_button.grid(row=3, column=0, columnspan=2, pady=(20, 0))
        
        # Botón de registro
        register_button = ttk.Button(main_frame, text="Registrarse", command=self.parent.show_register)
        register_button.grid(row=4, column=0, columnspan=2, pady=(10, 0))
    
    def login(self):
        """Procesar inicio de sesión"""
        email = self.email_var.get()
        password = self.password_var.get()
        
        if not email or not password:
            messagebox.showerror("Error", "Por favor, complete todos los campos")
            return
        
        # Intentar iniciar sesión
        user = self.auth_controller.login(email, password)
        
        if user:
            # Login exitoso
            self.on_login_success(user)
        else:
            # Login fallido
            messagebox.showerror("Error", "Email o contraseña incorrectos")