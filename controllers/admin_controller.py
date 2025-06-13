import os
from dotenv import load_dotenv
from supabase import create_client
from utils.date_utils import fecha_hora_actual_utc

# Cargar variables de entorno
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


class AdminController:
    def __init__(self):
        self.supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


# ====================================
# HELPERS EFICIENTES (la clave de la optimización)
# ====================================

def _obtener_id_asociado(tabla, usuario_id):
    """
    Helper privado y eficiente para obtener el ID de una tabla relacionada
    (medicos, pacientes, etc.) a partir de un usuario_id.
    """
    # Esta es la forma CORRECTA: le pedimos el dato específico a la base de datos.
    resultado = supabase.table(tabla).select("id").eq("usuario_id", usuario_id).limit(1).execute().data
    if resultado:
        return resultado[0]['id']
    return None


# ====================================
# GESTIÓN DE USUARIOS
# ====================================

def crear_usuario(email, password, tipo, nombre, apellido):
    """Crea un nuevo usuario en la tabla 'usuarios'."""
    # IMPORTANTE: La contraseña debe ser hasheada antes de guardarse en producción.
    data = {
        "email": email,
        "password": password,
        "tipo": tipo,
        "nombre": nombre,
        "apellido": apellido,
    }
    return supabase.table("usuarios").insert(data).execute().data


def obtener_usuarios():
    """Obtiene todos los usuarios."""
    return supabase.table("usuarios").select("*").execute().data


def actualizar_usuario(usuario_id, nuevos_datos):
    """Actualiza los datos de un usuario específico."""
    nuevos_datos["actualizado_en"] = fecha_hora_actual_utc()
    return supabase.table("usuarios").update(nuevos_datos).eq("id", usuario_id).execute().data


def borrar_usuario(usuario_id):
    """
    Borra un usuario. ¡CUIDADO! Esto puede requerir borrados en cascada
    o manejo de registros huérfanos (médicos, pacientes, etc.).
    """
    return supabase.table("usuarios").delete().eq("id", usuario_id).execute().data


# Métodos de la clase AdminController
default_admin_methods = {
    'crear_usuario': crear_usuario,
    'obtener_usuarios': obtener_usuarios,
    'actualizar_usuario': actualizar_usuario,
    'borrar_usuario': borrar_usuario,
}

# Agregar métodos a la clase AdminController
for method_name, method in default_admin_methods.items():
    setattr(AdminController, method_name, staticmethod(method))


# ====================================
# GESTIÓN DE INSTITUCIONES
# ====================================

def crear_institucion(usuario_id, nombre, direccion, telefono, email, descripcion, horario_apertura, horario_cierre,
                      logo_url):
    """Crea una nueva institución."""
    data = {
        "usuario_id": usuario_id,
        "nombre": nombre,
        "direccion": direccion,
        "telefono": telefono,
        "email": email,
        "descripcion": descripcion,
        "horario_apertura": horario_apertura,
        "horario_cierre": horario_cierre,
        "logo_url": logo_url
    }
    return supabase.table("instituciones").insert(data).execute().data


def obtener_instituciones():
    """Obtiene todas las instituciones."""
    return supabase.table("instituciones").select("*").execute().data


def actualizar_institucion(institucion_id, nuevos_datos):
    """Actualiza los datos de una institución."""
    nuevos_datos["actualizado_en"] = fecha_hora_actual_utc()
    return supabase.table("instituciones").update(nuevos_datos).eq("id", institucion_id).execute().data


# ====================================
# REPORTES Y ESTADÍSTICAS (Ahora optimizados)
# ====================================

