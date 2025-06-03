import tkinter as tk
from tkinter import ttk, messagebox

# Define la clase UsersFrame, que representa la interfaz de gestión de usuarios.
class UsersFrame(tk.Frame):
    # Constructor de la clase.
    def __init__(self, parent, controller):
        super().__init__(parent) # Inicializa el frame padre.
        self.controller = controller # Guarda una referencia al controlador (AdminController).
        self.setup_ui() # Configura los elementos visuales de la interfaz.
        self.load_users() # Carga los usuarios existentes al iniciar el frame.

    # Configura la interfaz de usuario de la gestión de usuarios.
    def setup_ui(self):
        # Título del panel.
        title = tk.Label(self, text="Gestión de Usuarios", font=("Arial", 14, "bold"))
        title.pack(pady=10)

        # Tabla (Treeview) para mostrar la lista de usuarios.
        self.tree = ttk.Treeview(self, columns=("id", "nombre", "email", "tipo"), show="headings")
        # Define los encabezados de las columnas.
        self.tree.heading("id", text="ID")
        self.tree.heading("nombre", text="Nombre")
        self.tree.heading("email", text="Email")
        self.tree.heading("tipo", text="Tipo")

        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10) # Empaqueta la tabla.

        # Contenedor para los botones CRUD (Crear, Leer, Actualizar, Borrar).
        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)

        # Botones de acción.
        tk.Button(button_frame, text="Crear Usuario", command=self.create_user).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Editar Usuario", command=self.edit_user).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Eliminar Usuario", command=self.delete_user).pack(side=tk.LEFT, padx=5)

    # Carga los usuarios desde el controlador y los muestra en la tabla.
    def load_users(self):
        self.tree.delete(*self.tree.get_children()) # Limpia la tabla existente.
        result = self.controller.get_all_users() # Obtiene todos los usuarios del controlador.
        if result and result.data: # Si hay resultados válidos.
            for user in result.data: # Itera sobre cada usuario.
                # Inserta los datos del usuario en la tabla.
                self.tree.insert("", "end", values=(
                    user.get("id"),
                    user.get("nombre"),
                    user.get("email"),
                    user.get("tipo")
                ))

    # Abre el formulario para crear un nuevo usuario.
    def create_user(self):
        self.open_user_form()

    # Abre el formulario para editar un usuario seleccionado.
    def edit_user(self):
        selected = self.tree.selection() # Obtiene el elemento seleccionado en la tabla.
        if not selected: # Si no hay nada seleccionado, muestra una advertencia.
            messagebox.showwarning("Aviso", "Selecciona un usuario para editar.")
            return

        values = self.tree.item(selected[0])["values"] # Obtiene los valores del usuario seleccionado.
        user_id = values[0] # El ID del usuario.
        user_data = { # Los demás datos del usuario.
            "nombre": values[1],
            "email": values[2],
            "tipo": values[3]
        }
        self.open_user_form(user_id, user_data) # Abre el formulario con los datos para editar.

    # Elimina un usuario seleccionado.
    def delete_user(self):
        selected = self.tree.selection() # Obtiene el elemento seleccionado.
        if not selected: # Si no hay nada seleccionado, muestra una advertencia.
            messagebox.showwarning("Aviso", "Selecciona un usuario para eliminar.")
            return

        user_id = self.tree.item(selected[0])["values"][0] # Obtiene el ID del usuario.
        # Pide confirmación al usuario antes de eliminar.
        confirm = messagebox.askyesno("Confirmar", "¿Estás seguro de que deseas eliminar este usuario?")
        if confirm: # Si el usuario confirma.
            self.controller.delete_user(user_id) # Llama al controlador para eliminar el usuario.
            self.load_users() # Recarga la lista de usuarios.

    # Abre un formulario para crear o editar un usuario.
    def open_user_form(self, user_id=None, user_data=None):
        form = tk.Toplevel(self) # Crea una nueva ventana de nivel superior para el formulario.
        form.title("Formulario de Usuario") # Título de la ventana.
        form.geometry("300x250") # Tamaño de la ventana.

        # Campos de entrada para Nombre, Email y Tipo.
        tk.Label(form, text="Nombre").pack(pady=5)
        entry_nombre = tk.Entry(form)
        entry_nombre.pack()

        tk.Label(form, text="Email").pack(pady=5)
        entry_email = tk.Entry(form)
        entry_email.pack()

        tk.Label(form, text="Tipo").pack(pady=5)
        tipo_var = tk.StringVar() # Variable para almacenar el tipo seleccionado.
        # Combobox para seleccionar el tipo de usuario.
        tipo_combobox = ttk.Combobox(form, textvariable=tipo_var, values=["paciente", "medico", "institucion", "admin"])
        tipo_combobox.pack()

        # Si se están editando datos, precarga los campos con la información existente.
        if user_data:
            entry_nombre.insert(0, user_data["nombre"])
            entry_email.insert(0, user_data["email"])
            tipo_var.set(user_data["tipo"])

        # Función que se ejecuta al enviar el formulario.
        def submit():
            data = { # Recopila los datos de los campos de entrada.
                "nombre": entry_nombre.get(),
                "email": entry_email.get(),
                "tipo": tipo_var.get()
            }

            if user_id: # Si hay un user_id, es una actualización.
                self.controller.update_user(user_id, data)
            else: # De lo contrario, es una creación.
                self.controller.create_user(data)

            form.destroy() # Cierra la ventana del formulario.
            self.load_users() # Recarga la lista de usuarios en la tabla principal.

        # Botón para guardar los cambios o crear el usuario.
        tk.Button(form, text="Guardar", command=submit).pack(pady=10)

        # e