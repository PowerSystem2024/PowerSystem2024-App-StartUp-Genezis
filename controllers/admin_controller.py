# controllers/admin_controller.py

from database.db_manager import DatabaseManager
from utils.date_utils import fecha_hora_actual_utc
from controllers import med_controller  # Importamos el controlador de médicos


class AdminController:
    def __init__(self):
        self.db = DatabaseManager()

    # ====================================
    # USUARIOS
    # ====================================

    def get_all_users(self):
        return self.db.fetch_all("usuarios")

    def create_user(self, data: dict):
        data["creado_en"] = fecha_hora_actual_utc()
        return self.db.insert("usuarios", data)

    def update_user(self, user_id, data: dict):
        data["actualizado_en"] = fecha_hora_actual_utc()
        return self.db.update("usuarios", user_id, data)

    def delete_user(self, user_id):
        return self.db.delete("usuarios", user_id)

    # ====================================
    # INSTITUCIONES
    # ====================================

    def get_all_institutions(self):
        return self.db.fetch_all("instituciones")

    def create_institution(self, data: dict):
        data["creado_en"] = fecha_hora_actual_utc()
        return self.db.insert("instituciones", data)

    def update_institution(self, institution_id, data: dict):
        data["actualizado_en"] = fecha_hora_actual_utc()
        return self.db.update("instituciones", institution_id, data)

    def delete_institution(self, institution_id):
        return self.db.delete("instituciones", institution_id)

    # ====================================
    # REPORTES Y ESTADÍSTICAS
    # ====================================

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

    # ====================================
    # INFO EXTENDIDA POR USUARIO
    # ====================================

    def get_medico_id_by_user_id(self, user_id):
        medicos = med_controller.obtener_medicos()
        for medico in medicos:
            if medico["usuario_id"] == user_id:
                return medico["id"]
        return None

    def get_paciente_id_by_user_id(self, user_id):
        pacientes = self.db.fetch_all("pacientes").data
        for paciente in pacientes:
            if paciente["usuario_id"] == user_id:
                return paciente["id"]
        return None

    def get_institucion_id_by_user_id(self, user_id):
        instituciones = self.db.fetch_all("instituciones").data
        for inst in instituciones:
            if inst["usuario_id"] == user_id:
                return inst["id"]
        return None

    def get_horarios_medico(self, user_id):
        """
        Obtiene los horarios disponibles de un médico de forma legible
        """
        medico_id = self.get_medico_id_by_user_id(user_id)
        if not medico_id:
            return []

        horarios_raw = med_controller.obtener_horarios_disponibles(medico_id)
        horarios_formateados = []

        # Mapeo de días de la semana
        dias_semana = {
            0: "Lunes", 1: "Martes", 2: "Miércoles", 3: "Jueves",
            4: "Viernes", 5: "Sábado", 6: "Domingo"
        }

        for horario in horarios_raw:
            dia_nombre = dias_semana.get(horario.get("dia_semana", 0), "Desconocido")
            hora_inicio = horario.get("hora_inicio", "00:00")
            hora_fin = horario.get("hora_fin", "00:00")

            horario_formateado = f"{dia_nombre}: {hora_inicio} - {hora_fin}"
            horarios_formateados.append(horario_formateado)

        return horarios_formateados

    def get_pacientes_medico(self, user_id):
        """
        Obtiene los pacientes atendidos por un médico con información legible
        """
        medico_id = self.get_medico_id_by_user_id(user_id)
        if not medico_id:
            return []

        pacientes_raw = med_controller.obtener_pacientes_por_medico(medico_id)
        pacientes_formateados = []

        for paciente in pacientes_raw:
            # Obtener información del usuario asociado al paciente
            usuario_info = self.db.fetch_by_id("usuarios", paciente.get("usuario_id"))

            if usuario_info and usuario_info.data:
                # Manejar si data es una lista o un diccionario
                if isinstance(usuario_info.data, list) and len(usuario_info.data) > 0:
                    user_data = usuario_info.data[0]
                elif isinstance(usuario_info.data, dict):
                    user_data = usuario_info.data
                else:
                    user_data = None

                if user_data:
                    nombre = user_data.get("nombre", "Sin nombre")
                    email = user_data.get("email", "Sin email")

                    # Formatear información del paciente
                    paciente_info = f"{nombre} ({email})"

                    # Agregar información adicional si está disponible
                    if paciente.get("telefono"):
                        paciente_info += f" - Tel: {paciente.get('telefono')}"

                    pacientes_formateados.append(paciente_info)
                else:
                    # Fallback si no se puede procesar la información del usuario
                    pacientes_formateados.append(f"Paciente ID: {paciente.get('id', 'Desconocido')}")
            else:
                # Fallback si no se encuentra la información del usuario
                pacientes_formateados.append(f"Paciente ID: {paciente.get('id', 'Desconocido')}")

        return pacientes_formateados

    def get_info_paciente(self, user_id):
        paciente_id = self.get_paciente_id_by_user_id(user_id)
        if paciente_id:
            return self.db.fetch_by_id("pacientes", paciente_id)
        return None

    def get_info_institucion(self, user_id):
        institucion_id = self.get_institucion_id_by_user_id(user_id)
        if institucion_id:
            return self.db.fetch_by_id("instituciones", institucion_id)
        return None

    # ====================================
    # MÉTODOS ADICIONALES PARA MEJORAR LA UI
    # ====================================

    def get_medico_full_info(self, user_id):
        """
        Obtiene información completa y formateada de un médico
        """
        medico_id = self.get_medico_id_by_user_id(user_id)
        if not medico_id:
            return None

        # Obtener datos básicos del médico
        medicos = med_controller.obtener_medicos()
        medico_data = None
        for medico in medicos:
            if medico["id"] == medico_id:
                medico_data = medico
                break

        if not medico_data:
            return None

        # Obtener información de la institución
        institucion_info = self.db.fetch_by_id("instituciones", medico_data.get("institucion_id"))
        institucion_nombre = "Sin institución"
        if institucion_info and institucion_info.data:
            # Manejar si data es una lista o un diccionario
            if isinstance(institucion_info.data, list) and len(institucion_info.data) > 0:
                institucion_nombre = institucion_info.data[0].get("nombre", "Sin nombre")
            elif isinstance(institucion_info.data, dict):
                institucion_nombre = institucion_info.data.get("nombre", "Sin nombre")

        # Formatear información completa
        info_completa = {
            "especialidad": medico_data.get("especialidad", "Sin especialidad"),
            "matricula": medico_data.get("matricula", "Sin matrícula"),
            "institucion": institucion_nombre,
            "duracion_turno": f"{medico_data.get('duracion_turno', 30)} minutos",
            "horarios": self.get_horarios_medico(user_id),
            "pacientes": self.get_pacientes_medico(user_id),
            "total_pacientes": len(self.get_pacientes_medico(user_id))
        }

        return info_completa