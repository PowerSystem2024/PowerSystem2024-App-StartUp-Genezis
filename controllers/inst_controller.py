import os
from math import degrees

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


#=======================================================================================================================
def fecha_hora_actual():
    return datetime.now(timezone.utc)
    

