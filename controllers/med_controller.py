import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

# Horarios

def obtener_horarios_disponibles(medico_id):
    return supabase.table("horarios_disponibles").select("*").eq("medico_id", medico_id).execute().data

def agregar_horario_disponible(medico_id, fecha, inicio, fin):
    return supabase.table("horarios_disponibles").insert({
        "medico_id": medico_id,
        "fecha_horario": fecha,
        "hora_inicio": inicio,
        "hora_fin": fin
    }).execute().data

def eliminar_horario_disponible(horario_id):
    return supabase.table("horarios_disponibles").delete().eq("id", horario_id).execute().data

# Agenda

def obtener_turnos_del_dia(medico_id, fecha):
    return supabase.table("turnos").select("*").eq("medico_id", medico_id).eq("fecha", fecha).execute().data

def completar_turno(turno_id, notas):
    return supabase.table("turnos").update({"estado": "completado", "notas": notas}).eq("id", turno_id).execute().data

def cancelar_turno(turno_id):
    return supabase.table("turnos").update({"estado": "cancelado"}).eq("id", turno_id).execute().data

# Pacientes

def obtener_pacientes_por_medico(medico_id):
    return supabase.rpc("obtener_pacientes_por_medico", {"mid": medico_id}).execute().data

def obtener_historial_paciente(paciente_id):
    return supabase.table("turnos").select("*").eq("paciente_id", paciente_id).order("fecha", desc=True).execute().data

def obtener_medico_id_por_usuario_id(usuario_id):
    resultado = supabase.table("medicos").select("id").eq("usuario_id", usuario_id).execute().data
    return resultado[0]["id"] if resultado else None

def obtener_pacientes_por_medico(medico_id):
    turnos = supabase.table("turnos").select("paciente_id").eq("medico_id", medico_id).execute().data
    ids_pacientes = list(set(t["paciente_id"] for t in turnos))

    pacientes = []
    for pid in ids_pacientes:
        # Modificado para incluir num_afiliado en la consulta
        p = supabase.table("pacientes").select("id, usuario_id, obra_social, num_afiliado").eq("id", pid).execute().data
        if p:
            u = supabase.table("usuarios").select("nombre, apellido").eq("id", p[0]["usuario_id"]).execute().data
            # Obtener el último estado del paciente
            ultimo_turno = supabase.table("turnos").select("estado").eq("paciente_id", pid).order("fecha",
                                                                                                  desc=True).limit(
                1).execute().data
            estado = ultimo_turno[0]["estado"] if ultimo_turno else "-"

            if u:
                pacientes.append({
                    "id": p[0]["id"],
                    "nombre": u[0]["nombre"],
                    "apellido": u[0]["apellido"],
                    "obra_social": p[0]["obra_social"],
                    "numero_afiliado": p[0].get("num_afiliado", "-"),
                    "estado": estado
                })
    return pacientes


