from tkinter import *
from tkinter import messagebox

class PerfilFrame(Frame):
    def __init__(self, parent, paciente_id=None):
        super().__init__(parent)
        self.paciente_id = paciente_id

        #Titulo
        Label(self, text="Perfil del Paciente", font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=10)

        #Campos para completar
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

        #Etiquetas y campos de entrada
        for idx, (label, var) in enumerate(self.campos.items()):
            Label(self, text=label + ":").grid(row=idx + 1, column=0, sticky=E, padx=5, pady=2)
            Entry(self, textvariable=var, width=40).grid(row=idx + 1, column=1, sticky=W, padx=5, pady=2)

        #Boton para guardar cambios
        Button(self, text="Guardar Cambios", command=self.guardar_cambios).grid(row=len(self.campos)+1, column=0, columnspan=2, pady=15)

        # No se cargan datos si no hay paciente
        if paciente_id:
            self.campos["ID"].set(str(paciente_id))

    def cargar_datos(self, paciente):

        #Méttodo para cargar datos en los campos desde un diccionario
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
        """Devuelve los datos del formulario como diccionario."""
        return {campo: var.get() for campo, var in self.campos.items()}

    def guardar_cambios(self):
        datos = self.obtener_datos()
        print("Simulando guardado:", datos) #-
        messagebox.showinfo("Guardar", "¡Datos actualizados correctamente!")

#__
if __name__ == "__main__":
    import tkinter as tk

    root = tk.Tk()
    root.title("Perfil del Paciente")

    frame = PerfilFrame(root)  # Ahora no se pasan datos
    frame.pack(fill="both", expand=True)

    root.mainloop()