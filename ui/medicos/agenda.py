from tkinter import *
from tkinter import ttk, messagebox, simpledialog
from tkcalendar import Calendar
from controllers.med_controller import obtener_turnos_del_dia, completar_turno, cancelar_turno, \
    obtener_pacientes_por_medico, supabase


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

        # Tabla de turnos mejorada
        frame_turnos = Frame(self)
        frame_turnos.pack(fill=BOTH, expand=True, padx=10, pady=10)

        self.tree = ttk.Treeview(frame_turnos,
                                 columns=("paciente", "hora", "estado", "obra_social", "num_afiliado"),
                                 show="headings",
                                 height=10)
        self.tree.heading("paciente", text="Paciente")
        self.tree.heading("hora", text="Hora")
        self.tree.heading("estado", text="Estado")
        self.tree.heading("obra_social", text="Obra Social")
        self.tree.heading("num_afiliado", text="Nº Afiliado")

        self.tree.column("paciente", width=150)
        self.tree.column("hora", width=80)
        self.tree.column("estado", width=100)
        self.tree.column("obra_social", width=120)
        self.tree.column("num_afiliado", width=100)

        scrollbar = ttk.Scrollbar(frame_turnos, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.pack(side=RIGHT, fill=Y)

        # Cargar los turnos iniciales
        self.cargar_turnos()

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

    def cargar_turnos(self, event=None):
        """Carga los turnos para la fecha seleccionada"""
        fecha = self.cal.get_date()
        self.tree.delete(*self.tree.get_children())

        turnos = obtener_turnos_del_dia(self.medico_id, fecha)
        for t in turnos:
            paciente_id = t["paciente_id"]
            paciente_info = self.pacientes.get(paciente_id, {})

            nombre_completo = f"{paciente_info.get('apellido', '')}, {paciente_info.get('nombre', '')}"
            obra_social = paciente_info.get('obra_social', '-')
            num_afiliado = paciente_info.get('numero_afiliado', '-')

            # Insertar datos del turno
            item_id = self.tree.insert("", END, iid=t["id"], values=(
                nombre_completo,
                t["hora_inicio"],
                t["estado"],
                obra_social,
                num_afiliado
            ))

            # Crear frame para botones de acción para cada turno
            self.tree.bind("<Double-1>", self.on_turno_select)

    def on_turno_select(self, event):
        """Maneja la selección de un turno para mostrar opciones"""
        turno_id = self.tree.focus()
        if not turno_id:
            return

        # Crear ventana emergente con opciones para este turno
        turno_window = Toplevel(self)
        turno_window.title("Gestionar Turno")
        turno_window.geometry("300x250")
        turno_window.resizable(False, False)

        # Obtener datos del turno seleccionado
        item = self.tree.item(turno_id)
        valores = item['values']
        paciente = valores[0]
        estado = valores[2]

        # Mostrar información del turno
        Label(turno_window, text=f"Paciente: {paciente}", font=("Arial", 12)).pack(pady=5)
        Label(turno_window, text=f"Estado actual: {estado}", font=("Arial", 10)).pack(pady=5)

        # Botones para cambiar estado
        frame_botones = Frame(turno_window)
        frame_botones.pack(pady=10)

        Button(frame_botones, text="Completar",
               command=lambda: self.cambiar_estado_turno(turno_id, "completado", turno_window),
               bg="#4CAF50", fg="white", width=12).pack(pady=5)

        Button(frame_botones, text="Cancelar",
               command=lambda: self.cambiar_estado_turno(turno_id, "cancelado", turno_window),
               bg="#F44336", fg="white", width=12).pack(pady=5)

        Button(frame_botones, text="En Espera",
               command=lambda: self.cambiar_estado_turno(turno_id, "en_espera", turno_window),
               bg="#2196F3", fg="white", width=12).pack(pady=5)

        Button(frame_botones, text="Ausente",
               command=lambda: self.cambiar_estado_turno(turno_id, "ausente", turno_window),
               bg="#FF9800", fg="white", width=12).pack(pady=5)

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
        else:
            # Para otros estados, usar la API general de actualización
            supabase.table("turnos").update({"estado": nuevo_estado}).eq("id", turno_id).execute()
            messagebox.showinfo("Éxito", f"Estado cambiado a '{nuevo_estado}'")

        # Cerrar ventana si existe
        if window:
            window.destroy()

        # Recargar turnos
        self.cargar_turnos()
