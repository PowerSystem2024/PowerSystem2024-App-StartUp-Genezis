import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")
supabase = create_client(SUPABASE_URL,SUPABASE_KEY)

#==========================================
# CRUD Institucion

def obtenerInstitucion(usuario_id,nombre,direccion,telefono,email,descripcion,horario_apertura,horario_cierre,logo_url,creado_en,actualizado_en):
    data ={
        "usuario_id": usuario_id,
        "nombre": nombre,
        "direccion": direccion,
        "telefono": telefono,
        "email": email,
        "descripcion": descripcion,
        "horario_apertura": horario_apertura,
        "horario_cierre": horario_cierre,
        "creado_en": creado_en,
        "actualizado_en": actualizado_en,
        "logo_url":logo_url
    }