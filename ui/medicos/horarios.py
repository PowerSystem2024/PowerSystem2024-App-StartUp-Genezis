from tkinter import ttk, messagebox, Frame
from controllers.med_controller import obtener_horarios_disponibles, agregar_horario_disponible, \
    eliminar_horario_disponible
from tkcalendar import DateEntry  # Asumiendo que se usa este componente para fechas


# Se elimina la constante DIAS_SEMANA

class HorariosFrame(Frame):
    def __init__(self, parent, medico_id):
        super().__init__(parent)
        self.medico_id = medico_id

        # Frame principal
        main_frame = ttk.Frame(self)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Frame para agregar horarios
        add_frame = ttk.LabelFrame(main_frame, text="Agregar horario disponible")
        add_frame.pack(fill="x", pady=10)

        # En vez de selector de día, usamos un DateEntry para fechas
        ttk.Label(add_frame, text="Fecha:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.fecha_entry = DateEntry(add_frame, width=12, background='darkblue',
                                     foreground='white', borderwidth=2)
        self.fecha_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        # Selector de hora inicio
        ttk.Label(add_frame, text="Hora inicio:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        hora_inicio_frame = ttk.Frame(add_frame)
        hora_inicio_frame.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        self.hora_inicio_hh = ttk.Combobox(hora_inicio_frame, width=2)
        self.hora_inicio_hh['values'] = [f"{i:02d}" for i in range(24)]
        self.hora_inicio_hh.current(8)
        self.hora_inicio_hh.pack(side="left")

        ttk.Label(hora_inicio_frame, text=":").pack(side="left")

        self.hora_inicio_mm = ttk.Combobox(hora_inicio_frame, width=2)
        self.hora_inicio_mm['values'] = ["00", "15", "30", "45"]
        self.hora_inicio_mm.current(0)
        self.hora_inicio_mm.pack(side="left")

        # Selector de hora fin
        ttk.Label(add_frame, text="Hora fin:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        hora_fin_frame = ttk.Frame(add_frame)
        hora_fin_frame.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        self.hora_fin_hh = ttk.Combobox(hora_fin_frame, width=2)
        self.hora_fin_hh['values'] = [f"{i:02d}" for i in range(24)]
        self.hora_fin_hh.current(9)
        self.hora_fin_hh.pack(side="left")

        ttk.Label(hora_fin_frame, text=":").pack(side="left")

        self.hora_fin_mm = ttk.Combobox(hora_fin_frame, width=2)
        self.hora_fin_mm['values'] = ["00", "15", "30", "45"]
        self.hora_fin_mm.current(0)
        self.hora_fin_mm.pack(side="left")

        # Botón para agregar
        ttk.Button(add_frame, text="Agregar", command=self.agregar_horario).grid(row=3, column=0, columnspan=2, pady=10)

        # Tabla de horarios
        table_frame = ttk.Frame(main_frame)
        table_frame.pack(fill="both", expand=True, pady=10)

        # Scrollbar
        scroll = ttk.Scrollbar(table_frame)
        scroll.pack(side="right", fill="y")

        # Treeview para mostrar horarios
        self.tree = ttk.Treeview(table_frame, columns=("fecha", "hora_inicio", "hora_fin"),
                                 show="headings", yscrollcommand=scroll.set)

        self.tree.heading("fecha", text="Fecha")
        self.tree.heading("hora_inicio", text="Hora inicio")
        self.tree.heading("hora_fin", text="Hora fin")

        self.tree.column("fecha", width=150)
        self.tree.column("hora_inicio", width=100)
        self.tree.column("hora_fin", width=100)

        self.tree.pack(fill="both", expand=True)
        scroll.config(command=self.tree.yview)

        # Botón para eliminar
        ttk.Button(main_frame, text="Eliminar horario seleccionado",
                   command=self.eliminar_horario).pack(pady=10)

        # Cargar horarios existentes
        self.cargar_horarios()

    def cargar_horarios(self):
        self.tree.delete(*self.tree.get_children())
        horarios = obtener_horarios_disponibles(self.medico_id)
        for h in horarios:
            # Ya no usamos DIAS_SEMANA, usamos directamente la fecha
            fecha_horario = h.get("fecha_horario", "Fecha no disponible")
            self.tree.insert("", "end", iid=h["id"], values=(fecha_horario, h["hora_inicio"], h["hora_fin"]))

    def agregar_horario(self):
        try:
            # Ya no usamos día de la semana, usamos la fecha directamente
            fecha = self.fecha_entry.get_date().strftime("%Y-%m-%d")

            hi = f"{self.hora_inicio_hh.get()}:{self.hora_inicio_mm.get()}"
            hf = f"{self.hora_fin_hh.get()}:{self.hora_fin_mm.get()}"

            # Validaciones
            if int(self.hora_inicio_hh.get()) > int(self.hora_fin_hh.get()) or \
                    (int(self.hora_inicio_hh.get()) == int(self.hora_fin_hh.get()) and
                     int(self.hora_inicio_mm.get()) >= int(self.hora_fin_mm.get())):
                messagebox.showerror("Error", "La hora de fin debe ser posterior a la hora de inicio")
                return

            # Agregar el horario usando la fecha en lugar del día de la semana
            resultado = agregar_horario_disponible(self.medico_id, fecha, hi, hf)

            if resultado:
                messagebox.showinfo("Éxito", "Horario agregado correctamente")
                self.cargar_horarios()
            else:
                messagebox.showerror("Error", "No se pudo agregar el horario")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")

    def eliminar_horario(self):
        seleccionado = self.tree.selection()
        if not seleccionado:
            messagebox.showwarning("Advertencia", "Debe seleccionar un horario para eliminar")
            return

        if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este horario?"):
            try:
                horario_id = seleccionado[0]
                resultado = eliminar_horario_disponible(horario_id)

                if resultado:
                    messagebox.showinfo("Éxito", "Horario eliminado correctamente")
                    self.cargar_horarios()
                else:
                    messagebox.showerror("Error", "No se pudo eliminar el horario")
            except Exception as e:
                messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")
