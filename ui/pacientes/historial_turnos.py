from tkinter import *
from tkinter import ttk, messagebox
from controllers.pac_controller import obtener_historial_turnos
from datetime import datetime

class HistorialTurnosFrame(Frame):
    def __init__(self, parent, paciente_id, volver_callback):
        super().__init__(parent)
        self.paciente_id = paciente_id
        self.volver_callback = volver_callback

        Label(self, text="Historial de Turnos", font=("Arial", 16, "bold")).pack(pady=10)

        columns = ("fecha", "hora", "medico", "especialidad", "estado")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=5)  # ← Cambiado de 12 a 5

        self.tree.heading("fecha", text="Fecha")
        self.tree.heading("hora", text="Hora")
        self.tree.heading("medico", text="Médico")
        self.tree.heading("especialidad", text="Especialidad")
        self.tree.heading("estado", text="Estado")

        for col in columns:
            self.tree.column(col, anchor=CENTER, width=120)

        self.tree.pack(pady=(5, 10), padx=10)  # ← Eliminado expand=True para evitar que se estire

        Button(self, text="Atrás", command=self.volver_callback).pack(pady=5)

        self.cargar_historial_turnos()

    def cargar_historial_turnos(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            historial = obtener_historial_turnos(self.paciente_id)
            turnos = historial.get("proximos", []) + historial.get("pasados", [])
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los turnos: {e}")
            return

        if not turnos:
            messagebox.showinfo("Información", "No se encontraron turnos en el historial.")
            return

        for turno in turnos:
            # Fecha con formato DD-MM-YYYY
            fecha_raw = turno.get("fecha", "")[:10]
            try:
                fecha = datetime.strptime(fecha_raw, "%Y-%m-%d").strftime("%d-%m-%Y")
            except ValueError:
                fecha = fecha_raw

            hora = turno.get("hora_inicio", "")

            medico_info = turno.get("medico", {})
            usuario_info = medico_info.get("usuario", {})
            nombre = usuario_info.get("nombre", "").strip()
            apellido = usuario_info.get("apellido", "").strip()
            nombre_medico = f"Dr. {nombre} {apellido}".strip() if nombre or apellido else "Desconocido"

            especialidad = medico_info.get("especialidad", "No especificada")
            estado = turno.get("estado", "Desconocido")

            self.tree.insert("", END, values=(fecha, hora, nombre_medico, especialidad, estado))
