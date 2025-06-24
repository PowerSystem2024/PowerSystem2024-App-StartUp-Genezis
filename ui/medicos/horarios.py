from tkinter import *
from tkinter import ttk, messagebox
from controllers.med_controller import (
    obtener_horarios_disponibles,
    agregar_horario_disponible,
    eliminar_horario_disponible
)

class HorariosFrame(Frame):
    def __init__(self, parent, medico_id):
        super().__init__(parent)
        self.medico_id = medico_id

        Label(self, text="Horarios Disponibles", font=("Arial", 14, "bold")).pack(pady=10)

        form = Frame(self)
        form.pack(pady=10)

        Label(form, text="Día (0=Dom, 6=Sáb):").grid(row=0, column=0)
        self.dia_entry = Entry(form, width=5)
        self.dia_entry.grid(row=0, column=1)

        Label(form, text="Hora Inicio (HH:MM):").grid(row=1, column=0)
        self.inicio_entry = Entry(form, width=10)
        self.inicio_entry.grid(row=1, column=1)

        Label(form, text="Hora Fin (HH:MM):").grid(row=2, column=0)
        self.fin_entry = Entry(form, width=10)
        self.fin_entry.grid(row=2, column=1)

        Button(form, text="Agregar", command=self.agregar).grid(row=3, column=0, columnspan=2, pady=5)

        self.tree = ttk.Treeview(self, columns=("dia", "inicio", "fin"), show="headings")
        self.tree.heading("dia", text="Día")
        self.tree.heading("inicio", text="Inicio")
        self.tree.heading("fin", text="Fin")
        self.tree.pack(padx=10, pady=10)

        Button(self, text="Eliminar Seleccionado", command=self.eliminar).pack(pady=5)

        self.cargar_horarios()

    def cargar_horarios(self):
        self.tree.delete(*self.tree.get_children())
        for h in obtener_horarios_disponibles(self.medico_id):
            self.tree.insert("", END, iid=h["id"], values=(h["dia_semana"], h["hora_inicio"], h["hora_fin"]))

    def agregar(self):
        try:
            agregar_horario_disponible(
                self.medico_id,
                int(self.dia_entry.get()),
                self.inicio_entry.get(),
                self.fin_entry.get()
            )
            self.cargar_horarios()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def eliminar(self):
        seleccionado = self.tree.focus()
        if seleccionado:
            eliminar_horario_disponible(seleccionado)
            self.cargar_horarios()