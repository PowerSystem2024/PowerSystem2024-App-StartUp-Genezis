from tkinter import *
from tkinter import messagebox
from controllers.pac_controller import get_paciente_por_usuario_id

class PerfilFrame(Frame):
    def __init__(self, parent, paciente_id=None, volver_callback=None):
        super().__init__(parent)
        self.paciente_id = paciente_id
        self.volver_callback = volver_callback
        self.modo_edicion = False

        # Título
        Label(self, text="Perfil del Paciente", font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=10)

        # Campos para completar
        self.campos = {
            "Nombres": StringVar(),
            "Apellidos": StringVar(),
            "Fecha de Nacimiento": StringVar(),
            "Género": StringVar(),
            "Obra Social / Seguro": StringVar(),
            "Número de Afiliado": StringVar(),

        }

        # Etiquetas y campos de entrada con campos de solo lectura
        self.entries = {}

        for idx, (label, var) in enumerate(self.campos.items()):
            Label(self, text=label + ":").grid(row=idx + 1, column=0, sticky=E, padx=5, pady=2)
            entry = Entry(self, textvariable=var, width=40)

            if label in ["ID", "Fecha de Creación", "Última Modificación"]:
                entry.config(state=DISABLED)
            else:
                entry.config(state=DISABLED)  # ← Desactivamos todos los campos por defecto

            entry.grid(row=idx + 1, column=1, sticky=W, padx=5, pady=2)
            self.entries[label] = entry

        # Botón para guardar cambios (lo creamos pero NO lo mostramos al inicio)
        self.btn_guardar = Button(self, text="Guardar Cambios", command=self.guardar_cambios)



        # Botón "Editar Datos"
        Button(self, text="Editar Datos", command=self.habilitar_edicion).grid(
            row=len(self.campos) + 2, column=0, columnspan=2, pady=5
        )

        # Botón "Atrás"
        Button(self, text="Atrás", command=self.volver_callback).grid(
            row=len(self.campos) + 3, column=0, columnspan=2, pady=5
        )

        self.obtener_datos_desde_supabase(self.paciente_id)


    def cargar_datos(self, paciente):
            self.campos["Nombres"].set(paciente.get("nombre", ""))
            self.campos["Apellidos"].set(paciente.get("apellido", ""))
            self.campos["Fecha de Nacimiento"].set(paciente.get("fecha_nacimiento", ""))
            self.campos["Género"].set(paciente.get("genero", ""))
            self.campos["Obra Social / Seguro"].set(paciente.get("obra_social", ""))
            self.campos["Número de Afiliado"].set(paciente.get("num_afiliado", ""))


    def obtener_datos(self):
        return {campo: var.get() for campo, var in self.campos.items()}

    def guardar_cambios(self):
        datos = self.obtener_datos()
        print("Simulando guardado:", datos)
        messagebox.showinfo("Guardar", "¡Datos actualizados correctamente!")

    def habilitar_edicion(self):
        campos_editables = [
            "Nombres", "Apellidos", "Fecha de Nacimiento",
            "Género", "Obra Social / Seguro"
        ]
        for campo in campos_editables:
            self.entries[campo].config(state=NORMAL)
        self.modo_edicion = True
        self.btn_guardar.grid(row=len(self.campos) + 1, column=0, columnspan=2, pady=10)

    def obtener_datos_desde_supabase(self, usuario_id):
        paciente = get_paciente_por_usuario_id(usuario_id)
        if paciente:
            self.paciente_id = paciente["id"]  # Guardamos el ID real del paciente
            self.cargar_datos(paciente)
        else:
            messagebox.showerror("Error", "No se pudieron cargar los datos del paciente.")

