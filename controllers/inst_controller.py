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


# En controllers.py

def buscar_medicos_para_asociar(termino_busqueda, institucion_id_actual):
    print(f"\n--- INICIANDO BÚSQUEDA (LÓGICA 'SOLO MÉDICOS') ---")

    try:
        # Paso 1: Obtener IDs de usuario que YA están en la institución actual.
        medicos_actuales = supabase.table("medicos").select("usuario_id").eq("institucion_id",
                                                                             institucion_id_actual).execute().data
        ids_a_excluir = {medico['usuario_id'] for medico in medicos_actuales if medico.get('usuario_id')}
        print(f"Paso 1 - OK: IDs a excluir: {ids_a_excluir}")

        print("Paso 2 - Buscando en la tabla 'medicos' y uniendo 'usuarios'...")
        query = supabase.table("medicos").select("*, usuarios(*)").eq("usuarios.tipo", "medico")

        if termino_busqueda:
            print(f"Aplicando filtro de email: {termino_busqueda}")
            query = query.ilike("usuarios.email", f"%{termino_busqueda}%")

        candidatos_crudos = query.execute().data
        print(f"Se encontraron {len(candidatos_crudos)} registros de médicos en total.")

        # Paso 3: Procesar y filtrar en Python para evitar duplicados.
        medicos_procesados = {}
        for medico in candidatos_crudos:
            usuario = medico.get('usuarios')
            if not usuario: continue
            # Si el médico ya está en la institución actual, lo ignoramos
            if usuario['id'] in ids_a_excluir:
                continue

            if usuario['id'] not in medicos_procesados:
                medicos_procesados[usuario['id']] = medico

        # Convertimos el diccionario de vuelta a una lista
        medicos_disponibles = list(medicos_procesados.values())

        print(f"Paso 3 - OK: Quedan {len(medicos_disponibles)} médicos únicos y disponibles.")
        print(f"--- BÚSQUEDA FINALIZADA ---\n")

        return medicos_disponibles

    except Exception as e:
        print(f"!!!!!!!!!! ERROR DURANTE LA BÚSQUEDA: {e} !!!!!!!!!!")
        return []


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
def crearTurno(paciente_id, medico_id, institucion_id, fecha, hora_inicio, hora_fin, estado, motivo_consulta=None):
    """Crea un nuevo turno"""
    data = {
        "paciente_id": paciente_id,
        "medico_id": medico_id,
        "institucion_id": institucion_id,
        "fecha": fecha,
        "hora_inicio": hora_inicio,
        "hora_fin": hora_fin,
        "estado": estado,
        "motivo_consulta": motivo_consulta,
        "creado_en": fecha_hora_actual()
    }
    return supabase.table("turnos").insert(data).execute().data

#----------------------------------------------------------------------------------------------------------------------

def obtenerTurnosConDetalles():
    """Método de respaldo con joins manuales"""
    print(f"Usando Metodo manual para obtenerTurnosConDetalles")
    try:
        turnos_data = supabase.table("turnos").select("*").execute().data
        if not turnos_data:
            return []

        # Obtener IDs únicos
        medico_ids = list({t["medico_id"] for t in turnos_data if t.get("medico_id")})
        paciente_ids = list({t["paciente_id"] for t in turnos_data if t.get("paciente_id")})
        institucion_ids = list({t["institucion_id"] for t in turnos_data if t.get("institucion_id")})

        # Obtener datos de médicos
        medicos_detalles = {}
        if medico_ids:
            medicos_results = supabase.table("medicos").select(
                "*, usuarios(nombre, apellido)"
            ).in_("id", medico_ids).execute().data
            medicos_detalles = {m["id"]: m for m in medicos_results if m and "id" in m}

        # Obtener datos de pacientes
        pacientes_detalles = {}
        if paciente_ids:
            pacientes_results = supabase.table("pacientes").select(
                "*, usuarios(nombre, apellido)"
            ).in_("id", paciente_ids).execute().data
            pacientes_detalles = {p["id"]: p for p in pacientes_results if p and "id" in p}

        # Obtener datos de instituciones
        instituciones_detalles = {}
        if institucion_ids:
            instituciones_results = supabase.table("instituciones").select(
                "id, nombre, direccion"
            ).in_("id", institucion_ids).execute().data
            instituciones_detalles = {i["id"]: i for i in instituciones_results if i and "id" in i}

        # Agregar datos relacionados a cada turno
        for turno in turnos_data:
            turno["medicos"] = medicos_detalles.get(turno.get("medico_id"))
            turno["pacientes"] = pacientes_detalles.get(turno.get("paciente_id"))
            turno["instituciones"] = instituciones_detalles.get(turno.get("institucion_id"))

        return turnos_data

    except Exception as e:
        print(f"Error en obtenerTurnosConDetalles_manual: {e}")
        return []


def actualizarTurno(turno_id, datos_actualizados):
    """Actualiza un turno existente"""
    datos_actualizados["actualizado_en"] = fecha_hora_actual()
    return supabase.table("turnos").update(datos_actualizados).eq("id", turno_id).execute().data


def eliminarTurno(turno_id):
    """Elimina un turno"""
    return supabase.table("turnos").delete().eq("id", turno_id).execute().data

def obtenerTurnosPorMedico(medico_id):
    """Obtiene turnos pendientes de un médico específico"""
    return supabase.table("turnos").select("*").eq("medico_id", medico_id).neq("estado", "cancelado").execute().data

def eliminarTurnosPorMedico(medico_id):
    """Elimina todos los turnos de un médico específico"""
    return supabase.table("turnos").delete().eq("medico_id", medico_id).execute().data

#=======================================================================================================================
def fecha_hora_actual():
    return datetime.now(timezone.utc).isoformat()


