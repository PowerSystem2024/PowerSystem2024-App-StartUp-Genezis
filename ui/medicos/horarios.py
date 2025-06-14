# ui/medicos/horarios.py

from tkinter import *
from tkinter import ttk, messagebox
from controllers.med_controller import (
    obtener_horarios_disponibles,
    agregar_horario_disponible,
    eliminar_horario_disponible
)

DIAS_SEMANA = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado","Domingo"]

class HorariosFrame(Frame):
    def __init__(self, parent, medico_id):
        super().__init__(parent)
        self.parent = parent
        self.medico_id = medico_id

        Label(self, text="Horarios Disponibles", font=("Arial", 16, "bold")).pack(pady=10)

        form_frame = Frame(self)
        form_frame.pack(pady=10)

        # Día de la semana con Combobox
        Label(form_frame, text="Día de la semana:").grid(row=0, column=0, sticky="e")
        self.dia_var = StringVar()
        self.combo_dia = ttk.Combobox(form_frame, textvariable=self.dia_var, values=DIAS_SEMANA, state="readonly")
        self.combo_dia.grid(row=0, column=1, padx=5)
        self.combo_dia.current(0)

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

        # Tabla
        self.tree = ttk.Treeview(self, columns=("dia", "inicio", "fin"), show="headings", height=8)
        self.tree.heading("dia", text="Día")
        self.tree.heading("inicio", text="Hora Inicio")
        self.tree.heading("fin", text="Hora Fin")
        self.tree.pack(padx=10, pady=10)

        Button(self, text="Eliminar Horario Seleccionado", command=self.eliminar_horario).pack(pady=5)

        self.cargar_horarios()

    def cargar_horarios(self):
        self.tree.delete(*self.tree.get_children())
        horarios = obtener_horarios_disponibles(self.medico_id)
        for h in horarios:
            nombre_dia = DIAS_SEMANA[h["dia_semana"]] if 0 <= h["dia_semana"] <= 6 else f"Desconocido ({h['dia_semana']})"
            self.tree.insert("", "end", iid=h["id"], values=(nombre_dia, h["hora_inicio"], h["hora_fin"]))

    def agregar_horario(self):
        dia_nombre = self.dia_var.get()
        hora_inicio = self.entry_inicio.get()
        hora_fin = self.entry_fin.get()

        if not dia_nombre or not hora_inicio or not hora_fin:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        try:
            # Validar hora (HH:MM)
            hi_h, hi_m = map(int, hora_inicio.split(":"))
            hf_h, hf_m = map(int, hora_fin.split(":"))
            if (hi_h, hi_m) >= (hf_h, hf_m):
                raise ValueError("La hora de inicio debe ser anterior a la hora de fin.")
        except Exception as e:
            messagebox.showerror("Error", f"Formato de hora inválido o inconsistente:\n{e}")
            return

        try:
            dia_numero = DIAS_SEMANA.index(dia_nombre)
            agregar_horario_disponible(self.medico_id, dia_numero, hora_inicio, hora_fin)
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
