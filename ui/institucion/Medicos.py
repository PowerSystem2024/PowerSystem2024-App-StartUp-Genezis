import os
from dotenv import load_dotenv
from supabase import create_client
from datetime import datetime, timezone

# Cargar variables de entorno
load_dotenv()

SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

#==========================================
# Función de utilidad
#==========================================

def fecha_hora_actual():
    return datetime.now(timezone.utc)

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
