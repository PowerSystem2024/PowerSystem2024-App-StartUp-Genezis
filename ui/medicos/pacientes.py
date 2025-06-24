from tkinter import *
from tkinter import ttk, messagebox
from controllers.med_controller import obtener_pacientes_por_medico, obtener_historial_paciente

class PacientesFrame(Frame):
    def __init__(self, parent, medico_id):
        super().__init__(parent)
        self.medico_id = medico_id

        Label(self, text="Pacientes Atendidos", font=("Arial", 14, "bold")).pack(pady=10)

        self.tree = ttk.Treeview(self, columns=("id", "nombre", "obra_social"), show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("nombre", text="Nombre")
        self.tree.heading("obra_social", text="Obra Social")
        self.tree.pack(padx=10, pady=10)

        Button(self, text="Ver Historial", command=self.ver_historial).pack(pady=5)

        self.cargar()

    def cargar(self):
        self.tree.delete(*self.tree.get_children())
        for p in obtener_pacientes_por_medico(self.medico_id):
            nombre = f"{p.get('nombre', '')} {p.get('apellido', '')}"
            self.tree.insert("", END, iid=p["id"], values=(p["id"], nombre.strip(), p.get("obra_social", "-")))

    def ver_historial(self):
        sel = self.tree.focus()
        if sel:
            historial = obtener_historial_paciente(sel)
            if historial:
                info = "\n".join([f"{t['fecha']} - {t['estado']} - {t.get('notas', '')}" for t in historial])
                messagebox.showinfo("Historial", info)
            else:
                messagebox.showinfo("Sin datos", "Este paciente no tiene historial.")