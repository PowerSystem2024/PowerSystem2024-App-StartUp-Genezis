import os
from dotenv import load_dotenv
from supabase import create_client
from utils.date_utils import fecha_hora_actual_utc
from datetime import datetime
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


# ================================ #
#          CRUD PACIENTES          #
# ================================ #

# Función para crear un paciente:
def create_paciente(usuario_id, fecha_nacimiento, genero, telefono, obra_social, num_afiliado, creado_en,
                   actualizado_en):
    data = {
        "usuario_id": usuario_id,
        "fecha_nacimiento": fecha_nacimiento,
        "genero": genero,
        "telefono": telefono,
        "obra_social": obra_social,
        "num_afiliado": num_afiliado,
        "creado_en": fecha_hora_actual_utc,
        "actualizado_en": actualizado_en
    }

    return supabase.table("pacientes").insert(data).execute().data

# Función para obtener un paciente:
def get_paciente():
    return supabase.table("pacientes").select("*").execute().data

# Función para actualizar los datos de un paciente:
def update_paciente(paciente_id, nuevos_datos):
    nuevos_datos["actualizado_en"] = fecha_hora_actual_utc()
    return supabase.table("pacientes").update(nuevos_datos).eq("id", paciente_id).execute().data

# Función para eliminar un paciente:
def delete_paciente(paciente_id):
    return supabase.table("pacientes").delete().eq("id", paciente_id).execute().data


# ================================ #
#         TURNOS PACIENTES         #
# ================================ #

# Función para BUSCAR horarios disponibles.

def buscar_turnos_disponibles(especialidad, fecha, institucion_id):
    try:
        dia_semana = datetime.strptime(fecha, "%Y-%m-%d").weekday()

        response = supabase.table("horarios_disponibles").select("*") \
            .eq("dia_semana", dia_semana) \
            .eq("activo", True) \
            .execute()

        turnos_disponibles = response.data
        print(f"[DEBUG] Turnos crudos desde Supabase: {turnos_disponibles}")

        resultados_filtrados = []

        for turno in turnos_disponibles:
            medico_id = turno.get("medico_id")

            if not medico_id:
                continue

            medico_response = supabase.table("medicos").select("id, institucion_id, especialidad, usuario:usuario_id(nombre, apellido)") \
                .eq("id", medico_id).single().execute()

            medico = medico_response.data
            if not medico:
                continue

            if medico["especialidad"] != especialidad:
                continue

            if medico["institucion_id"] != institucion_id:
                continue

            usuario = medico.get("usuario", {})
            nombre_medico = f"{usuario.get('nombre', '')} {usuario.get('apellido', '')}"

            resultados_filtrados.append({
                "id": turno["id"],
                "nombre_medico": nombre_medico,
                "fecha": fecha,
                "hora_inicio": turno["hora_inicio"][:5],
                "hora_fin": turno["hora_fin"][:5],
            })

        print(f"[DEBUG] Turnos disponibles encontrados: {resultados_filtrados}")
        return resultados_filtrados

    except Exception as e:
        print(f"[ERROR] buscar_turnos_disponibles: {e}")
        return []

#Función para RESERVAR un turno nuevo e insertarlo en la tabla turnos.
def reservar_turno(horario_id, usuario_id, fecha_turno):
    try:
        # Obtener horario
        horario = supabase.table("horarios_disponibles").select("*").eq("id", horario_id).single().execute()
        horario_data = horario.data

        if not horario_data:
            return {"exito": False, "mensaje": "No se encontró el horario seleccionado."}

        hora_inicio = horario_data["hora_inicio"]
        hora_fin = horario_data["hora_fin"]
        medico_id = horario_data["medico_id"]

        # Obtener el ID real del paciente usando usuario_id
        paciente_result = supabase.table("pacientes").select("id").eq("usuario_id", usuario_id).single().execute()
        if not paciente_result.data:
            print("[ERROR] Paciente no encontrado con usuario_id:", usuario_id)
            return {"exito": False, "mensaje": "Paciente no válido."}

        paciente_id_real = paciente_result.data["id"]

        # Validar si ya tiene turno en esa fecha y hora
        turno_existente = supabase.table("turnos").select("*") \
            .eq("paciente_id", paciente_id_real) \
            .eq("fecha", fecha_turno) \
            .eq("hora_inicio", hora_inicio).execute()

        if turno_existente.data:
            return {"exito": False, "mensaje": "Ya tiene un turno reservado en ese horario."}

        # Obtener la institución del médico
        medico_result = supabase.table("medicos").select("institucion_id").eq("id", medico_id).single().execute()
        if not medico_result.data:
            return {"exito": False, "mensaje": "No se encontró la institución del médico."}

        institucion_id = medico_result.data["institucion_id"]

        # Insertar el nuevo turno
        nuevo_turno = {
            "fecha": fecha_turno,
            "hora_inicio": hora_inicio,
            "hora_fin": hora_fin,
            "paciente_id": paciente_id_real,
            "medico_id": medico_id,
            "institucion_id": institucion_id,
            "estado": "pendiente"
        }

        insertar = supabase.table("turnos").insert(nuevo_turno).execute()

        if insertar.data:
            try: #Si se insertó el turno reservado, se elimina el horario disponible correspondiente.
                supabase.table("horarios_disponibles").delete().eq("id", horario_id).execute()
            except Exception as delete_error:
                print("[WARNING] Turno reservado pero no se pudo eliminar el horario disponible:", delete_error)
            return {"exito": True, "mensaje": "Turno reservado con éxito."}


    except Exception as e:
        print("[ERROR] al reservar turno:", e)
        return {"exito": False, "mensaje": "Ocurrió un error al reservar el turno."}


