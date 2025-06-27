from tkinter import *
from tkinter import messagebox
from controllers.pac_controller import get_paciente_por_usuario_id, update_paciente
from tkcalendar import DateEntry
from datetime import datetime
from tkinter import ttk


class PerfilFrame(Frame):
    def __init__(self, parent, paciente_id=None, volver_callback=None):
        super().__init__(parent)
        self.paciente_data = None
        self.paciente_id = paciente_id
        self.volver_callback = volver_callback
        self.modo_edicion = False

        # Título
        self.label_titulo = Label(self, text="Perfil del Paciente", font=("Arial", 16, "bold"))
        self.label_titulo.grid(row=0, column=0, columnspan=2, pady=10)

        # Campos para completar
        self.campos = {
            "Nombres": StringVar(),
            "Apellidos": StringVar(),
            "Fecha de Nacimiento": StringVar(),
            "Teléfono": StringVar(),
            "Género": StringVar(),
            "Obra Social / Seguro": StringVar(),
            "Número de Afiliado": StringVar(),

        }

        # Etiquetas y campos de entrada con campos de solo lectura
        self.entries = {}

        for idx, (label, var) in enumerate(self.campos.items()):
            Label(self, text=label + ":").grid(row=idx + 1, column=0, sticky=E, padx=5, pady=2)

            if label == "Fecha de Nacimiento":
                entry = DateEntry(self, width=37, date_pattern="yyyy-mm-dd")
                entry.config(state=DISABLED)


            elif label == "Género":

                opciones_genero = ["Masculino", "Femenino", "Otro"]

                entry = ttk.Combobox(self, textvariable=var, values=opciones_genero, state="readonly", width=37)

                entry.config(state="disabled")

            elif label == "Obra Social / Seguro":
                obras_sociales = [
                    "OSDE", "Swiss Medical", "Galeno", "Medifé", "Omint",
                    "PAMI", "IOMA", "Federada", "Sancor Salud", "Prevención Salud"
                ]
                entry = ttk.Combobox(self, textvariable=var, values=obras_sociales, state="readonly", width=37)
                entry.config(state="disabled")


            else:
                entry = Entry(self, textvariable=var, width=40)
                entry.config(state=DISABLED)

            entry.grid(row=idx + 1, column=1, sticky="ew", padx=10, pady=5)
            self.grid_columnconfigure(1, weight=1)

            self.entries[label] = entry

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

        # Llamada para cargar los datos del paciente
        self.obtener_datos_desde_supabase(self.paciente_id)

    def cargar_datos(self, paciente):
            self.campos["Nombres"].set(paciente.get("nombre", ""))
            self.campos["Apellidos"].set(paciente.get("apellido", ""))
            fecha_str = paciente.get("fecha_nacimiento", "")
            if fecha_str:
                try:
                    fecha_dt = datetime.strptime(fecha_str, "%Y-%m-%d")
                    self.entries["Fecha de Nacimiento"].set_date(fecha_dt)
                except ValueError:
                    pass  # en caso de que el formato no sea válido

            self.campos["Teléfono"].set(paciente.get("telefono", ""))
            self.campos["Género"].set(paciente.get("genero", ""))
            self.campos["Obra Social / Seguro"].set(paciente.get("obra_social", ""))
            self.campos["Número de Afiliado"].set(paciente.get("num_afiliado", ""))

    def obtener_datos(self):
        datos = {}
        for campo, var in self.campos.items():
            if campo == "Fecha de Nacimiento":
                datos[campo] = self.entries[campo].get()  # Obtenemos directamente del DateEntry
            else:
                datos[campo] = var.get()
        return datos

    def guardar_cambios(self):
        if not self.paciente_id:
            messagebox.showerror("Error", "ID de paciente no encontrado.")
            return

        datos = self.obtener_datos()

        nuevos_datos = {
            "fecha_nacimiento": datos["Fecha de Nacimiento"],
            "genero": datos["Género"],
            "obra_social": datos["Obra Social / Seguro"],
            "telefono": datos["Teléfono"],
            "num_afiliado": datos["Número de Afiliado"]
        }

        try:
            update_paciente(self.paciente_id, nuevos_datos)
            messagebox.showinfo("Éxito", "¡Datos actualizados correctamente!")

            # Desactivar todos los campos después del guardado
            for campo, entry in self.entries.items():
                entry.config(state=DISABLED)

            self.btn_guardar.grid_remove()
            self.modo_edicion = False

        except Exception as e:
            print("Error al actualizar paciente:", e)
            messagebox.showerror("Error", "No se pudieron guardar los cambios.")

    def habilitar_edicion(self):
        campos_editables = [
            "Nombres", "Apellidos", "Fecha de Nacimiento", "Teléfono",
            "Género", "Obra Social / Seguro", "Número de Afiliado"
        ]
        for campo in campos_editables:
            self.entries[campo].config(state="normal")
        self.modo_edicion = True
        self.btn_guardar.grid(row=len(self.campos) + 1, column=0, columnspan=2, pady=10)

    def obtener_datos_desde_supabase(self, usuario_id):
        paciente = get_paciente_por_usuario_id(usuario_id)
        if paciente:
            self.paciente_id = paciente["id"]  # Guardamos el ID real del paciente
            self.cargar_datos(paciente)
            self.paciente_data = paciente
            self.label_titulo.config(text=f"Perfil de {paciente['nombre']} {paciente['apellido']}")

        else:
            messagebox.showerror("Error", "No se pudieron cargar los datos del paciente.")

