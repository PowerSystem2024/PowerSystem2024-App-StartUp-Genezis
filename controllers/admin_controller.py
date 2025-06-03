# controllers/admin_controller.py

# Importa la clase para la gestión de la base de datos.
from database.db_manager import DatabaseManager
# Importa la función para obtener la fecha y hora actual en UTC.
from utils.date_utils import fecha_hora_actual_utc


# Clase principal para controlar operaciones administrativas.
class AdminController:
    # Inicializa la conexión con la base de datos
    def __init__(self):
        self.db = DatabaseManager()

    # ====================================
    # USUARIOS
    # ====================================

    # Obtiene todos los usuarios de la base de datos
    def get_all_users(self):
        return self.db.fetch_all("usuarios")

    # Crea un nuevo usuario, añadiendo la fecha de creación automáticamente
    def create_user(self, data: dict):
        data["creado_en"] = fecha_hora_actual_utc()
        return self.db.insert("usuarios", data)

    # Actualiza un usuario existente, añadiendo la fecha de última actualización
    def update_user(self, user_id, data: dict):
        data["actualizado_en"] = fecha_hora_actual_utc()
        return self.db.update("usuarios", user_id, data)

    # Elimina un usuario por su ID.
    def delete_user(self, user_id):
        return self.db.delete("usuarios", user_id)

    # ====================================
    # INSTITUCIONES
    # ====================================

    # Obtiene todas las instituciones de la base de datos
    def get_all_institutions(self):
        return self.db.fetch_all("instituciones")

    # Crea una nueva institución, añadiendo la fecha de creación
    def create_institution(self, data: dict):
        data["creado_en"] = fecha_hora_actual_utc()
        return self.db.insert("instituciones", data)

    # Actualiza una institución existente, con su fecha de actualización
    def update_institution(self, institution_id, data: dict):
        data["actualizado_en"] = fecha_hora_actual_utc()
        return self.db.update("instituciones", institution_id, data)

    # Elimina una institución por su ID.
    def delete_institution(self, institution_id):
        return self.db.delete("instituciones", institution_id)

    # ====================================
    # REPORTES Y ESTADÍSTICAS
    # ====================================

    # Recopila y devuelve estadísticas clave del sistema
    def get_system_stats(self):
        usuarios = self.get_all_users()
        instituciones = self.get_all_institutions()
        medicos = self.db.fetch_all("medicos")
        pacientes = self.db.fetch_all("pacientes")
        turnos = self.db.fetch_all("turnos")

        return {
            "usuarios_totales": len(usuarios.data),
            "instituciones_totales": len(instituciones.data),
            "medicos_totales": len(medicos.data),
            "pacientes_totales": len(pacientes.data),
            "turnos_totales": len(turnos.data),
        }