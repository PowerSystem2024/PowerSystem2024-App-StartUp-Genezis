from tkinter import *
from tkinter import ttk, messagebox
from controllers.med_controller import obtener_pacientes_por_medico, obtener_historial_paciente


class PacientesFrame(Frame):
    def __init__(self, parent, medico_id):
        super().__init__(parent)
        self.medico_id = medico_id
        self.botones = []  # Para mantener referencia a los botones

        Label(self, text="Pacientes Atendidos", font=("Arial", 14, "bold")).pack(pady=10)

        # Frame para contener el treeview y un scrollbar
        frame_tree = Frame(self)
        frame_tree.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # Scrollbar para el treeview
        scrollbar = ttk.Scrollbar(frame_tree)
        scrollbar.pack(side=RIGHT, fill=Y)

        # Modificación de las columnas: agregamos estado y mantenemos ver_nota
        self.tree = ttk.Treeview(frame_tree, columns=("nombre", "obra_social", "numero_afiliado", "estado", "ver_nota"),
                                 show="headings", yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.tree.yview)

        self.tree.heading("nombre", text="Nombre")
        self.tree.heading("obra_social", text="Obra Social")
        self.tree.heading("numero_afiliado", text="Número de Afiliado")
        self.tree.heading("estado", text="Estado")
        self.tree.heading("ver_nota", text="Ver Nota")

        # Configurar ancho de columnas
        self.tree.column("nombre", width=150)
        self.tree.column("obra_social", width=120)
        self.tree.column("numero_afiliado", width=120)
        self.tree.column("estado", width=100)
        self.tree.column("ver_nota", width=80, anchor=CENTER)

        self.tree.pack(side=LEFT, fill=BOTH, expand=True)

        # Frame para contener los botones que estarán alineados con el treeview
        self.frame_botones = Frame(self)
        self.frame_botones.pack(fill=X, padx=10)

        # Cuando se dibuja o actualiza el treeview, actualizar los botones
        self.tree.bind("<Map>", self.actualizar_botones)
        self.tree.bind("<Configure>", self.actualizar_botones)
        self.tree.bind("<Expose>", self.actualizar_botones)

        self.cargar()

    def cargar(self):
        self.tree.delete(*self.tree.get_children())
        # Limpiar botones existentes
        for btn in self.botones:
            btn.destroy()
        self.botones = []

        pacientes = obtener_pacientes_por_medico(self.medico_id)
        for p in pacientes:
            nombre = f"{p.get('nombre', '')} {p.get('apellido', '')}"
            # Obtenemos el estado del último turno del paciente
            historial = obtener_historial_paciente(p["id"])
            estado = historial[0].get('estado', '-') if historial else '-'

            self.tree.insert("", END, iid=p["id"], values=(
                nombre.strip(),
                p.get("obra_social", "-"),
                p.get("numero_afiliado", "-"),
                estado,
                "Ver"  # Mantenemos el texto como referencia
            ))

        # Después de insertar todos los elementos, actualizamos los botones
        self.actualizar_botones()

    def actualizar_botones(self, event=None):
        # Eliminar botones existentes
        for btn in self.botones:
            btn.destroy()
        self.botones = []

        # Crear nuevos botones para cada fila visible
        for item_id in self.tree.get_children():
            # Verificar si el ítem es visible
            if self.tree.exists(item_id):
                bbox = self.tree.bbox(item_id, column=4)  # Columna "Ver Nota"
                if bbox:  # Solo si es visible
                    x, y, width, height = bbox
                    btn = Button(self.tree, text="Ver", bg="#0078D7", fg="white",
                                 command=lambda pid=item_id: self.abrir_ventana_nota(pid))
                    btn.place(x=x + width // 2 - 15, y=y + 2, width=30, height=height - 4)
                    self.botones.append(btn)

    def abrir_ventana_nota(self, paciente_id):
        # Obtener el historial del paciente para mostrar sus notas
        historial = obtener_historial_paciente(paciente_id)
        if historial:
            # Crear una nueva ventana para mostrar las notas
            ventana_nota = Toplevel(self)
            ventana_nota.title("Notas del Paciente")
            ventana_nota.geometry("500x400")

            # Crear un widget de texto para mostrar todas las notas
            txt_nota = Text(ventana_nota, wrap=WORD)
            txt_nota.pack(fill=BOTH, expand=True, padx=10, pady=10)

            # Insertar cada nota con formato
            for t in historial:
                txt_nota.insert(END, f"Fecha: {t['fecha']}\n")
                txt_nota.insert(END, f"Estado: {t['estado']}\n")
                txt_nota.insert(END, f"Nota: {t.get('notas', '')}\n")
                txt_nota.insert(END, "-" * 40 + "\n\n")

            txt_nota.config(state=DISABLED)  # Hacer el texto de solo lectura

            # Botón para cerrar la ventana
            Button(ventana_nota, text="Cerrar", command=ventana_nota.destroy).pack(pady=10)
        else:
            messagebox.showinfo("Sin datos", "Este paciente no tiene notas registradas.")
