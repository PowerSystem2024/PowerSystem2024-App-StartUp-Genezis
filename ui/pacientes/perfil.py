from tkinter import *
from tkinter import messagebox


class PerfilFrame(Frame):
    def __init__(self, parent, paciente_id=None, volver_callback=None):
        super().__init__(parent)
        self.paciente_id = paciente_id
        self.volver_callback = volver_callback

        # Título
        Label(self, text="Perfil del Paciente", font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=10)

        # Campos para completar
        self.campos = {
            "ID": StringVar(),
            "Nombres": StringVar(),
            "Apellidos": StringVar(),
            "Fecha de Nacimiento": StringVar(),
            "Género": StringVar(),
            "Obra Social / Seguro": StringVar(),
            "Número de Afiliado": StringVar(),
            "Fecha de Creación": StringVar(),
            "Última Modificación": StringVar(),
        }

        # Etiquetas y campos de entrada con campos de solo lectura
        self.entries = {}

        for idx, (label, var) in enumerate(self.campos.items()):
            Label(self, text=label + ":").grid(row=idx + 1, column=0, sticky=E, padx=5, pady=2)
            entry = Entry(self, textvariable=var, width=40)

            # Desactivar los campos de solo lectura
            if label in ["ID", "Fecha de Creación", "Última Modificación"]:
                entry.config(state=DISABLED)

            entry.grid(row=idx + 1, column=1, sticky=W, padx=5, pady=2)
            self.entries[label] = entry


        # Botón para guardar cambios
        Button(self, text="Guardar Cambios", command=self.guardar_cambios).grid(
            row=len(self.campos) + 1, column=0, columnspan=2, pady=10
        )

        # Botón "Atrás"
        Button(self, text="Atrás", command=self.volver_callback).grid(
            row=len(self.campos) + 2, column=0, columnspan=2, pady=5
        )

        # No se cargan datos si no hay paciente
        if paciente_id:
            self.campos["ID"].set(str(paciente_id))

    def cargar_datos(self, paciente):
        self.campos["ID"].set(paciente.get("id", ""))
        self.campos["Nombres"].set(paciente.get("nombres", ""))
        self.campos["Apellidos"].set(paciente.get("apellidos", ""))
        self.campos["Fecha de Nacimiento"].set(paciente.get("fecha_nacimiento", ""))
        self.campos["Género"].set(paciente.get("genero", ""))
        self.campos["Obra Social / Seguro"].set(paciente.get("obra_social", ""))
        self.campos["Número de Afiliado"].set(paciente.get("numero_afiliado", ""))
        self.campos["Fecha de Creación"].set(paciente.get("fecha_creacion", ""))
        self.campos["Última Modificación"].set(paciente.get("ultima_modificacion", ""))

    def obtener_datos(self):
        return {campo: var.get() for campo, var in self.campos.items()}

    def guardar_cambios(self):
        datos = self.obtener_datos()
        print("Simulando guardado:", datos)
        messagebox.showinfo("Guardar", "¡Datos actualizados correctamente!")
