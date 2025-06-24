from tkinter import *
from tkinter import messagebox, ttk
from datetime import datetime
from controllers.pac_controller import obtener_historial_turnos, cancelar_turno

class CancelarTurnosFrame(Frame):
    def __init__(self, parent, paciente_id, volver_callback):
        super().__init__(parent)
        self.parent = parent
        self.paciente_id = paciente_id
        self.volver_callback = volver_callback
        self.turnos_proximos = []

        Label(self, text="Cancelar Turno", font=("Arial", 16, "bold")).pack(pady=10)
        Label(self, text="Seleccione un turno para cancelar", font=("Arial", 11)).pack(pady=(0, 10))

        columns = ("fecha", "hora", "medico", "especialidad")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=10)
        self.tree.heading("fecha", text="Fecha")
        self.tree.heading("hora", text="Hora")
        self.tree.heading("medico", text="Médico")
        self.tree.heading("especialidad", text="Especialidad")

        for col in columns:
            self.tree.column(col, anchor="center", width=150)

        self.tree.pack(pady=10, padx=10, fill=X)
        self.tree.bind("<Double-1>", self.on_double_click)

        # Botón Atrás
        Button(self, text="Atrás", command=self.volver_atras).pack(pady=10)

        self.cargar_turnos()

    def cargar_turnos(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.turnos_proximos = []

        try:
            historial = obtener_historial_turnos(self.paciente_id)
            self.turnos_proximos = historial.get("proximos", [])
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los turnos: {e}")
            return

        if not self.turnos_proximos:
            messagebox.showinfo("Información", "No hay turnos próximos disponibles.")
            return

        for i, turno in enumerate(self.turnos_proximos):
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

            self.tree.insert("", END, iid=i, values=(fecha, hora, nombre_medico, especialidad))

    def on_double_click(self, event):
        item_id = self.tree.identify_row(event.y)
        if not item_id:
            return

        index = int(item_id)
        if index >= len(self.turnos_proximos):
            return

        turno = self.turnos_proximos[index]
        turno_id = turno.get("id")

        confirmar = messagebox.askyesno("Confirmar cancelación", "¿Estás seguro de que querés cancelar este turno?")
        if confirmar:
            resultado = cancelar_turno(turno_id, self.paciente_id)
            if resultado.get("exito"):
                messagebox.showinfo("Éxito", resultado["mensaje"])
                self.cargar_turnos()
            else:
                messagebox.showerror("Error", resultado.get("error", "No se pudo cancelar el turno."))

    def volver_atras(self):
        self.destroy()
        if self.volver_callback:
            self.volver_callback()
