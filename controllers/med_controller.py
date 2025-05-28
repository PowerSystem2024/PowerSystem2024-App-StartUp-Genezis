# controllers/medico_controller.py

import os
from dotenv import load_dotenv
from supabase import create_client
from datetime import datetime

# Cargar variables de entorno
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


# ================================
# CRUD MÉDICOS
# ================================

def crear_medico(usuario_id, institucion_id, especialidad, matricula, duracion_turno):
    data = {
        "usuario_id": usuario_id,
        "institucion_id": institucion_id,
        "especialidad": especialidad,
        "matricula": matricula,
        "duracion_turno": duracion_turno,
        "creado_en": datetime.utcnow().isoformat()
    }
    return supabase.table("medicos").insert(data).execute().data


def obtener_medicos():
    return supabase.table("medicos").select("*").execute().data


def actualizar_medico(medico_id, nuevos_datos):
    nuevos_datos["actualizado_en"] = datetime.utcnow().isoformat()
    return supabase.table("medicos").update(nuevos_datos).eq("id", medico_id).execute().data


def eliminar_medico(medico_id):
    return supabase.table("medicos").delete().eq("id", medico_id).execute().data


# ================================
# AGENDA Y TURNOS
# ================================

def obtener_turnos_del_dia(medico_id, fecha):
    return supabase.table("turnos") \
        .select("*") \
        .eq("medico_id", medico_id) \
        .eq("fecha", fecha) \
        .neq("estado", "cancelado") \
        .execute().data


def completar_turno(turno_id, notas_consulta):
    return supabase.table("turnos") \
        .update({
        "estado": "completado",
        "notas": notas_consulta,
        "actualizado_en": datetime.utcnow().isoformat()
    }) \
        .eq("id", turno_id).execute().data


def cancelar_turno(turno_id):
    return supabase.table("turnos") \
        .update({
        "estado": "cancelado",
        "actualizado_en": datetime.utcnow().isoformat()
    }) \
        .eq("id", turno_id).execute().data


# ================================
# DISPONIBILIDAD HORARIA
# ================================

def agregar_horario_disponible(medico_id, dia_semana, hora_inicio, hora_fin):
    data = {
        "medico_id": medico_id,
        "dia_semana": dia_semana,
        "hora_inicio": hora_inicio,
        "hora_fin": hora_fin,
        "activo": True,
        "creado_en": datetime.utcnow().isoformat()
    }
    return supabase.table("horarios_disponibles").insert(data).execute().data


def eliminar_horario_disponible(horario_id):
    return supabase.table("horarios_disponibles").delete().eq("id", horario_id).execute().data


def obtener_horarios_disponibles(medico_id):
    return supabase.table("horarios_disponibles").select("*") \
        .eq("medico_id", medico_id) \
        .eq("activo", True).execute().data


# ================================
# PACIENTES ATENDIDOS
# ================================

def obtener_pacientes_por_medico(medico_id):
    # Busca pacientes únicos que hayan tenido turnos con este médico
    query = """
        SELECT DISTINCT p.*
        FROM turnos t
        JOIN pacientes p ON t.paciente_id = p.id
        WHERE t.medico_id = %s
    """
    # Este tipo de consulta requiere una función RPC en Supabase o SQL directo si es posible
    # Aquí simulamos con filtro múltiple si se hace en app:
    turnos = supabase.table("turnos").select("paciente_id").eq("medico_id", medico_id).execute().data
    paciente_ids = list(set([t["paciente_id"] for t in turnos]))

    pacientes = []
    for pid in paciente_ids:
        paciente = supabase.table("pacientes").select("*").eq("id", pid).single().execute().data
        pacientes.append(paciente)
    return pacientes


def obtener_historial_paciente(paciente_id):
    return supabase.table("turnos").select("*").eq("paciente_id", paciente_id).order("fecha", desc=True).execute().data

