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

def obtenerMedicosConUsuarios():
    """Obtiene médicos con información del usuario (nombre y apellido)"""
    return supabase.table("medicos").select("""*,usuarios!medicos_usuario_id_fkey(nombre, apellido)""").execute().data

def actualizarMedico(medico_id, dato_actualizado):
    dato_actualizado["actualizado_en"] = fecha_hora_actual()
    return supabase.table("medicos").update(dato_actualizado).eq("id", medico_id).execute().data


def eliminarMedico(medico_id):
    return supabase.table("medicos").delete().eq("id", medico_id).execute().data


#==========================================
# CRUD Horarios Disponibles
#==========================================
def crearHorario(medico_id, dia_semana, hora_inicio, hora_fin, fecha_turno, activo=True):
    data = {
        "medico_id": medico_id,
        "dia_semana": dia_semana,
        "hora_inicio": hora_inicio,
        "hora_fin": hora_fin,
        "activo": activo,
        "fecha_turno": fecha_turno,
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

# ==========================================
# CRUD Turnos
# ==========================================
def crearTurno(paciente_id, medico_id, institucion_id, fecha, hora_inicio, hora_fin, estado, motivo_consulta=None, notas=None):
    data = {
        "paciente_id": paciente_id,
        "medico_id": medico_id,
        "institucion_id": institucion_id,
        "fecha": fecha,
        "hora_inicio": hora_inicio,
        "hora_fin": hora_fin,
        "estado": estado,
        "motivo_consulta": motivo_consulta,
        "notas": notas,
        "creado_en": fecha_hora_actual()
    }
    return supabase.table("turnos").insert(data).execute().data

def obtenerTurnos():
    return supabase.table("turnos").select("*").execute().data

def obtenerTurnosPorPaciente(paciente_id):
    """Obtiene todos los turnos de un paciente específico."""
    return supabase.table("turnos").select("*").eq("paciente_id", paciente_id).execute().data

def obtenerTurnosPorMedico(medico_id):
    """Obtiene todos los turnos de un médico específico."""
    return supabase.table("turnos").select("*").eq("medico_id", medico_id).execute().data


def obtenerTurnosConDetalles():
    """
    Obtiene todos los turnos con información detallada del paciente, médico e institución.
    Si los joins automáticos de Supabase fallan, realiza las uniones manualmente.
    """
    turnos_data = supabase.table("turnos").select("*").execute().data

    if not turnos_data:
        return []

    # Obtener todos los IDs de médicos, pacientes e instituciones
    medico_ids = list(set([t.get("medico_id") for t in turnos_data if t.get("medico_id")]))
    paciente_ids = list(set([t.get("paciente_id") for t in turnos_data if t.get("paciente_id")]))
    institucion_ids = list(set([t.get("institucion_id") for t in turnos_data if t.get("institucion_id")]))

    # Obtener datos de médicos y sus usuarios
    medicos_detalles = {}
    if medico_ids:
        medicos_results = supabase.table("medicos").select("*, usuarios(nombre, apellido)").in_("id",
                                                                                                medico_ids).execute().data
        for m in medicos_results:
            # *** VERIFICACIÓN Y DEPURAICÓN AÑADIDA AQUÍ ***
            if m and "id" in m:  # Asegura que m no es None y tiene la clave 'id'
                medicos_detalles[m["id"]] = m
            else:
                print(f"DEBUG ERROR: Objeto médico sin 'id' encontrado o nulo: {m}")

    # Obtener datos de pacientes y sus usuarios
    pacientes_detalles = {}
    if paciente_ids:
        pacientes_results = supabase.table("pacientes").select("*, usuarios(nombre, apellido)").in_("id",
                                                                                                    paciente_ids).execute().data
        for p in pacientes_results:
            # *** VERIFICACIÓN Y DEPURAICÓN AÑADIDA AQUÍ ***
            if p and "id" in p:  # Asegura que p no es None y tiene la clave 'id'
                pacientes_detalles[p["id"]] = p
            else:
                print(f"DEBUG ERROR: Objeto paciente sin 'id' encontrado o nulo: {p}")

    # Obtener datos de instituciones
    instituciones_detalles = {}
    if institucion_ids:
        instituciones_results = supabase.table("instituciones").select("id, nombre, direccion, telefono, email").in_(
            "id", institucion_ids).execute().data
        for i in instituciones_results:
            # *** VERIFICACIÓN Y DEPURAICÓN AÑADIDA AQUÍ ***
            if i and "id" in i:  # Asegura que i no es None y tiene la clave 'id'
                instituciones_detalles[i["id"]] = i
            else:
                print(f"DEBUG ERROR: Objeto institución sin 'id' encontrado o nulo: {i}")

    # Unir los datos
    for turno in turnos_data:
        turno["medicos"] = medicos_detalles.get(turno.get("medico_id"))
        turno["pacientes"] = pacientes_detalles.get(turno.get("paciente_id"))
        turno["instituciones"] = instituciones_detalles.get(turno.get("institucion_id"))

    return turnos_data

#=======================================================================================================================
def fecha_hora_actual():
    return datetime.now(timezone.utc).isoformat()


