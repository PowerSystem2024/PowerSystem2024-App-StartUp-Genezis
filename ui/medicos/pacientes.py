# ui/medicos/pacientes.py

from tkinter import *
from tkinter import ttk, messagebox
from controllers.med_controller import obtener_pacientes_por_medico, obtener_historial_paciente

class PacientesFrame(Frame):
    def __init__(self, parent, medico_id):
        super().__init__(parent)
        self.parent = parent
        self.medico_id = medico_id
        self.pacientes = []

        Label(self, text="Pacientes Atendidos", font=("Arial", 16, "bold")).pack(pady=10)

        # Tabla de pacientes
        self.tree = ttk.Treeview(self, columns=("id", "nombre", "documento", "obra_social"), show="headings", height=10)
        self.tree.heading("id", text="ID")
        self.tree.heading("nombre", text="Nombre")
        self.tree.heading("documento", text="Documento")
        self.tree.heading("obra_social", text="Obra Social")
        self.tree.pack(padx=10, pady=10)

        # Botón para ver historial
        Button(self, text="Ver Historial del Paciente", command=self.ver_historial).pack(pady=5)

        self.cargar_pacientes()

    def cargar_pacientes(self):
        self.tree.delete(*self.tree.get_children())
        self.pacientes = obtener_pacientes_por_medico(self.medico_id)
        for p in self.pacientes:
            nombre = f"{p.get('nombre', '')} {p.get('apellido', '')}".strip()
            self.tree.insert("", "end", iid=p["id"], values=(
                p["id"],
                nombre,
                p.get("num_afiliado", "—"),
                p.get("obra_social", "—")
            ))

    def ver_historial(self):
        seleccionado = self.tree.focus()
        if seleccionado:
            historial = obtener_historial_paciente(seleccionado)
            if not historial:
                messagebox.showinfo("Historial vacío", "Este paciente no tiene turnos registrados.")
                return
            historial_str = ""
            for t in historial:
                historial_str += f"{t['fecha']} - {t['estado']} - {t.get('notas', '')}\n"
            messagebox.showinfo("Historial de Turnos", historial_str)
        else:
            messagebox.showwarning("Atención", "Seleccione un paciente.")
