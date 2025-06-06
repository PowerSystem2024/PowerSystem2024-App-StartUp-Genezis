from tkinter import *
from tkinter import messagebox
from controllers.pac_controller import obtener_historial_turnos, cancelar_turno

class CancelarTurnosFrame(Frame):
    def __init__(self, parent, paciente_id):
        super().__init__(parent)
        self.parent = parent
        self.paciente_id = paciente_id
        self.turnos_proximos = []

        Label(self, text="Cancelar Turno", font=("Arial", 16, "bold")).pack(pady=10)

        self.listbox = Listbox(self, width=80, height=10)
        self.listbox.pack(pady=10)

        Button(self, text="Cancelar Turno Seleccionado", command=self.cancelar_turno_seleccionado).pack(pady=5)

        self.cargar_turnos()

    def cargar_turnos(self):
        historial = obtener_historial_turnos(self.paciente_id)
        self.turnos_proximos = historial["proximos"]

        self.listbox.delete(0, END)
        for turno in self.turnos_proximos:
            fecha = turno.get("fecha", "")[:10]
            hora = turno.get("hora_inicio", "")
            medico = turno.get("medico_id", "")  # Si querés mostrar nombre, deberías hacer join
            estado = turno.get("estado", "")
            texto = f"{fecha} - {hora} - Médico: {medico} - Estado: {estado}"
            self.listbox.insert(END, texto)

    def cancelar_turno_seleccionado(self):
        seleccion = self.listbox.curselection()
        if not seleccion:
            messagebox.showwarning("Atención", "Por favor, seleccioná un turno para cancelar.")
            return

        index = seleccion[0]
        turno = self.turnos_proximos[index]
        turno_id = turno["id"]

        confirmar = messagebox.askyesno("Confirmar", "¿Estás seguro que querés cancelar este turno?")
        if confirmar:
            cancelar_turno(turno_id)
            messagebox.showinfo("Éxito", "El turno fue cancelado correctamente.")
            self.cargar_turnos()