def obtener_estadisticas_sistema():
    """
    Obtiene estadísticas del sistema contando por el campo 'tipo' en la tabla 'usuarios',
    asegurando que los datos sean consistentes y correctos.
    """
    try:
        # Contamos cada tipo de usuario directamente desde la tabla 'usuarios'.
        # Esta es la fuente de verdad única y correcta.
        medicos_count = supabase.table("usuarios").select("id", count='exact').eq("tipo", "medico").execute().count
        pacientes_count = supabase.table("usuarios").select("id", count='exact').eq("tipo", "paciente").execute().count
        instituciones_count = supabase.table("usuarios").select("id", count='exact').eq("tipo", "institucion").execute().count
        admins_count = supabase.table("usuarios").select("id", count='exact').eq("tipo", "admin").execute().count

        # El total de usuarios se puede obtener sumando los parciales o con una consulta general.
        # Sumar es más rápido si ya tenemos los conteos.
        usuarios_totales = medicos_count + pacientes_count + instituciones_count + admins_count

        # El conteo de turnos sigue siendo sobre su propia tabla.
        turnos_count = supabase.table("turnos").select("id", count='exact').execute().count

        return {
            "usuarios_totales": usuarios_totales,
            "medicos_totales": medicos_count,
            "pacientes_totales": pacientes_count,
            "instituciones_totales": instituciones_count,
            "admins_totales": admins_count,
            "turnos_totales": turnos_count
        }
    except Exception as e:
        print(f"Error al obtener estadísticas: {e}")
        return {
            "usuarios_totales": 0, "medicos_totales": 0, "pacientes_totales": 0,
            "instituciones_totales": 0, "admins_totales": 0, "turnos_totales": 0
        }


# ====================================
# OBTENCIÓN DE INFORMACIÓN (Ahora optimizados con Joins)
# ====================================

def obtener_info_completa_medico(usuario_id):
    """
    Obtiene información completa y formateada de un médico de forma eficiente,
    usando un JOIN para traer los datos de la institución en una sola consulta.
    """
    # Hacemos una única consulta pidiendo los datos del médico
    # y, a la vez, los datos de la institución relacionada (*:instituciones(*)).
    query = "*, institucion:instituciones(nombre)"
    resultado = supabase.table("medicos").select(query).eq("usuario_id", usuario_id).limit(1).execute().data

    if not resultado:
        return None

    medico_data = resultado[0]
    institucion_data = medico_data.get("institucion")

    # Obtenemos los horarios de este médico de forma eficiente
    medico_id = medico_data.get("id")
    horarios_raw = supabase.table("horarios_disponibles").select("*").eq("medico_id", medico_id).eq("activo",
                                                                                                    True).execute().data

    # Mapeo de días de la semana
    dias_semana = {0: "Lunes", 1: "Martes", 2: "Miércoles", 3: "Jueves", 4: "Viernes", 5: "Sábado", 6: "Domingo"}
    horarios_formateados = [
        f"{dias_semana.get(h.get('dia_semana'), 'Día no válido')}: {h.get('hora_inicio')} - {h.get('hora_fin')}"
        for h in horarios_raw
    ]

    info_completa = {
        "especialidad": medico_data.get("especialidad", "N/A"),
        "matricula": medico_data.get("matricula", "N/A"),
        "duracion_turno": f"{medico_data.get('duracion_turno', 30)} minutos",
        "institucion": institucion_data.get("nombre", "Sin institución") if institucion_data else "Sin institución",
        "horarios": horarios_formateados
    }
    return info_completa


def obtener_info_paciente(usuario_id):
    """Obtiene el perfil de un paciente a partir de su usuario_id."""
    return supabase.table("pacientes").select("*").eq("usuario_id", usuario_id).limit(1).execute().data


def obtener_info_institucion(usuario_id):
    """Obtiene el perfil de una institución a partir de su usuario_id."""
    return supabase.table("instituciones").select("*").eq("usuario_id", usuario_id).limit(1).execute().data


# Añadir métodos de información a la clase AdminController
info_methods = {
    'obtener_info_completa_medico': obtener_info_completa_medico,
    'obtener_info_paciente': obtener_info_paciente,
    'obtener_info_institucion': obtener_info_institucion,
    'obtener_estadisticas_sistema': obtener_estadisticas_sistema
}

# Agregar métodos a la clase AdminController
for method_name, method in info_methods.items():
    setattr(AdminController, method_name, staticmethod(method))