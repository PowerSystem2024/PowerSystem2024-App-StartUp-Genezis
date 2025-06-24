from tkinter import *
from tkinter import ttk, messagebox, simpledialog
from tkcalendar import Calendar
from controllers.med_controller import obtener_turnos_del_dia, completar_turno, cancelar_turno, \
    obtener_pacientes_por_medico, supabase, obtener_todos_los_turnos


class AgendaMedicoFrame(Frame):
    def __init__(self, parent, medico_id):
        super().__init__(parent)
        self.medico_id = medico_id
        self.pacientes = {}
        self.cargar_pacientes()

        # Configuración del calendario
        self.cal = Calendar(self, selectmode='day', date_pattern='yyyy-mm-dd')
        self.cal.pack(pady=10)

        # Vincular el evento de selección de fecha para actualizar automáticamente
        self.cal.bind("<<CalendarSelected>>", self.cargar_turnos)

        # Marcar días con turnos
        self.marcar_dias_con_turnos()

        # Botón para ver todos los turnos
        self.btn_frame = Frame(self)
        self.btn_frame.pack(pady=5)
        self.btn_todos_turnos = Button(self.btn_frame, text="Ver todos los turnos",
                                       command=self.ver_todos_turnos,
                                       bg="#3498db", fg="white")
        self.btn_todos_turnos.pack(pady=5)

        # Tabla de turnos mejorada
        frame_turnos = Frame(self)
        frame_turnos.pack(fill=BOTH, expand=True, padx=10, pady=10)

        self.tree = ttk.Treeview(frame_turnos,
                                 columns=("paciente", "hora", "estado", "obra_social", "num_afiliado", "fecha"),
                                 show="headings",
                                 height=10)
        self.tree.heading("paciente", text="Paciente")
        self.tree.heading("hora", text="Hora")
        self.tree.heading("estado", text="Estado")
        self.tree.heading("obra_social", text="Obra Social")
        self.tree.heading("num_afiliado", text="Nº Afiliado")
        self.tree.heading("fecha", text="Fecha")

        self.tree.column("paciente", width=150)
        self.tree.column("hora", width=80)
        self.tree.column("estado", width=100)
        self.tree.column("obra_social", width=120)
        self.tree.column("num_afiliado", width=100)
        self.tree.column("fecha", width=100)

        scrollbar = ttk.Scrollbar(frame_turnos, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.pack(side=RIGHT, fill=Y)

        # Cargar todos los turnos inicialmente
        self.ver_todos_turnos()

    def cargar_pacientes(self):
        """Carga la información de todos los pacientes para uso posterior"""
        pacientes_lista = obtener_pacientes_por_medico(self.medico_id)
        for paciente in pacientes_lista:
            self.pacientes[paciente["id"]] = paciente

    def marcar_dias_con_turnos(self):
        """Marca en verde los días que tienen turnos asignados"""
        import datetime

        # Obtener todos los turnos del médico
        todos_turnos = supabase.table("turnos").select("fecha").eq("medico_id", self.medico_id).execute().data

        # Crear un conjunto de fechas únicas con turnos
        fechas_con_turnos = set()
        for turno in todos_turnos:
            fechas_con_turnos.add(turno["fecha"])

        # Marcar cada fecha con turnos en el calendario
        for fecha_str in fechas_con_turnos:
            try:
                # Convertir la cadena de fecha (formato YYYY-MM-DD) a objeto datetime.date
                year, month, day = map(int, fecha_str.split('-'))
                fecha_obj = datetime.date(year, month, day)

                # Ahora crear el evento con el objeto date
                self.cal.calevent_create(fecha_obj, "Turnos asignados", "turno")
            except (ValueError, TypeError) as e:
                print(f"Error al procesar la fecha {fecha_str}: {e}")

        # Configurar el tag para que se muestre en verde
        self.cal.tag_config("turno", background="green", foreground="white")

    def ver_todos_turnos(self):
        """Muestra todos los turnos asignados sin filtrar por fecha"""
        self.tree.delete(*self.tree.get_children())
        turnos = obtener_todos_los_turnos(self.medico_id)
        self._mostrar_turnos(turnos, mostrar_fecha=True)

        # Mostrar botón para ver turnos del día seleccionado
        self.btn_todos_turnos.config(text="Ver turnos del día seleccionado",
                                     command=lambda: self.cargar_turnos())

    def cargar_turnos(self, event=None):
        """Carga los turnos para la fecha seleccionada"""
        fecha = self.cal.get_date()
        self.tree.delete(*self.tree.get_children())

        turnos = obtener_turnos_del_dia(self.medico_id, fecha)
        self._mostrar_turnos(turnos, mostrar_fecha=False)

        # Cambiar botón para ver todos los turnos
        self.btn_todos_turnos.config(text="Ver todos los turnos",
                                     command=self.ver_todos_turnos)

    def _mostrar_turnos(self, turnos, mostrar_fecha=False):
        """Muestra los turnos en el treeview"""
        for t in turnos:
            paciente_id = t["paciente_id"]
            paciente_info = self.pacientes.get(paciente_id, {})

            nombre_completo = f"{paciente_info.get('apellido', '')}, {paciente_info.get('nombre', '')}"
            obra_social = paciente_info.get('obra_social', '-')
            num_afiliado = paciente_info.get('numero_afiliado', '-')

            valores = [
                nombre_completo,
                t["hora_inicio"],
                t["estado"],
                obra_social,
                num_afiliado
            ]

            # Añadir fecha si es necesario
            if mostrar_fecha:
                valores.append(t["fecha"])
            else:
                valores.append("")  # Columna vacía para mantener consistencia

            # Insertar datos del turno
            item_id = self.tree.insert("", END, iid=t["id"], values=tuple(valores))

        # Vincular evento de doble clic
        self.tree.bind("<Double-1>", self.on_turno_select)

    def on_turno_select(self, event):
        """Maneja la selección de un turno para mostrar opciones"""
        turno_id = self.tree.focus()
        if not turno_id:
            return

        # Obtener datos del turno seleccionado de la base de datos
        turno_data = supabase.table("turnos").select("*").eq("id", turno_id).execute().data
        if not turno_data:
            return

        turno = turno_data[0]

        # Crear ventana emergente con opciones para este turno
        turno_window = Toplevel(self)
        turno_window.title("Gestionar Turno")
        turno_window.geometry("350x300")
        turno_window.resizable(False, False)

        # Obtener datos del turno seleccionado del treeview
        item = self.tree.item(turno_id)
        valores = item['values']
        paciente = valores[0]
        estado = valores[2]

        # Mostrar información del turno
        Label(turno_window, text=f"Paciente: {paciente}", font=("Arial", 12)).pack(pady=5)
        Label(turno_window, text=f"Estado actual: {estado}", font=("Arial", 10)).pack(pady=5)

        # Botones para cambiar estado (solo completar y cancelar)
        frame_botones = Frame(turno_window)
        frame_botones.pack(pady=10)

        Button(frame_botones, text="Completar",
               command=lambda: self.cambiar_estado_turno(turno_id, "completado", turno_window),
               bg="#4CAF50", fg="white", width=12).pack(pady=5)

        Button(frame_botones, text="Cancelar",
               command=lambda: self.cambiar_estado_turno(turno_id, "cancelado", turno_window),
               bg="#F44336", fg="white", width=12).pack(pady=5)

        # Si el estado es completado, mostrar las notas
        if estado == "completado" and "notas" in turno and turno["notas"]:
            notas_frame = ttk.LabelFrame(turno_window, text="Notas de la consulta")
            notas_frame.pack(fill="both", expand=True, padx=10, pady=5)

            # Usar un Text widget para mostrar las notas con scroll si son largas
            notas_text = Text(notas_frame, wrap=WORD, height=5, width=30)
            notas_text.insert(END, turno["notas"])
            notas_text.config(state=DISABLED)  # Hacer el texto de solo lectura
            notas_text.pack(fill="both", expand=True, padx=5, pady=5)

            scrollbar = ttk.Scrollbar(notas_text, orient="vertical", command=notas_text.yview)
            notas_text.configure(yscrollcommand=scrollbar.set)
            scrollbar.pack(side=RIGHT, fill=Y)

        Button(turno_window, text="Cerrar", command=turno_window.destroy,
               bg="#9E9E9E", fg="white", width=10).pack(pady=10)

    def cambiar_estado_turno(self, turno_id, nuevo_estado, window=None):
        """Cambia el estado de un turno"""
        if nuevo_estado == "completado":
            notas = simpledialog.askstring("Notas", "Ingrese notas de consulta:")
            if notas is not None:  # Si el usuario no canceló el diálogo
                completar_turno(turno_id, notas)
                messagebox.showinfo("Éxito", "Turno completado correctamente")
        elif nuevo_estado == "cancelado":
            if messagebox.askyesno("Confirmar", "¿Está seguro de cancelar este turno?"):
                cancelar_turno(turno_id)
                messagebox.showinfo("Éxito", "Turno cancelado correctamente")

        # Cerrar ventana si existe
        if window:
            window.destroy()

        # Recargar turnos
        # Si estamos viendo todos los turnos, mantener esa vista
        if self.btn_todos_turnos.cget("text") == "Ver turnos del día seleccionado":
            self.ver_todos_turnos()
        else:
            self.cargar_turnos()
