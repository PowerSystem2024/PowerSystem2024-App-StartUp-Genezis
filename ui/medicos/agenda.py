from tkinter import *
from tkinter import ttk, messagebox, simpledialog
from tkcalendar import Calendar
from controllers.med_controller import obtener_turnos_del_dia, completar_turno, cancelar_turno

class AgendaMedicoFrame(Frame):
    def __init__(self, parent, medico_id):
        super().__init__(parent)
        self.medico_id = medico_id

        self.cal = Calendar(self, selectmode='day', date_pattern='yyyy-mm-dd')
        self.cal.pack(pady=10)

        Button(self, text="Ver Turnos", command=self.cargar).pack(pady=5)

        self.tree = ttk.Treeview(self, columns=("paciente", "hora", "estado"), show="headings")
        self.tree.heading("paciente", text="Paciente")
        self.tree.heading("hora", text="Hora")
        self.tree.heading("estado", text="Estado")
        self.tree.pack(padx=10, pady=10)

        Button(self, text="Completar", command=self.completar).pack(side=LEFT, padx=10)
        Button(self, text="Cancelar", command=self.cancelar).pack(side=RIGHT, padx=10)

    def cargar(self):
        fecha = self.cal.get_date()
        self.tree.delete(*self.tree.get_children())
        for t in obtener_turnos_del_dia(self.medico_id, fecha):
            self.tree.insert("", END, iid=t["id"], values=(t["paciente_id"], t["hora_inicio"], t["estado"]))

    def completar(self):
        sel = self.tree.focus()
        if sel:
            notas = simpledialog.askstring("Notas", "Ingrese notas de consulta:")
            completar_turno(sel, notas)
            self.cargar()

    def cancelar(self):
        sel = self.tree.focus()
        if sel:
            cancelar_turno(sel)
            self.cargar()