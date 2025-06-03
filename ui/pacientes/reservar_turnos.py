# views/paciente/reservar_turno.py

from tkinter import *
from tkinter import ttk, messagebox
from tkcalendar import Calendar
from controllers.pac_controller import buscar_turnos_disponibles, reservar_turno

class ReservarTurnoFrame(Frame):
    def __init__(self, parent, paciente_id):
        super().__init__(parent)
        self.parent = parent
        self.paciente_id = paciente_id
        self.turnos_disponibles = []

        Label(self, text="Reservar Turno", font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=10)

        # Calendario
        self.cal = Calendar(self, selectmode='day', date_pattern='yyyy-mm-dd')
        self.cal.grid(row=1, column=0, padx=10, pady=10)

        # Combo de especialidades
        Label(self, text="Especialidad:").grid(row=2, column=0)
        self.especialidad_cb = ttk.Combobox(self, values=["Clínica", "Pediatría", "Cardiología"], state="readonly")
        self.especialidad_cb.grid(row=3, column=0)

        # Botón buscar
        Button(self, text="Buscar Turnos", command=self.buscar_turnos).grid(row=4, column=0, pady=10)

        # Tabla de turnos disponibles
        self.tree = ttk.Treeview(self, columns=("medico", "hora", "consultorio"), show='headings', height=10)
        self.tree.heading("medico", text="Médico")
        self.tree.heading("hora", text="Hora")
        self.tree.heading("consultorio", text="Consultorio")
        self.tree.grid(row=1, column=1, rowspan=4, padx=10, pady=10)

        # Botón reservar
        Button(self, text="Reservar Turno", command=self.reservar_turno_seleccionado).grid(row=5, column=1, pady=10)

    def buscar_turnos(self):
        fecha = self.cal.get_date()
        especialidad = self.especialidad_cb.get()

        if not especialidad:
            messagebox.showwarning("Atención", "Seleccione una especialidad.")
            return

        self.turnos_disponibles = buscar_turnos_disponibles(especialidad, fecha)
        self.tree.delete(*self.tree.get_children())

        for turno in self.turnos_disponibles:
            self.tree.insert("", "end", iid=turno["id"], values=(turno["medico_nombre"], turno["hora_inicio"], turno["consultorio"]))

    def reservar_turno_seleccionado(self):
        seleccionado = self.tree.focus()
        if seleccionado:
            confirmar = messagebox.askyesno("Confirmar", "¿Desea reservar este turno?")
            if confirmar:
                reservar_turno(seleccionado, self.paciente_id)
                messagebox.showinfo("Éxito", "Turno reservado con éxito.")
                self.buscar_turnos()  # Refresca la tabla
        else:
            messagebox.showwarning("Atención", "Seleccione un turno disponible.")
