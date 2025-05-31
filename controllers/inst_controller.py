import os
from dotenv import load_dotenv
from supabase import create_client
from datetime import datetime,timezone

load_dotenv()

SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")
supabase = create_client(SUPABASE_URL,SUPABASE_KEY)

#==========================================
# CRUD Institucion
#==========================================

def crearInstitucion(usuario_id,nombre,direccion,telefono,email,descripcion,horario_apertura,horario_cierre,logo_url):
    data ={
        "usuario_id": usuario_id,
        "nombre": nombre,
        "direccion": direccion,
        "telefono": telefono,
        "email": email,
        "descripcion": descripcion,
        "horario_apertura": horario_apertura,
        "horario_cierre": horario_cierre,
        "creado_en": fecha_hora_actual(),
        "logo_url":logo_url
    }
    return supabase.table("instituciones").insert(data).execute().data


def obtenerInstitucion():
    return supabase.table("instituciones").select("*").execute().data


def ActualizarInstitucion(instituciones_id,dato_actualizado):
    dato_actualizado["actualizado_en"] = fecha_hora_actual()
    return supabase.table("instituciones").update(dato_actualizado).eq("id",instituciones_id).execute().data


#==========================================
# CRUD Médicos
#==========================================

def crearMedico(usuario_id, institucion_id, especialidad, matricula, duracion_turno):
    data = {
        "usuario_id": usuario_id,
        "institucion_id": institucion_id,
        "especialidad": especialidad,
        "matricula": matricula,
        "duracion_turno": duracion_turno,
        "creado_en": fecha_hora_actual()
    }
    return supabase.table("medicos").insert(data).execute().data


def obtenerMedicos():
    return supabase.table("medicos").select("*").execute().data


def actualizarMedico(medico_id, dato_actualizado):
    dato_actualizado["actualizado_en"] = fecha_hora_actual()
    return supabase.table("medicos").update(dato_actualizado).eq("id", medico_id).execute().data


def eliminarMedico(medico_id):
    return supabase.table("medicos").delete().eq("id", medico_id).execute().data


#==========================================
# CRUD Horarios Disponibles
#==========================================

def crearHorario(medico_id, dia_semana, hora_inicio, hora_fin, activo=True):
    data = {
        "medico_id": medico_id,
        "dia_semana": dia_semana,
        "hora_inicio": hora_inicio,
        "hora_fin": hora_fin,
        "activo": activo,
        "creado_en": fecha_hora_actual()
    }
    return supabase.table("horarios_disponibles").insert(data).execute().data


def obtenerHorarios():
    return supabase.table("horarios_disponibles").select("*").execute().data


def obtenerHorariosPorMedico(medico_id):
    return supabase.table("horarios_disponibles").select("*").eq("medico_id", medico_id).execute().data


def actualizarHorario(horario_id, datos_actualizados):
    datos_actualizados["actualizado_en"] = fecha_hora_actual()
    return supabase.table("horarios_disponibles").update(datos_actualizados).eq("id", horario_id).execute().data


def eliminarHorario(horario_id):
    return supabase.table("horarios_disponibles").delete().eq("id", horario_id).execute().data


#=======================================================================================================================
def fecha_hora_actual():
    return datetime.now(timezone.utc).isoformat()
    

