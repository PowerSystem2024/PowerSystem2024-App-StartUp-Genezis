from tkinter import Frame, Label, Button, messagebox
from controllers.pac_controller import confirmar_turno, obtener_historial_turnos

class ConfirmarTurnoFrame(Frame):
    def __init__(self, master, paciente_id, volver_callback):
        super().__init__(master)
        self.paciente_id = paciente_id
        self.volver_callback = volver_callback

        Label(self, text="Confirmar Turnos Pendientes", font=("Arial", 16)).pack(pady=10)

        self.listar_turnos_proximos()

        Button(self, text="Volver", command=self.volver_callback).pack(pady=10)

    def listar_turnos_proximos(self):
        # Obtener los turnos del paciente desde el controlador
        historial = obtener_historial_turnos(self.paciente_id)
        turnos_proximos = historial.get("proximos", [])

        if not turnos_proximos:
            Label(self, text="No hay turnos próximos para confirmar.").pack(pady=5)
            return

        for turno in turnos_proximos:
            fecha = turno["fecha"]
            hora = turno["hora_inicio"]
            estado = turno["estado"]
            turno_id = turno["id"]

            texto = f"Turno: {fecha} a las {hora} - Estado: {estado}"
            Label(self, text=texto).pack()

            if estado == "pendiente":
                Button(
                    self,
                    text="Confirmar",
                    command=lambda t_id=turno_id: self.confirmar_turno_seleccionado(t_id)
                ).pack(pady=2)

    def confirmar_turno_seleccionado(self, turno_id):
        resultado = confirmar_turno(turno_id, self.paciente_id)

        if "exito" in resultado:
            messagebox.showinfo("Éxito", resultado["mensaje"])
            self.actualizar_interfaz()
        else:
            messagebox.showerror("Error", resultado.get("error", "Error al confirmar turno."))

    def actualizar_interfaz(self):
        # Limpiar y recargar la interfaz con los turnos actualizados
        for widget in self.winfo_children():
            widget.destroy()
        Label(self, text="Confirmar Turnos Pendientes", font=("Arial", 16)).pack(pady=10)
        self.listar_turnos_proximos()
        Button(self, text="Volver", command=self.volver_callback).pack(pady=10)
