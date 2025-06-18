from tkinter import *
from tkinter import ttk, messagebox
from tkcalendar import Calendar
from controllers.pac_controller import buscar_turnos_disponibles, obtener_instituciones, obtener_especialidades, reservar_turno
from datetime import datetime

class BuscarTurnosFrame(Frame):
    def __init__(self, parent, paciente_id):
        super().__init__(parent)
        self.parent = parent
        self.paciente_id = paciente_id
        self.resultados = []
        self.especialidad_seleccionada = None
        self.institucion_seleccionada = None

        self.canvas = Canvas(self)
        self.scrollbar = Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.mostrar_selector_instituciones()

    def mostrar_selector_especialidad(self):
        especialidades = obtener_especialidades()

        if not especialidades:
            messagebox.showerror("Error", "No se pudieron cargar las especialidades.")
            return

        selector = Toplevel(self)
        selector.title("Seleccionar Especialidad")
        selector.geometry("300x150")
        selector.transient(self)
        selector.grab_set()
        self.center_window(selector, 300, 150)

        Label(selector, text="Seleccione una especialidad:").pack(pady=10)

        especialidad_cb = ttk.Combobox(selector, values=especialidades, state="readonly")
        especialidad_cb.pack(pady=5)

        def confirmar():
            seleccion = especialidad_cb.get()
            if seleccion:
                self.especialidad_seleccionada = seleccion
                selector.destroy()
                self.construir_interfaz()
            else:
                messagebox.showwarning("Atención", "Debe seleccionar una especialidad.")

        Button(selector, text="Confirmar", command=confirmar).pack(pady=10)

    def mostrar_selector_instituciones(self):
        instituciones = obtener_instituciones()

        if not instituciones:
            messagebox.showerror("Error", "No se pudieron cargar las instituciones.")
            return

        self.mapa_instituciones = {inst["nombre"]: inst["id"] for inst in instituciones}
        nombres_instituciones = list(self.mapa_instituciones.keys())

        selector = Toplevel(self)
        selector.title("Seleccionar Institución")
        selector.geometry("300x150")
        selector.transient(self)
        selector.grab_set()
        self.center_window(selector, 300, 150)

        Label(selector, text="Seleccione una institución:").pack(pady=10)

        institucion_combobox = ttk.Combobox(selector, values=nombres_instituciones, state="readonly")
        institucion_combobox.pack(pady=5)

        def confirmar():
            seleccion_nombre = institucion_combobox.get()
            if seleccion_nombre:
                self.institucion_seleccionada = seleccion_nombre
                self.institucion_id = self.mapa_instituciones[seleccion_nombre]
                selector.destroy()
                self.mostrar_selector_especialidad()
            else:
                messagebox.showwarning("Atención", "Debe seleccionar una institución.")

        Button(selector, text="Confirmar", command=confirmar).pack(pady=10)

    def center_window(self, window, width, height):
        x = self.winfo_screenwidth() // 2 - width // 2
        y = self.winfo_screenheight() // 2 - height // 2
        window.geometry(f"{width}x{height}+{x}+{y}")

    def construir_interfaz(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        Label(self.scrollable_frame, text=f"Especialidad: {self.especialidad_seleccionada}", font=("Arial", 12)).grid(
            row=0, column=0, padx=10, pady=5, sticky="w")

        self.cal = Calendar(self.scrollable_frame, selectmode='day', date_pattern='yyyy-mm-dd')
        self.cal.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
        self.cal.bind("<<CalendarSelected>>", self.habilitar_boton_buscar)

        self.boton_buscar = Button(self.scrollable_frame, text="Buscar Turnos", command=self.buscar_turnos,
                                   state="disabled")
        self.boton_buscar.grid(row=2, column=0, columnspan=2, pady=10)

        self.tree = ttk.Treeview(
            self.scrollable_frame,
            columns=("medico", "fecha", "hora_inicio", "hora_fin"),
            show='headings',
            height=10
        )

        self.tree.heading("medico", text="Médico", anchor="center")
        self.tree.heading("fecha", text="Fecha", anchor="center")
        self.tree.heading("hora_inicio", text="Hora Inicio", anchor="center")
        self.tree.heading("hora_fin", text="Hora Fin", anchor="center")

        self.tree.column("medico", anchor="center", width=200)
        self.tree.column("fecha", anchor="center", width=100)
        self.tree.column("hora_inicio", anchor="center", width=100)
        self.tree.column("hora_fin", anchor="center", width=100)

        self.tree.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        Button(self.scrollable_frame, text="Cambiar Especialidad", command=self.mostrar_selector_especialidad).grid(
            row=4, column=0, columnspan=2, pady=10)

        self.boton_reservar = Button(self.scrollable_frame, text="Reservar Turno", command=self.confirmar_reserva)
        self.boton_reservar.grid(row=5, column=0, columnspan=2, pady=10)
        self.boton_reservar.grid_remove()

        self.tree.bind("<<TreeviewSelect>>", self.mostrar_boton_reservar)

    def habilitar_boton_buscar(self, event):
        self.boton_buscar.config(state="normal")

    def mostrar_boton_reservar(self, event):
        seleccion = self.tree.selection()
        if seleccion:
            self.boton_reservar.grid()
        else:
            self.boton_reservar.grid_remove()

    def confirmar_reserva(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Debe seleccionar un turno.")
            return

        item_id = seleccion[0]
        turno = self.tree.item(item_id)["values"]

        confirmar = messagebox.askyesno(
            "Confirmar Reserva",
            f"¿Está seguro que desea reservar el turno con el Dr/a {turno[0]} a las {turno[2]}?"
        )

        if confirmar:
            turno_id = item_id
            resultado = reservar_turno(turno_id, self.paciente_id, self.cal.get_date())


            if resultado["exito"]:
                messagebox.showinfo("Éxito", resultado["mensaje"])
                self.tree.delete(item_id)
                self.boton_reservar.grid_remove()
            else:
                messagebox.showerror("Error", resultado["mensaje"])

    def buscar_turnos(self):
        fecha = self.cal.get_date()
        especialidad = self.especialidad_seleccionada

        if not fecha or not especialidad:
            messagebox.showwarning("Atención", "Seleccione una especialidad y una fecha.")
            return

        fecha_seleccionada = datetime.strptime(fecha, "%Y-%m-%d").date()
        hoy = datetime.today().date()

        if fecha_seleccionada < hoy:
            messagebox.showwarning("Fecha inválida", "No puede buscar turnos en fechas anteriores a hoy.")
            return

        self.resultados = buscar_turnos_disponibles(especialidad, fecha, self.institucion_id)
        print(f"[DEBUG] Turnos disponibles encontrados: {self.resultados}")

        self.tree.delete(*self.tree.get_children())

        if not self.resultados:
            messagebox.showinfo("Sin turnos", "No hay turnos disponibles para esta especialidad en esa fecha.")
            return

        for turno in self.resultados:
            self.tree.insert(
                "",
                "end",
                iid=turno["id"],
                values=(
                    turno["nombre_medico"],
                    turno["fecha"],
                    turno["hora_inicio"],
                    turno["hora_fin"]
                )
            )
