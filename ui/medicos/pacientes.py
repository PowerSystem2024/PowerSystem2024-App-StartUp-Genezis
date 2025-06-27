import tkinter as tk
from tkinter import ttk, messagebox
from controllers import med_controller

class HistorialTurnosFrame(tk.Toplevel):
    def __init__(self, parent, paciente_id, paciente_nombre):
        super().__init__(parent)
        self.title(f"Historial de Turnos - {paciente_nombre}")
        self.geometry("800x500")
        self.resizable(True, True)

        # Etiqueta del título
        tk.Label(self, text=f"Historial de Turnos: {paciente_nombre}",
                 font=("Arial", 14, "bold")).pack(pady=10)

        # Crear el Treeview para mostrar el historial
        columns = ("fecha", "hora_inicio", "estado", "notas")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")

        # Configurar encabezados
        self.tree.heading("fecha", text="Fecha")
        self.tree.heading("hora_inicio", text="Hora")
        self.tree.heading("estado", text="Estado")
        self.tree.heading("notas", text="Notas")

        # Configurar columnas
        self.tree.column("fecha", width=120, anchor="center")
        self.tree.column("hora_inicio", width=100, anchor="center")
        self.tree.column("estado", width=100, anchor="center")
        self.tree.column("notas", width=400, anchor="w")

        # Añadir scrollbar
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Colocar elementos en la ventana
        self.tree.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y", pady=10)

        # Botón de cerrar
        tk.Button(self, text="Cerrar", command=self.destroy).pack(pady=10)

        # Cargar los datos
        self.cargar_historial(paciente_id)

    def cargar_historial(self, paciente_id):
        # Limpiar el treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            # Obtener el historial del paciente
            turnos = med_controller.obtener_historial_paciente(paciente_id)

            # Verificar si hay turnos
            if not turnos:
                messagebox.showinfo("Información", "Este paciente no tiene turnos registrados.")
                return

            # Insertar los turnos en el treeview
            for turno in turnos:
                fecha = turno.get("fecha", "")
                hora = turno.get("hora_inicio", "")
                estado = turno.get("estado", "")
                notas = turno.get("notas", "")

                self.tree.insert("", "end", values=(fecha, hora, estado, notas))

        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar el historial: {str(e)}")


class PacientesFrame(tk.Frame):
    def __init__(self, parent, medico_id):
        super().__init__(parent)
        self.parent = parent
        self.medico_id = medico_id

        # Título
        tk.Label(self, text="Pacientes", font=("Arial", 16, "bold")).pack(pady=10)

        # Frame para el treeview y scrollbar
        frame_tree = tk.Frame(self)
        frame_tree.pack(fill="both", expand=True, padx=10, pady=5)

        # Crear Treeview
        columns = ("id", "nombre", "obra_social", "numero_afiliado", "ver_historial")
        self.tree = ttk.Treeview(frame_tree, columns=columns, show="headings", height=15)

        # Configurar encabezados
        self.tree.heading("id", text="ID")
        self.tree.heading("nombre", text="Nombre")
        self.tree.heading("obra_social", text="Obra Social")
        self.tree.heading("numero_afiliado", text="Número Afiliado")
        self.tree.heading("ver_historial", text="Historial")

        # Configurar columnas
        self.tree.column("id", width=50, anchor="center")
        self.tree.column("nombre", width=200, anchor="w")
        self.tree.column("obra_social", width=150, anchor="w")
        self.tree.column("numero_afiliado", width=150, anchor="w")
        self.tree.column("ver_historial", width=100, anchor="center")

        # Ocultar la columna ID
        self.tree.column("id", width=0, stretch=tk.NO)



        # Scrollbar vertical
        scrollbar = ttk.Scrollbar(frame_tree, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Colocar treeview y scrollbar
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Vincular evento de clic
        self.tree.bind("<ButtonRelease-1>", self.verificar_clic_historial)

        # Frame para botones
        self.frame_botones = tk.Frame(self)
        self.frame_botones.pack(fill="x", padx=10, pady=10)

        # Botón de actualizar
        self.botones = {}
        self.botones["actualizar"] = tk.Button(
            self.frame_botones,
            text="Actualizar",
            command=self.cargar
        )
        self.botones["actualizar"].pack(side="left", padx=5)

        # Inicialmente cargar datos
        self.cargar()

    def cargar(self):
        # Limpiar el treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            # Obtener pacientes
            pacientes = med_controller.obtener_pacientes_por_medico(self.medico_id)

            # Verificar si hay pacientes
            if not pacientes:
                messagebox.showinfo("Información", "No se encontraron pacientes.")
                return

            # Insertar pacientes en el treeview
            for paciente in pacientes:
                # Combinar apellido y nombre
                nombre_completo = f"{paciente['apellido']}, {paciente['nombre']}"

                values = (
                    paciente["id"],
                    nombre_completo,
                    paciente["obra_social"],
                    paciente["numero_afiliado"],
                    "Ver más"
                )
                item_id = self.tree.insert("", "end", values=values)


        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar pacientes: {str(e)}")

    def verificar_clic_historial(self, event):
        region = self.tree.identify_region(event.x, event.y)
        if region == "cell":
            column = self.tree.identify_column(event.x)
            if column == "#5":  # Quinta columna (Ver historial)
                item = self.tree.focus()
                if item:
                    self.mostrar_historial(item)

    def mostrar_historial(self, item):
        # Obtener datos del paciente seleccionado
        valores = self.tree.item(item, "values")
        paciente_id = valores[0]
        nombre_completo = valores[1]

        # Abrir ventana de historial
        historial_window = HistorialTurnosFrame(self, paciente_id, nombre_completo)
        historial_window.transient(self)
        historial_window.grab_set()
