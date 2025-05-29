
from config import supabase, fecha_hora_actual

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
