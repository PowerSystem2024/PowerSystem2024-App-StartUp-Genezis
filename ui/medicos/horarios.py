# horarios.py

import tkinter as tk
from tkinter import ttk, messagebox, Frame
# IMPORTACIÓN AÑADIDA para la validación de fechas
from datetime import date
from controllers.med_controller import obtener_horarios_disponibles, agregar_horario_disponible, \
    eliminar_horario_disponible
from tkcalendar import DateEntry


class HorariosFrame(Frame):
    def __init__(self, parent, medico_id):
        super().__init__(parent)
        self.medico_id = medico_id

        main_frame = ttk.Frame(self)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # --- Frame para agregar horarios (se empaquetará más adelante) ---
        add_frame = ttk.LabelFrame(main_frame, text="Agregar horario disponible")

        ttk.Label(add_frame, text="Fecha:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.fecha_entry = DateEntry(add_frame, width=12, background='darkblue',
                                     foreground='white', borderwidth=2, date_pattern='y-mm-dd')
        self.fecha_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(add_frame, text="Hora inicio:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        hora_inicio_frame = ttk.Frame(add_frame)
        hora_inicio_frame.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        self.hora_inicio_hh = ttk.Combobox(hora_inicio_frame, width=3, values=[f"{i:02d}" for i in range(24)])
        self.hora_inicio_hh.current(8)
        self.hora_inicio_hh.pack(side="left")
        ttk.Label(hora_inicio_frame, text=":").pack(side="left")
        self.hora_inicio_mm = ttk.Combobox(hora_inicio_frame, width=3, values=["00", "15", "30", "45"])
        self.hora_inicio_mm.current(0)
        self.hora_inicio_mm.pack(side="left")

        ttk.Label(add_frame, text="Hora fin:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        hora_fin_frame = ttk.Frame(add_frame)
        hora_fin_frame.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        self.hora_fin_hh = ttk.Combobox(hora_fin_frame, width=3, values=[f"{i:02d}" for i in range(24)])
        self.hora_fin_hh.current(9)
        self.hora_fin_hh.pack(side="left")
        ttk.Label(hora_fin_frame, text=":").pack(side="left")
        self.hora_fin_mm = ttk.Combobox(hora_fin_frame, width=3, values=["00", "15", "30", "45"])
        self.hora_fin_mm.current(0)
        self.hora_fin_mm.pack(side="left")

        ttk.Button(add_frame, text="Agregar", command=self.agregar_horario).grid(row=3, column=0, columnspan=2, pady=10)

        # --- Frame para la tabla (se empaquetará más adelante) ---
        table_frame = ttk.Frame(main_frame)
        scroll = ttk.Scrollbar(table_frame)
        scroll.pack(side="right", fill="y")
        self.tree = ttk.Treeview(table_frame, columns=("fecha", "hora_inicio", "hora_fin"),
                                 show="headings", yscrollcommand=scroll.set)
        self.tree.heading("fecha", text="Fecha")
        self.tree.heading("hora_inicio", text="Hora inicio")
        self.tree.heading("hora_fin", text="Hora fin")
        self.tree.column("fecha", width=150, anchor="center")
        self.tree.column("hora_inicio", width=100, anchor="center")
        self.tree.column("hora_fin", width=100, anchor="center")
        self.tree.pack(fill="both", expand=True)
        scroll.config(command=self.tree.yview)

        # --- Botón de eliminar (se crea aquí pero se empaqueta en el orden correcto) ---
        eliminar_btn = ttk.Button(main_frame, text="Eliminar horario seleccionado",
                                  command=self.eliminar_horario)

        # --- CORRECCIÓN DE LAYOUT ---
        # Se define el orden de empaquetado para asegurar la visibilidad de todos los elementos.

        # 1. El botón de eliminar se ancla a la PARTE INFERIOR.
        eliminar_btn.pack(side="bottom", pady=10)

        # 2. El formulario de agregar se ancla a la PARTE SUPERIOR.
        add_frame.pack(side="top", fill="x", pady=5)

        # 3. La tabla llena todo el espacio restante en el medio.
        table_frame.pack(side="top", fill="both", expand=True, pady=(5, 0))

        # Finalmente, se cargan los horarios iniciales.
        self.cargar_horarios()

    def cargar_horarios(self):
        self.tree.delete(*self.tree.get_children())
        horarios = obtener_horarios_disponibles(self.medico_id)
        if horarios:
            for h in horarios:
                fecha_horario = h.get("fecha_horario", "Fecha no disponible")
                self.tree.insert("", "end", iid=h["id"], values=(fecha_horario, h["hora_inicio"], h["hora_fin"]))

    def agregar_horario(self):
        try:
            # VALIDACIÓN DE FECHA AÑADIDA
            fecha_seleccionada = self.fecha_entry.get_date()
            if fecha_seleccionada < date.today():
                messagebox.showerror("Error de Validación",
                                     "No se puede agregar un horario para una fecha anterior al día de hoy.")
                return

            fecha = fecha_seleccionada.strftime("%Y-%m-%d")
            hi = f"{self.hora_inicio_hh.get()}:{self.hora_inicio_mm.get()}"
            hf = f"{self.hora_fin_hh.get()}:{self.hora_fin_mm.get()}"

            if int(self.hora_inicio_hh.get()) > int(self.hora_fin_hh.get()) or \
                    (int(self.hora_inicio_hh.get()) == int(self.hora_fin_hh.get()) and
                     int(self.hora_inicio_mm.get()) >= int(self.hora_fin_mm.get())):
                messagebox.showerror("Error", "La hora de fin debe ser posterior a la hora de inicio")
                return

            resultado = agregar_horario_disponible(self.medico_id, fecha, hi, hf)

            if resultado:
                messagebox.showinfo("Éxito", "Horario agregado correctamente")
                self.cargar_horarios()
            else:
                # MENSAJE DE ERROR MEJORADO
                messagebox.showerror("Error", "No se pudo agregar el horario. ¡Es posible que ya exista!")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")

    def eliminar_horario(self):
        seleccionado = self.tree.selection()
        if not seleccionado:
            messagebox.showwarning("Advertencia", "Debe seleccionar un horario para eliminar")
            return

        if messagebox.askyesno("Confirmar", "¿Está seguro de que desea eliminar este horario?"):
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