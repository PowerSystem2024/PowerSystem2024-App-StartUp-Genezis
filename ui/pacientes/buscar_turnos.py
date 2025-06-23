from tkinter import *
from tkinter import ttk, messagebox
from tkcalendar import Calendar
from controllers.pac_controller import buscar_turnos_disponibles, obtener_instituciones, obtener_especialidades, reservar_turno
from datetime import datetime

class BuscarTurnosFrame(Frame):
    def __init__(self, parent, paciente_id, volver_callback):
        super().__init__(parent)
        self.parent = parent
        self.paciente_id = paciente_id
        self.volver_callback = volver_callback

        self.resultados = []
        self.especialidad_seleccionada = None
        self.institucion_seleccionada = None

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
        for widget in self.winfo_children():
            widget.destroy()

        Label(self, text=f"Especialidad: {self.especialidad_seleccionada}", font=("Arial", 12)).pack(pady=5)

        self.cal = Calendar(self, selectmode='day', date_pattern='yyyy-mm-dd')
        self.cal.pack(pady=10)
        self.cal.bind("<<CalendarSelected>>", self.habilitar_boton_buscar)

        # Botones en fila
        botones_frame = Frame(self)
        botones_frame.pack(pady=10)

        self.boton_buscar = Button(botones_frame, text="Buscar Turnos", command=self.buscar_turnos, state="disabled")
        self.boton_buscar.pack(side=LEFT, padx=5)

        Button(botones_frame, text="Cambiar Especialidad", command=self.mostrar_selector_especialidad).pack(side=LEFT, padx=5)
        Button(botones_frame, text="Atrás", command=self.volver_atras).pack(side=LEFT, padx=5)

        # Treeview de resultados oculto inicialmente
        self.tree = ttk.Treeview(self, columns=("medico", "fecha", "hora_inicio", "hora_fin"), show='headings', height=10)
        self.tree.heading("medico", text="Médico", anchor="center")
        self.tree.heading("fecha", text="Fecha", anchor="center")
        self.tree.heading("hora_inicio", text="Hora Inicio", anchor="center")
        self.tree.heading("hora_fin", text="Hora Fin", anchor="center")
        for col in ("medico", "fecha", "hora_inicio", "hora_fin"):
            self.tree.column(col, anchor="center", width=120)
        self.tree.pack(padx=10, pady=10)
        self.tree.pack_forget()
        self.tree.bind("<<TreeviewSelect>>", self.mostrar_boton_reservar)

        self.boton_reservar = Button(self, text="Reservar Turno", command=self.confirmar_reserva)
        self.boton_reservar.pack(pady=10)
        self.boton_reservar.pack_forget()

    def habilitar_boton_buscar(self, event):
        self.boton_buscar.config(state="normal")

    def mostrar_boton_reservar(self, event):
        seleccion = self.tree.selection()
        if seleccion:
            self.boton_reservar.pack(pady=10)
        else:
            self.boton_reservar.pack_forget()

    def confirmar_reserva(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Debe seleccionar un turno.")
            return

        item_id = seleccion[0]
        turno = self.tree.item(item_id)["values"]
        confirmar = messagebox.askyesno("Confirmar Reserva", f"¿Está seguro que desea reservar el turno con el Dr/a {turno[0]} a las {turno[2]}?")
        if confirmar:
            turno_id = item_id
            resultado = reservar_turno(turno_id, self.paciente_id, self.cal.get_date())
            if resultado["exito"]:
                messagebox.showinfo("Éxito", resultado["mensaje"])
                self.tree.delete(item_id)
                self.boton_reservar.pack_forget()
            else:
                messagebox.showerror("Error", resultado["mensaje"])

    def buscar_turnos(self):
        fecha = self.cal.get_date()
        especialidad = self.especialidad_seleccionada
        if not fecha or not especialidad:
            messagebox.showwarning("Atención", "Seleccione una especialidad y una fecha.")
            return

        fecha_seleccionada = datetime.strptime(fecha, "%Y-%m-%d").date()
        if fecha_seleccionada < datetime.today().date():
            messagebox.showwarning("Fecha inválida", "No puede buscar turnos en fechas anteriores a hoy.")
            return

        self.resultados = buscar_turnos_disponibles(especialidad, fecha, self.institucion_id)
        self.tree.delete(*self.tree.get_children())

        if not self.resultados:
            messagebox.showinfo("Sin turnos", "No hay turnos disponibles para esta especialidad en esa fecha.")
            return

        for turno in self.resultados:
            self.tree.insert("", "end", iid=turno["id"], values=(turno["nombre_medico"], turno["fecha"], turno["hora_inicio"], turno["hora_fin"]))
        self.tree.pack()

    def volver_atras(self):
        self.destroy()  # elimina el frame actual
        if self.volver_callback:
            self.volver_callback()

