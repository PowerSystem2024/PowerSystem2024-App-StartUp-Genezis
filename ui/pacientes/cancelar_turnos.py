from tkinter import *
from tkinter import ttk, messagebox
from controllers.pac_controller import obtener_historial_turnos, cancelar_turno

class CancelarTurnosFrame(Frame):
    def __init__(self, parent, paciente_id):
        super().__init__(parent)
        self.parent = parent
        self.paciente_id = paciente_id
        self.turnos_proximos = []

        Label(self, text="Cancelar Turno", font=("Arial", 16, "bold")).pack(pady=10)

        self.tree = ttk.Treeview(
            self,
            columns=("fecha", "hora_inicio", "nombre_medico", "especialidad"),
            show='headings',
            height=10
        )

        self.tree.heading("fecha", text="Fecha")
        self.tree.heading("hora_inicio", text="Hora Inicio")
        self.tree.heading("nombre_medico", text="Médico")
        self.tree.heading("especialidad", text="Especialidad")

        self.tree.column("fecha", anchor="center", width=100)
        self.tree.column("hora_inicio", anchor="center", width=100)
        self.tree.column("nombre_medico", anchor="center", width=200)
        self.tree.column("especialidad", anchor="center", width=150)

        self.tree.pack(padx=10, pady=10)

        Button(self, text="Cancelar Turno Seleccionado", command=self.cancelar_turno_seleccionado).pack(pady=5)

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
            messagebox.showinfo("Sin turnos", "No hay turnos próximos disponibles.")
            return

        for turno in self.turnos_proximos:
            fecha = turno.get("fecha", "")[:10]
            hora = turno.get("hora_inicio", "")
            medico = turno.get("nombre_medico", "Desconocido")
            especialidad = turno.get("especialidad", "Desconocida")

            self.tree.insert("", "end", values=(fecha, hora, medico, especialidad))

    def cancelar_turno_seleccionado(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Por favor, seleccioná un turno para cancelar.")
            return

        item_id = seleccion[0]
        index = self.tree.index(item_id)

        if index >= len(self.turnos_proximos):
            return

        turno = self.turnos_proximos[index]
        turno_id = turno["id"]

        confirmar = messagebox.askyesno("Confirmar", "¿Estás seguro que querés cancelar este turno?")
        if confirmar:
            resultado = cancelar_turno(turno_id, self.paciente_id)

            if resultado.get("exito"):
                messagebox.showinfo("Éxito", resultado["mensaje"])
                self.cargar_turnos()
            else:
                messagebox.showerror("Error", resultado.get("error", "No se pudo cancelar el turno."))
