# ui/medicos/horarios.py

from tkinter import *
from tkinter import ttk, messagebox
from controllers.med_controller import obtener_horarios_disponibles, agregar_horario_disponible, eliminar_horario_disponible

class HorariosFrame(Frame):
    def __init__(self, parent, medico_id):
        super().__init__(parent)
        self.parent = parent
        self.medico_id = medico_id

        # Título
        Label(self, text="Horarios Disponibles", font=("Arial", 16, "bold")).pack(pady=10)

        # Frame del formulario
        form_frame = Frame(self)
        form_frame.pack(pady=10)

        # Día de la semana
        Label(form_frame, text="Día (0=Domingo, 6=Sábado):").grid(row=0, column=0, sticky="e")
        self.entry_dia = Entry(form_frame, width=5)
        self.entry_dia.grid(row=0, column=1, padx=5)

        # Hora inicio
        Label(form_frame, text="Hora Inicio (HH:MM):").grid(row=1, column=0, sticky="e")
        self.entry_inicio = Entry(form_frame, width=10)
        self.entry_inicio.grid(row=1, column=1, padx=5)

        # Hora fin
        Label(form_frame, text="Hora Fin (HH:MM):").grid(row=2, column=0, sticky="e")
        self.entry_fin = Entry(form_frame, width=10)
        self.entry_fin.grid(row=2, column=1, padx=5)

        # Botón agregar
        Button(form_frame, text="Agregar Horario", command=self.agregar_horario).grid(row=3, column=0, columnspan=2, pady=10)

        # Tabla de horarios
        self.tree = ttk.Treeview(self, columns=("dia", "inicio", "fin"), show="headings", height=8)
        self.tree.heading("dia", text="Día")
        self.tree.heading("inicio", text="Hora Inicio")
        self.tree.heading("fin", text="Hora Fin")
        self.tree.pack(padx=10, pady=10)

        # Botón eliminar
        Button(self, text="Eliminar Horario Seleccionado", command=self.eliminar_horario).pack(pady=5)

        self.cargar_horarios()

    def cargar_horarios(self):
        self.tree.delete(*self.tree.get_children())
        horarios = obtener_horarios_disponibles(self.medico_id)
        for h in horarios:
            self.tree.insert("", "end", iid=h["id"], values=(h["dia_semana"], h["hora_inicio"], h["hora_fin"]))

    def agregar_horario(self):
        try:
            dia = int(self.entry_dia.get())
            inicio = self.entry_inicio.get()
            fin = self.entry_fin.get()

            if not (0 <= dia <= 6):
                raise ValueError("El día debe estar entre 0 y 6")

            agregar_horario_disponible(self.medico_id, dia, inicio, fin)
            self.cargar_horarios()
            messagebox.showinfo("Éxito", "Horario agregado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo agregar el horario:\n{e}")

    def eliminar_horario(self):
        seleccionado = self.tree.focus()
        if seleccionado:
            confirmar = messagebox.askyesno("Confirmar", "¿Eliminar este horario?")
            if confirmar:
                eliminar_horario_disponible(seleccionado)
                self.cargar_horarios()
        else:
            messagebox.showwarning("Atención", "Seleccione un horario para eliminar.")
