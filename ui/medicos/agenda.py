# views/medico/agenda.py

from tkinter import *
from tkinter import ttk, messagebox
from tkcalendar import Calendar
#from dateutil import datetime corregir
from controllers.med_controller import obtener_turnos_del_dia, completar_turno, cancelar_turno

class AgendaMedicoFrame(Frame):
    def __init__(self, parent, medico_id):
        super().__init__(parent)
        self.parent = parent
        self.medico_id = medico_id
        self.turnos = []

        # Calendario
        self.cal = Calendar(self, selectmode='day', date_pattern='yyyy-mm-dd')
        self.cal.grid(row=0, column=0, padx=10, pady=10)

        # Botón para cargar turnos del día
        Button(self, text="Ver turnos del día", command=self.cargar_turnos).grid(row=1, column=0, pady=10)

        # Tabla de turnos
        self.tree = ttk.Treeview(self, columns=("paciente", "hora", "estado"), show='headings', height=10)
        self.tree.heading("paciente", text="Paciente ID")
        self.tree.heading("hora", text="Hora")
        self.tree.heading("estado", text="Estado")
        self.tree.grid(row=0, column=1, rowspan=3, padx=10, pady=10)

        # Botones de acción
        Button(self, text="Completar Turno", command=self.marcar_completado).grid(row=2, column=1, sticky='w', padx=5)
        Button(self, text="Cancelar Turno", command=self.cancelar_turno).grid(row=2, column=1, sticky='e', padx=5)

    def cargar_turnos(self):
        fecha = self.cal.get_date()
        self.turnos = obtener_turnos_del_dia(self.medico_id, fecha)
        self.tree.delete(*self.tree.get_children())
        for turno in self.turnos:
            self.tree.insert("", "end", iid=turno["id"], values=(turno["paciente_id"], turno["hora_inicio"], turno["estado"]))

    def marcar_completado(self):
        seleccionado = self.tree.focus()
        if seleccionado:
            notas = simpledialog.askstring("Notas de consulta", "Ingrese notas:")
            completar_turno(seleccionado, notas)
            self.cargar_turnos()
        else:
            messagebox.showwarning("Atención", "Seleccione un turno")

    def cancelar_turno(self):
        seleccionado = self.tree.focus()
        if seleccionado:
            confirmar = messagebox.askyesno("Confirmar", "¿Cancelar este turno?")
            if confirmar:
                cancelar_turno(seleccionado)
                self.cargar_turnos()
        else:
            messagebox.showwarning("Atención", "Seleccione un turno")
