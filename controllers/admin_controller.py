# controllers/admin_controller.py

import os
import secrets
from dotenv import load_dotenv
from supabase import create_client
from utils.date_utils import fecha_hora_actual_utc
from utils.security_utils import hash_password

# Cargar variables de entorno
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


# ====================================
# DEFINICIÓN DE LA CLASE PRINCIPAL
# ====================================
class AdminController:
    """
    Controlador para todas las operaciones administrativas.
    Los métodos se le añaden dinámicamente al final del archivo.
    """

    def __init__(self):
        self.supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


# ====================================
# SECCIÓN: GESTIÓN DE USUARIOS
# ====================================
def crear_usuario(email, password, tipo, nombre, apellido):
    """Crea un nuevo usuario en la tabla 'usuarios'."""
    hashed_password = hash_password(password)
    data = {
        "email": email,
        "password": hashed_password,
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
    """Borra un usuario."""
    return supabase.table("usuarios").delete().eq("id", usuario_id).execute().data


# ====================================
# SECCIÓN: GESTIÓN DE INSTITUCIONES
# ====================================
def crear_institucion(usuario_id, nombre, direccion, telefono, email, descripcion, horario_apertura, horario_cierre,
                      logo_url):
    """Crea una nueva institución."""
    data = {
        "usuario_id": usuario_id, "nombre": nombre, "direccion": direccion, "telefono": telefono,
        "email": email, "descripcion": descripcion, "horario_apertura": horario_apertura,
        "horario_cierre": horario_cierre, "logo_url": logo_url
    }
    return supabase.table("instituciones").insert(data).execute().data


def obtener_instituciones():
    """Obtiene todas las instituciones."""
    return supabase.table("instituciones").select("*").execute().data


def actualizar_institucion(institucion_id, nuevos_datos):
    """Actualiza los datos de una institución."""
    nuevos_datos["actualizado_en"] = fecha_hora_actual_utc()
    return supabase.table("instituciones").update(nuevos_datos).eq("id", institucion_id).execute().data


def registrar_nueva_institucion(nombre, password, direccion, email, telefono="", descripcion="",
                                horario_apertura="09:00", horario_cierre="18:00", logo_url=""):
    """Orquesta la creación completa de una institución."""
    try:
        usuario_data = crear_usuario(
            email=email, password=password, tipo='institucion',
            nombre=nombre, apellido='Institución'
        )
        if not usuario_data:
            raise Exception("No se pudo crear el registro de usuario para la institución.")

        nuevo_usuario_id = usuario_data[0]['id']

        institucion_creada = crear_institucion(
            usuario_id=nuevo_usuario_id, nombre=nombre, direccion=direccion, telefono=telefono,
            email=email, descripcion=descripcion, horario_apertura=horario_apertura,
            horario_cierre=horario_cierre, logo_url=logo_url
        )
        if not institucion_creada:
            raise Exception("El usuario fue creado, pero la institución no pudo registrarse.")

        return institucion_creada
    except Exception as e:
        print(f"Error en el proceso de registro de institución: {e}")
        raise e


# ====================================
# SECCIÓN: OBTENCIÓN DE INFORMACIÓN DETALLADA
# ====================================
def obtener_info_completa_medico(usuario_id):
    """Obtiene información completa y formateada de un médico."""
    query = "*, institucion:instituciones(nombre)"
    resultado = supabase.table("medicos").select(query).eq("usuario_id", usuario_id).limit(1).execute().data
    # ... (lógica de formato)
    return resultado  # Simplificado para brevedad, tu lógica original está bien


def obtener_info_paciente(usuario_id):
    """Obtiene el perfil de un paciente a partir de su usuario_id."""
    return supabase.table("pacientes").select("*").eq("usuario_id", usuario_id).limit(1).execute().data


def obtener_info_institucion(usuario_id):
    """Obtiene el perfil de una institución a partir de su usuario_id."""
    return supabase.table("instituciones").select("*").eq("usuario_id", usuario_id).limit(1).execute().data


# ====================================
# SECCIÓN: REPORTES Y ESTADÍSTICAS
# ====================================
def obtener_estadisticas_sistema():
    """Obtiene estadísticas del sistema."""
    try:
        medicos_count = supabase.table("usuarios").select("id", count='exact').eq("tipo", "medico").execute().count
        pacientes_count = supabase.table("usuarios").select("id", count='exact').eq("tipo", "paciente").execute().count
        instituciones_count = supabase.table("usuarios").select("id", count='exact').eq("tipo",
                                                                                        "institucion").execute().count
        turnos_count = supabase.table("turnos").select("id", count='exact').execute().count
        return {
            "usuarios_totales": medicos_count + pacientes_count + instituciones_count,
            "medicos_totales": medicos_count,
            "pacientes_totales": pacientes_count,
            "instituciones_totales": instituciones_count,
            "turnos_totales": turnos_count
        }
    except Exception as e:
        print(f"Error al obtener estadísticas: {e}")
        return {}


# =============================================================
# === REGISTRO CENTRALIZADO DE MÉTODOS EN EL ADMINCONTROLLER ===
# =============================================================
# Aquí "pegamos" todas las funciones anteriores como métodos estáticos
# a la clase AdminController para que puedan ser llamadas desde la UI.

# Métodos de gestión de usuarios
user_methods = {
    'crear_usuario': crear_usuario,
    'obtener_usuarios': obtener_usuarios,
    'actualizar_usuario': actualizar_usuario,
    'borrar_usuario': borrar_usuario,
}

# Métodos de gestión de instituciones (ESTA ERA LA PARTE QUE FALTABA)
institution_methods = {
    'crear_institucion': crear_institucion,
    'obtener_instituciones': obtener_instituciones,
    'actualizar_institucion': actualizar_institucion,
    'registrar_nueva_institucion': registrar_nueva_institucion,
}

# Métodos para obtener información detallada
info_methods = {
    'obtener_info_completa_medico': obtener_info_completa_medico,
    'obtener_info_paciente': obtener_info_paciente,
    'obtener_info_institucion': obtener_info_institucion,
}

# Métodos de estadísticas
stats_methods = {
    'obtener_estadisticas_sistema': obtener_estadisticas_sistema,
}

# Bucle para registrar todos los métodos de todos los diccionarios
all_methods = {
    **user_methods,
    **institution_methods,
    **info_methods,
    **stats_methods
}

for method_name, method_func in all_methods.items():
    setattr(AdminController, method_name, staticmethod(method_func))