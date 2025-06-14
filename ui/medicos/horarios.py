# ui/medicos/horarios.py

from tkinter import *
from tkinter import ttk, messagebox
from controllers.med_controller import (
    obtener_horarios_disponibles,
    agregar_horario_disponible,
    eliminar_horario_disponible
)

DIAS_SEMANA = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]

class HorariosFrame(Frame):
    def __init__(self, parent, medico_id):
        super().__init__(parent)
        self.medico_id = medico_id

        Label(self, text="Horarios Disponibles", font=("Arial", 16, "bold")).pack(pady=10)

        form_frame = Frame(self)
        form_frame.pack(pady=10)

        # Día + Hora Inicio + Hora Fin (todo alineado horizontalmente)
        Label(form_frame, text="Día:").grid(row=0, column=0, sticky="e")
        self.dia_var = StringVar()
        self.combo_dia = ttk.Combobox(form_frame, textvariable=self.dia_var, values=DIAS_SEMANA, state="readonly", width=10)
        self.combo_dia.grid(row=0, column=1, padx=5)
        self.combo_dia.current(0)

        Label(form_frame, text="Hora Inicio:").grid(row=0, column=2, sticky="e")
        self.hora_inicio_hh = StringVar()
        self.hora_inicio_mm = StringVar()
        ttk.Combobox(form_frame, textvariable=self.hora_inicio_hh, values=[f"{i:02d}" for i in range(24)],
                     width=3, state="readonly").grid(row=0, column=3)
        Label(form_frame, text=":").grid(row=0, column=4)
        ttk.Combobox(form_frame, textvariable=self.hora_inicio_mm, values=["00", "15", "30", "45"],
                     width=3, state="readonly").grid(row=0, column=5, padx=(0, 10))

        Label(form_frame, text="Hora Fin:").grid(row=0, column=6, sticky="e")
        self.hora_fin_hh = StringVar()
        self.hora_fin_mm = StringVar()
        ttk.Combobox(form_frame, textvariable=self.hora_fin_hh, values=[f"{i:02d}" for i in range(24)],
                     width=3, state="readonly").grid(row=0, column=7)
        Label(form_frame, text=":").grid(row=0, column=8)
        ttk.Combobox(form_frame, textvariable=self.hora_fin_mm, values=["00", "15", "30", "45"],
                     width=3, state="readonly").grid(row=0, column=9)

        # Botón agregar
        Button(form_frame, text="Agregar Horario", command=self.agregar_horario).grid(row=1, column=0, columnspan=10, pady=10)

        # Tabla
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
            nombre_dia = DIAS_SEMANA[h["dia_semana"]] if 0 <= h["dia_semana"] <= 6 else f"Desconocido ({h['dia_semana']})"
            self.tree.insert("", "end", iid=h["id"], values=(nombre_dia, h["hora_inicio"], h["hora_fin"]))

    def agregar_horario(self):
        try:
            dia_nombre = self.dia_var.get()
            dia_num = DIAS_SEMANA.index(dia_nombre)

            hi = f"{self.hora_inicio_hh.get()}:{self.hora_inicio_mm.get()}"
            hf = f"{self.hora_fin_hh.get()}:{self.hora_fin_mm.get()}"

            if not all([self.hora_inicio_hh.get(), self.hora_inicio_mm.get(),
                        self.hora_fin_hh.get(), self.hora_fin_mm.get()]):
                raise ValueError("Debe seleccionar horas y minutos para ambos campos.")

            hi_total = int(self.hora_inicio_hh.get()) * 60 + int(self.hora_inicio_mm.get())
            hf_total = int(self.hora_fin_hh.get()) * 60 + int(self.hora_fin_mm.get())
            if hi_total >= hf_total:
                raise ValueError("La hora de inicio debe ser menor a la de fin.")

            agregar_horario_disponible(self.medico_id, dia_num, hi, hf)
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
