# institucion/dashboard.py
import tkinter as tk
from tkinter import ttk, messagebox

# Importar desde los otros archivos de TU módulo
from . import config as inst_cfg # Configuraciones específicas de institución
from . import horarios as inst_hr_logic # Lógica de horarios

# Importar el controlador
from controllers import inst_controller

class InstitucionMainDashboard(tk.Frame):
    def __init__(self, master, institucion_id):
        super().__init__(master, bg=inst_cfg.COLOR_FONDO_DASHBOARD_INST)
        self.institucion_id = institucion_id
        self.current_institucion_data = None # Para los datos cargados

        self.pack(fill=tk.BOTH, expand=True) # El frame principal se expande

        # Frames para las dos "vistas" que este dashboard puede mostrar
        self.summary_view_frame = tk.Frame(self, bg=self.cget('bg'))
        self.edit_view_frame = tk.Frame(self, bg=self.cget('bg'))
        
        # Inicializar ambas vistas (pero solo una se mostrará a la vez)
        self._crear_summary_view_widgets(self.summary_view_frame)
        self._crear_edit_view_widgets(self.edit_view_frame)

        # Mostrar la vista de resumen por defecto
        self.show_summary_view()

    # --- Lógica para cambiar entre vistas ---
    def show_summary_view(self):
        self.edit_view_frame.pack_forget() # Ocultar vista de edición
        self.summary_view_frame.pack(fill=tk.BOTH, expand=True) # Mostrar vista de resumen
        self._load_summary_data() # Cargar/refrescar datos del resumen

    def show_edit_view(self):
        self.summary_view_frame.pack_forget() # Ocultar vista de resumen
        self.edit_view_frame.pack(fill=tk.BOTH, expand=True) # Mostrar vista de edición
        self._load_data_for_edit_form() # Cargar datos en el formulario de edición

    # --- Creación de Widgets para la Vista de Resumen (Tarjetas) ---
    def _crear_summary_view_widgets(self, parent_frame):
        # Frame para las tarjetas de resumen (las azules)
        summary_cards_container = tk.Frame(parent_frame, bg=parent_frame.cget('bg'))
        summary_cards_container.pack(pady=20, padx=20, fill=tk.X)

        # Tarjeta Médicos Disponibles (Placeholder)
        card1 = self._create_styled_card(summary_cards_container, inst_cfg.COLOR_TARJETA_RESUMEN_INST)
        card1.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=10)
        tk.Label(card1, text=inst_cfg.TEXTO_TARJETA_MEDICOS_DISPONIBLES, font=inst_cfg.FUENTE_TARJETA_TITULO, bg=inst_cfg.COLOR_TARJETA_RESUMEN_INST, fg=inst_cfg.COLOR_TEXTO_TARJETA_TITULO_INST).pack(pady=(10,5))
        self.lbl_medicos_disponibles_summary = tk.Label(card1, text="--", font=inst_cfg.FUENTE_TARJETA_VALOR, bg=inst_cfg.COLOR_TARJETA_RESUMEN_INST, fg=inst_cfg.COLOR_TEXTO_TARJETA_VALOR_INST)
        self.lbl_medicos_disponibles_summary.pack(pady=(0,10))

        # Tarjeta Turnos Activos (Placeholder)
        card2 = self._create_styled_card(summary_cards_container, inst_cfg.COLOR_TARJETA_RESUMEN_INST)
        card2.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=10)
        tk.Label(card2, text=inst_cfg.TEXTO_TARJETA_TURNOS_ACTIVOS, font=inst_cfg.FUENTE_TARJETA_TITULO, bg=inst_cfg.COLOR_TARJETA_RESUMEN_INST, fg=inst_cfg.COLOR_TEXTO_TARJETA_TITULO_INST).pack(pady=(10,5))
        self.lbl_turnos_activos_summary = tk.Label(card2, text="--", font=inst_cfg.FUENTE_TARJETA_VALOR, bg=inst_cfg.COLOR_TARJETA_RESUMEN_INST, fg=inst_cfg.COLOR_TEXTO_TARJETA_VALOR_INST)
        self.lbl_turnos_activos_summary.pack(pady=(0,10))
        
        # Tarjeta Horarios Institución
        card3 = self._create_styled_card(summary_cards_container, inst_cfg.COLOR_TARJETA_RESUMEN_INST)
        card3.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=10)
        tk.Label(card3, text=inst_cfg.TEXTO_TARJETA_HORARIOS_INSTITUCION, font=inst_cfg.FUENTE_TARJETA_TITULO, bg=inst_cfg.COLOR_TARJETA_RESUMEN_INST, fg=inst_cfg.COLOR_TEXTO_TARJETA_TITULO_INST).pack(pady=(10,5))
        self.lbl_horarios_summary = tk.Label(card3, text="Cargando...", font=inst_cfg.FUENTE_HORARIOS_TEXTO, bg=inst_cfg.COLOR_TARJETA_RESUMEN_INST, fg=inst_cfg.COLOR_TEXTO_TARJETA_VALOR_INST, wraplength=200, justify=tk.LEFT)
        self.lbl_horarios_summary.pack(pady=(0,10), expand=True, fill=tk.BOTH)

        # Botón para ir a la vista de edición (desde la vista de resumen)
        # Este botón podría estar aquí o ser el icono de lápiz en la barra lateral de main.py
        # que llame a self.show_edit_view() en esta instancia del dashboard.
        ttk.Button(parent_frame, text=inst_cfg.TEXTO_EDITAR_INSTITUCION_BTN, command=self.show_edit_view).pack(pady=20)

        # Frame para las tarjetas de detalle (las rosadas, placeholders)
        detail_cards_container = tk.Frame(parent_frame, bg=parent_frame.cget('bg'))
        detail_cards_container.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        for i in range(4):
            card_detail = self._create_styled_card(detail_cards_container, inst_cfg.COLOR_TARJETA_DETALLE_INST)
            detail_cards_container.grid_columnconfigure(i, weight=1)
            card_detail.grid(row=0, column=i, sticky="nsew", padx=5, pady=5)
            if i == 0:
                # Contenido de la primera tarjeta de detalle
                tk.Label(card_detail, text="Nombre:", bg=inst_cfg.COLOR_TARJETA_DETALLE_INST, anchor="w").pack(fill=tk.X)
                # ... más labels ...
            else:
                tk.Label(card_detail, text=f"Detalle {i+1}", bg=inst_cfg.COLOR_TARJETA_DETALLE_INST).pack(expand=True)
        detail_cards_container.grid_rowconfigure(0, weight=1)
    
    def _load_summary_data(self):
        if not self.institucion_id: return
        self.current_institucion_data = inst_controller.obtener_institucion_por_id(self.institucion_id)
        if self.current_institucion_data:
            horarios_db = self.current_institucion_data.get('horarios_atencion', '')
            self.lbl_horarios_summary.config(text=inst_hr_logic.formatear_horarios_para_display(horarios_db))
            # Aquí podrías llamar a otros controladores para los conteos si fuera necesario
            self.lbl_medicos_disponibles_summary.config(text="N/A") # Simulado
            self.lbl_turnos_activos_summary.config(text="N/A") # Simulado
        else:
            self.lbl_horarios_summary.config(text="Error al cargar datos.")
            messagebox.showerror("Error", "No se pudieron cargar los datos de la institución.")
    
    def _create_styled_card(self, parent, bg_color):
        return tk.Frame(parent, bg=bg_color, bd=1, relief=tk.RAISED, padx=10, pady=10)


    # --- Creación de Widgets para la Vista de Edición (Formulario) ---
    def _crear_edit_view_widgets(self, parent_frame):
        tk.Label(parent_frame, text=inst_cfg.TEXTO_TITULO_PANEL_EDICION.format(id=self.institucion_id), 
                 font=inst_cfg.FUENTE_EDIT_PANEL_TITULO, bg=parent_frame.cget('bg')).pack(pady=(10,20))
        
        form_fields_frame = ttk.Frame(parent_frame) # Usar ttk.Frame para consistencia si se usa ttk.Label/Entry
        form_fields_frame.pack(padx=20, pady=10, expand=True)

        self.edit_entries = {}
        fields_to_edit = {
            "Nombre:": "nombre", "Dirección:": "direccion", "Teléfono:": "telefono",
            "Email:": "email", "Horarios:": "horarios_atencion", "URL del Logo:": "logo_url"
        }
        for i, (label_text, db_key) in enumerate(fields_to_edit.items()):
            ttk.Label(form_fields_frame, text=label_text).grid(row=i, column=0, sticky=tk.W, padx=5, pady=5)
            entry = ttk.Entry(form_fields_frame, width=60)
            entry.grid(row=i, column=1, sticky=tk.EW, padx=5, pady=5)
            self.edit_entries[db_key] = entry
        form_fields_frame.columnconfigure(1, weight=1)

        button_bar_edit = ttk.Frame(parent_frame)
        button_bar_edit.pack(pady=20)
        ttk.Button(button_bar_edit, text=inst_cfg.TEXTO_GUARDAR_CAMBIOS_BTN, command=self._save_edited_data).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_bar_edit, text=inst_cfg.TEXTO_CANCELAR_BTN, command=self.show_summary_view).pack(side=tk.LEFT, padx=10) # Vuelve al resumen

    def _load_data_for_edit_form(self):
        # Los datos ya deberían estar en self.current_institucion_data si se cargó el resumen
        # O se pueden volver a cargar para asegurar frescura
        data_to_edit = inst_controller.obtener_institucion_por_id(self.institucion_id)
        if data_to_edit:
            self.current_institucion_data = data_to_edit # Actualizar
            for db_key, entry_widget in self.edit_entries.items():
                entry_widget.delete(0, tk.END)
                entry_widget.insert(0, self.current_institucion_data.get(db_key, ''))
        else:
            messagebox.showerror("Error", "No se pudieron cargar datos para edición.")
            self.show_summary_view() # Volver si hay error

    def _save_edited_data(self):
        if not self.institucion_id: return

        data_payload = {}
        for db_key, entry_widget in self.edit_entries.items():
            data_payload[db_key] = entry_widget.get().strip()

        if not data_payload.get("nombre"):
            messagebox.showerror("Validación", "El nombre es obligatorio.")
            return
        
        # Validación de horarios (opcional, usando institucion/horarios.py)
        is_valid_horario, horario_msg = inst_hr_logic.validar_formato_horarios(data_payload.get("horarios_atencion"))
        if not is_valid_horario:
            messagebox.showerror("Validación Horarios", horario_msg)
            return

        if inst_controller.editar_institucion(self.institucion_id, data_payload):
            messagebox.showinfo("Éxito", "Institución actualizada correctamente.")
            self.show_summary_view() # Volver al resumen y refrescar datos
        else:
            messagebox.showerror("Error", "No se pudo actualizar la institución.")

# --- Para probar este dashboard.py de forma aislada ---
if __name__ == '__main__':
    import sys
    import os
    # Asegurar que la raíz del proyecto esté en sys.path para que 'from controllers import ...' funcione
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

    from database.db_manager import supabase # Para inicializar la conexión

    if supabase:
        root = tk.Tk()
        root.title("Test Institucion Dashboard (Strict Files)")
        root.geometry("1000x700")
        
        # Simular un ID de institución existente en tu base de datos para probar
        test_institucion_id_val = 1 # CAMBIA ESTO AL ID DE UNA INSTITUCIÓN REAL EN TU DB
        if not test_institucion_id_val: # Si no se define un ID, no se puede probar bien
            tk.Label(root, text="Por favor, define un 'test_institucion_id_val' válido en el código para probar.").pack(pady=50)
        else:
            # Aquí, la MainApplication (o algo similar) sería la que instancia este dashboard.
            # Pasamos root como master y el ID de la institución.
            app_dashboard = InstitucionMainDashboard(root, institucion_id=test_institucion_id_val)
            app_dashboard.pack(fill=tk.BOTH, expand=True)
        
        root.mainloop()
    else:
        print("Supabase no se pudo inicializar. La prueba del dashboard no se ejecutará.")
