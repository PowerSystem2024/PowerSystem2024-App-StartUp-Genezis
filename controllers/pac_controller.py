import os
from dotenv import load_dotenv
from supabase import create_client
from utils.date_utils import fecha_hora_actual_utc
from utils.date_utils import fecha_hora_actual_utc



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

# Función para BUSCAR turnos médicos disponibles.
def buscar_turnos_disponibles(especialidad, fecha):

    # Trae todos los médicos de esa especialidad
    medicos = supabase.table("medicos") \
        .select("id, nombre") \
        .eq("especialidad", especialidad) \
        .execute().data

    medicos_disponibles = []

    # Para cada medico, revisar si tiene algún turno libre ese día
    for medico in medicos:
        medico_id = medico["id"]
    # Buscar turnos YA reservados para ese médico en esa fecha

        turnos_reservados = supabase.table("turnos") \
            .select("hora_inicio") \
            .eq("medico_id", medico_id) \
            .eq("fecha", fecha) \
            .neq("estado", "cancelado") \
            .execute().data

        horas_ocupadas = [turno["hora_inicio"] for turno in turnos_reservados]

        todos_los_horarios = [f"{h:02}:00" for h in range(9, 18)]

    # Horarios disponibles para ese médico
        horarios_disponibles = [hora for hora in todos_los_horarios if hora not in horas_ocupadas]

        if horarios_disponibles:
        # Agregar el médico a la lista si tiene al menos 1 horario disponible
            medicos_disponibles.append({
            "medico_id": medico_id,
            "nombre": medico["nombre"],
            "horarios_disponibles": horarios_disponibles
        })

    return medicos_disponibles



# Función para RESERVAR un turno médico.
def reservar_turno(paciente_id, medico_id, fecha, hora_inicio, notas=""):

# Verificar si ya existe un turno para ese médico en esa fecha y hora

    turnos_existentes = supabase.table("turnos") \
        .select("id") \
        .eq("medico_id", medico_id) \
        .eq("fecha", fecha) \
        .eq("hora_inicio", hora_inicio) \
        .neq("estado", "cancelado") \
        .execute()

    if turnos_existentes.data:
        # Ya existe un turno para ese horario
        return {"error": "El médico ya tiene un turno reservado en ese horario."}

    # Insertar el nuevo turno
    nuevo_turno = {
        "paciente_id": paciente_id,
        "medico_id": medico_id,
        "fecha": fecha,
        "hora_inicio": hora_inicio,
        "estado": "pendiente",
        "notas": notas,
        "creado_en": fecha_hora_actual_utc(),
        "actualizado_en": fecha_hora_actual_utc()
    }

    resultado = supabase.table("turnos").insert(nuevo_turno).execute()

    return resultado

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
    # Buscar el turno para validar
    turno = supabase.table("turnos") \
        .select("*") \
        .eq("id", turno_id) \
        .eq("paciente_id", paciente_id) \
        .neq("estado", "cancelado") \
        .single() \
        .execute()

    if not turno.data:
        return {"error": "Turno no encontrado o ya fue cancelado."}

    # Actualizar el estado del turno
    resultado = supabase.table("turnos") \
        .update({
            "estado": "cancelado",
            "notas": motivo_cancelacion,
            "actualizado_en": fecha_hora_actual_utc()
        }) \
        .eq("id", turno_id) \
        .execute()

    return {"exito": True, "mensaje": "El turno fue cancelado correctamente."}



# Función para ver HISTORIAL de Turnos
def obtener_historial_turnos(paciente_id):

    # Turnos futuros o del día
    turnos_proximos = supabase.table("turnos") \
        .select("*") \
        .eq("paciente_id", paciente_id) \
        .gte("fecha", fecha_hora_actual_utc()) \
        .neq("estado", "cancelado") \
        .order("fecha") \
        .execute().data

    # Turnos pasados
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





