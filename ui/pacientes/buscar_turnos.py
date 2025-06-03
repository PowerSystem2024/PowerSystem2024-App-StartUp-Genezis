# views/paciente/buscar_turnos.py

from tkinter import *
from tkinter import ttk, messagebox
from tkcalendar import Calendar
from controllers.pac_controller import buscar_turnos_disponibles

class BuscarTurnosFrame(Frame):
    def __init__(self, parent, paciente_id):
        super().__init__(parent)
        self.parent = parent
        self.paciente_id = paciente_id
        self.resultados = []

        # Dropdown de especialidades
        Label(self, text="Especialidad:").grid(row=0, column=0, padx=10, pady=5, sticky='w')
        self.especialidad_cb = ttk.Combobox(self, values=[
            "Clínico", "Pediatra", "Cardiólogo", "Dermatólogo"  # podés cargar dinámicamente desde la DB si querés
        ])
        self.especialidad_cb.grid(row=0, column=1, padx=10, pady=5)

        # Calendario
        self.cal = Calendar(self, selectmode='day', date_pattern='yyyy-mm-dd')
        self.cal.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        # Botón para buscar
        Button(self, text="Buscar Turnos", command=self.buscar_turnos).grid(row=2, column=0, columnspan=2, pady=10)

        # Tabla de resultados
        self.tree = ttk.Treeview(self, columns=("medico", "horarios"), show='headings', height=10)
        self.tree.heading("medico", text="Médico")
        self.tree.heading("horarios", text="Horarios Disponibles")
        self.tree.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    def buscar_turnos(self):
        especialidad = self.especialidad_cb.get()
        fecha = self.cal.get_date()

        if not especialidad:
            messagebox.showwarning("Atención", "Seleccione una especialidad.")
            return

        self.resultados = buscar_turnos_disponibles(especialidad, fecha)
        self.tree.delete(*self.tree.get_children())

        if not self.resultados:
            messagebox.showinfo("Sin turnos", "No hay turnos disponibles para esta especialidad en esa fecha.")
            return

        for medico in self.resultados:
            horarios_str = ", ".join(medico["horarios_disponibles"])
            self.tree.insert("", "end", values=(medico["nombre"], horarios_str))
