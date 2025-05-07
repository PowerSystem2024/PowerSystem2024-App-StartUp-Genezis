from pathlib import Path
from tkinter import Frame, Canvas, Entry, Button, PhotoImage, messagebox
from controllers.auth_controller import AuthController

# Definición de rutas para los recursos
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = Path(__file__).parent / "common/assets/login"

def relative_to_assets(path: str) -> Path:
    full_path = ASSETS_PATH / Path(path)
    print(f"Cargando imagen desde: {full_path}")  # Depuración
    return full_path

class LoginInterface(Frame):
    def __init__(self, parent, on_login_success):
        super().__init__(parent)
        self.parent = parent
        self.on_login_success = on_login_success
        self.auth_controller = AuthController()
        self.configure(bg="#FFFFFF")

        # Guardamos referencias a las imágenes como atributos de la clase
        self.images = {}

        # Creación del lienzo principal (ahora usando Canvas en lugar de Frame)
        self.canvas = Canvas(
            self,
            bg="#FFFFFF",
            height=587,
            width=895,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)

        try:
            # Imagen de fondo
            self.images["image_1"] = PhotoImage(file=relative_to_assets("image_1.png"))
            self.canvas.create_image(224.0, 293.0, image=self.images["image_1"])

            # Botón 1
            self.images["button_1"] = PhotoImage(file=relative_to_assets("button_1.png"))
            button_1 = Button(
                self,
                image=self.images["button_1"],
                borderwidth=0,
                highlightthickness=0,
                command=self.parent.show_register,
                relief="flat"
            )
            button_1.place(x=690.0, y=372.0, width=118.0, height=40.0)

            # Botón 2
            self.images["button_2"] = PhotoImage(file=relative_to_assets("button_2.png"))
            button_2 = Button(
                self,
                image=self.images["button_2"],
                borderwidth=0,
                highlightthickness=0,
                command=self.handle_login,
                relief="flat"
            )
            button_2.place(x=555.0, y=372.0, width=118.0, height=40.0)

            # Campos de entrada - Correo
            self.images["entry_1"] = PhotoImage(file=relative_to_assets("entry_1.png"))
            entry_bg_1 = self.canvas.create_image(681.5, 322.0, image=self.images["entry_1"])
            self.password_entry = Entry(
                self,
                bd=0,
                bg="#D9D9D9",
                fg="#000716",
                highlightthickness=0,
                font=("Inter", 14),
                justify="center",
                show="*"
            )
            self.password_entry.place(x=555.0, y=302.0, width=253.0, height=38.0)

            # Campos de entrada - Contraseña
            self.images["entry_2"] = PhotoImage(file=relative_to_assets("entry_2.png"))
            entry_bg_2 = self.canvas.create_image(681.5, 273.0, image=self.images["entry_2"])
            self.username_entry = Entry(
                self,
                bd=0,
                bg="#D9D9D9",
                fg="#000716",
                highlightthickness=0,
                font=("Inter", 14),
                justify="center"
            )
            self.username_entry.place(x=555.0, y=253.0, width=253.0, height=38.0)

            # Texto principal
            self.canvas.create_text(
                590.0,
                182.0,
                anchor="nw",
                text="Turnos Medicos",
                fill="#000000",
                font=("Inter SemiBold", 24)
            )

        except Exception as e:
            print(f"Error al cargar recursos: {e}")
            messagebox.showerror("Error", f"Error al cargar la interfaz: {str(e)}")

    def handle_login(self):
        # Implementar la lógica de login aquí
        print("button_1 clicked Login")

        email = self.username_entry.get()
        password = self.password_entry.get()

        if not email or not password:
            messagebox.showerror("Error", "Por favor, complete todos los campos")
            return

        # Intentamos Iniciar Seccion
        user = self.auth_controller.login(email, password)

        if user:
            # Login exitoso
            self.on_login_success(user)
        else:
            # Login fallido
            messagebox.showerror("Error", "Email o contraseña incorrectos")
        pass

    def handle_register(self):
        # Implementar la lógica de register aquí
        print("button_1 clicked register")

        pass