# Función para CONFIRMAR un turno médico.
def confirmar_turno(turno_id, paciente_id):
    # Buscar el turno para validar que le pertenece al paciente y está pendiente
    turno = supabase.table("turnos") \
        .select("*") \
        .eq("id", turno_id) \
        .eq("paciente_id", paciente_id) \
        .eq("estado", "pendiente") \
        .single() \
        .execute()

    if not turno.data:
        return {"error": "Turno no encontrado o ya fue confirmado/cancelado."}

    # Actualizar el estado del turno a confirmado
    resultado = supabase.table("turnos") \
        .update({
            "estado": "confirmado",
            "actualizado_en": fecha_hora_actual_utc()
        }) \
        .eq("id", turno_id) \
        .execute()

    return {"exito": True, "mensaje": "Turno confirmado correctamente."}

# Función para CANCELAR un turno.
def cancelar_turno(turno_id, paciente_id, motivo_cancelacion="Cancelado por el paciente"):
    try:
        # Buscar el turno para validar
        turno_response = supabase.table("turnos") \
            .select("*") \
            .eq("id", turno_id) \
            .eq("paciente_id", paciente_id) \
            .neq("estado", "cancelado") \
            .single() \
            .execute()

        turno = turno_response.data

        if not turno:
            return {"error": "Turno no encontrado o ya fue cancelado."}

        # Actualizar el estado del turno
        supabase.table("turnos") \
            .update({
                "estado": "cancelado",
                "notas": motivo_cancelacion,
                "actualizado_en": fecha_hora_actual_utc()
            }) \
            .eq("id", turno_id) \
            .execute()

        # Restaurar horario en horarios_disponibles
        fecha_str = turno["fecha"]  # formato: YYYY-MM-DD
        fecha_obj = datetime.strptime(fecha_str, "%Y-%m-%d")
        dia_semana = fecha_obj.weekday()  # lunes=0, domingo=6

        nuevo_horario = {
            "medico_id": turno["medico_id"],
            "hora_inicio": turno["hora_inicio"],
            "hora_fin": turno["hora_fin"],
            "dia_semana": dia_semana,
            "activo": True,
            "institucion_id": turno.get("institucion_id"),
            "creado_en": fecha_hora_actual_utc(),
            "actualizado_en": fecha_hora_actual_utc()
        }

        supabase.table("horarios_disponibles").insert(nuevo_horario).execute()

        return {"exito": True, "mensaje": "El turno fue cancelado correctamente y el horario fue liberado."}

    except Exception as e:
        print("[ERROR] al cancelar turno:", e)
        return {"error": "Ocurrió un error al cancelar el turno."}


# Función para ver HISTORIAL de Turnos
def obtener_historial_turnos(paciente_id):
    # Turnos futuros (o del día), incluyendo nombre del médico y especialidad
    turnos_proximos = supabase.table("turnos") \
        .select("""
            id,
            fecha,
            hora_inicio,
            estado,
            medico_id,
            medico:medicos (
                nombre,
                apellido,
                especialidad:especialidades (
                    nombre
                )
            )
        """) \
        .eq("paciente_id", paciente_id) \
        .gte("fecha", fecha_hora_actual_utc()) \
        .neq("estado", "cancelado") \
        .order("fecha") \
        .execute().data

    # Enriquecer los datos para el frontend
    for turno in turnos_proximos:
        medico = turno.get("medico", {})
        especialidad = medico.get("especialidad", {})
        turno["nombre_medico"] = f"{medico.get('nombre', '')} {medico.get('apellido', '')}".strip()
        turno["especialidad"] = especialidad.get("nombre", "No especificada")

    # Turnos pasados (sin join detallado por ahora)
    turnos_pasados = supabase.table("turnos") \
        .select("id, fecha, hora_inicio, estado, medico_id") \
        .eq("paciente_id", paciente_id) \
        .lt("fecha", fecha_hora_actual_utc()) \
        .order("fecha", desc=True) \
        .execute().data

    return {
        "proximos": turnos_proximos,
        "pasados": turnos_pasados
    }


def obtener_instituciones():
    return supabase.table("instituciones").select("id, nombre").execute().data

def obtener_medicos():
    return supabase.table("medicos").select("id, especialidad").execute().data

def obtener_especialidades():
    medicos = obtener_medicos()
    especialidades = list({medico["especialidad"] for medico in medicos if medico.get("especialidad")})
    especialidades.sort()
    return especialidades

def debug_obtener_todos_los_horarios():
    try:
        resultado = supabase.table("horarios_disponibles") \
            .select("*") \
            .execute()

        print("[DEBUG] Horarios disponibles recibidos:")
        for horario in resultado.data:
            print(horario)

        return resultado.data

    except Exception as e:
        print(f"[ERROR] al obtener horarios disponibles: {e}")
        return []

def obtener_paciente_id_por_usuario(usuario_id):
    resultado = supabase.table("pacientes") \
        .select("id") \
        .eq("usuario_id", usuario_id) \
        .single() \
        .execute()

    if resultado.data:
        return resultado.data["id"]
    else:
        return None








