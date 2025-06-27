import os
import secrets
from dotenv import load_dotenv
from supabase import create_client
from utils.date_utils import fecha_hora_actual_utc
from utils.security_utils import hash_password
from datetime import datetime
from postgrest.exceptions import APIError

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
    """
    Borra un usuario y sus registros asociados.
    """
    try:
        # Primero, obtener el tipo de usuario para manejar eliminaciones en cascada
        user_data_response = supabase.table("usuarios").select("tipo").eq("id", usuario_id).single().execute()
        user_type = user_data_response.data.get("tipo") if user_data_response.data else None

        # Borra registros dependientes primero
        if user_type == "paciente":
            supabase.table("pacientes").delete().eq("usuario_id", usuario_id).execute()
        elif user_type == "medico":
            supabase.table("medicos").delete().eq("usuario_id", usuario_id).execute()
        elif user_type == "institucion":
            supabase.table("instituciones").delete().eq("usuario_id", usuario_id).execute()

        # Finalmente, eliminar el registro del usuario
        final_delete_response = supabase.table("usuarios").delete().eq("id", usuario_id).execute()
        return final_delete_response.data

    except APIError as e:
        # Si el error es "no se encontró una fila", puede que el sub-registro no existiera.
        # No es un error fatal para la operación de borrado.
        if e.code == 'PGRST116':
            print(
                f"Advertencia: No se encontró un sub-registro ({user_type}) para el usuario {usuario_id} durante el borrado. Continuando...")
        else:
            print(f"Error de Supabase en borrar_usuario: {e}")
            raise e  # Propagar otros errores de API
    except Exception as e:
        print(f"Error general en borrar_usuario: {e}")
        raise e


def admin_actualizar_password_usuario(usuario_id, nueva_password):
    """Permite a un admin actualizar la contraseña de un usuario."""
    if not nueva_password:
        raise ValueError("La nueva contraseña no puede estar vacía.")
    hashed_password = hash_password(nueva_password)
    datos_actualizados = {"password": hashed_password, "actualizado_en": fecha_hora_actual_utc()}
    return supabase.table("usuarios").update(datos_actualizados).eq("id", usuario_id).execute().data


# ====================================
# SECCIÓN: GESTIÓN DE INSTITUCIONES
# ====================================
def crear_institucion(usuario_id, nombre, direccion, email, telefono=None, descripcion=None,
                      horario_apertura=None, horario_cierre=None, logo_url=None):
    """Crea una nueva institución. Acepta None para campos opcionales."""
    data = {
        "usuario_id": usuario_id, "nombre": nombre, "direccion": direccion, "email": email,
        "telefono": telefono, "descripcion": descripcion, "horario_apertura": horario_apertura,
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


def registrar_nueva_institucion(nombre, password, direccion, email, telefono=None, descripcion=None,
                                horario_apertura=None, horario_cierre=None, logo_url=None):
    """
    Orquesta la creación de una institución, asegurando la atomicidad de la operación.
    Si la creación de la institución falla, se elimina el usuario creado previamente.
    """
    nuevo_usuario_id = None
    try:
        # Paso 1: Crear el usuario base
        usuario_data = crear_usuario(
            email=email, password=password, tipo='institucion',
            nombre=nombre, apellido='Institución'
        )
        if not usuario_data or not usuario_data[0].get('id'):
            raise Exception("Falló la creación del registro de usuario base.")

        nuevo_usuario_id = usuario_data[0]['id']

        # Paso 2: Crear la institución asociada
        institucion_creada = crear_institucion(
            usuario_id=nuevo_usuario_id, nombre=nombre, direccion=direccion, email=email,
            telefono=telefono, descripcion=descripcion, horario_apertura=horario_apertura,
            horario_cierre=horario_cierre, logo_url=logo_url
        )

        if not institucion_creada:
            # Este 'raise' será capturado por el 'except' de abajo
            raise Exception("La API de Supabase no devolvió datos para la institución, aunque no lanzó un error.")

        return institucion_creada

    except Exception as e:
        print(f"Error en el proceso de registro de institución: {e}")
        # Paso 3: Limpieza. Si el usuario fue creado pero la institución falló, borrar el usuario.
        if nuevo_usuario_id:
            print(f"Intentando revertir la creación del usuario con ID: {nuevo_usuario_id}")
            try:
                borrar_usuario(nuevo_usuario_id)
                print("Reversión exitosa: el usuario huérfano fue eliminado.")
            except Exception as clean_e:
                # Este es un caso grave que requiere logging o monitoreo.
                print(
                    f"¡ERROR CRÍTICO! No se pudo revertir la creación del usuario {nuevo_usuario_id}. Error de limpieza: {clean_e}")

        # Propagamos la excepción original para que la UI pueda manejarla y mostrar un mensaje.
        raise e


# ====================================
# SECCIÓN: GESTIÓN DE PACIENTES
# ====================================
def crear_paciente(usuario_id, fecha_nacimiento, genero, telefono, obra_social, num_afiliado):
    """Crea un nuevo paciente."""
    data = {
        "usuario_id": usuario_id, "fecha_nacimiento": fecha_nacimiento, "genero": genero,
        "telefono": telefono, "obra_social": obra_social, "num_afiliado": num_afiliado,
    }
    return supabase.table("pacientes").insert(data).execute().data


def actualizar_paciente(paciente_id, nuevos_datos):
    """Actualiza los datos de un paciente."""
    nuevos_datos["actualizado_en"] = fecha_hora_actual_utc()
    return supabase.table("pacientes").update(nuevos_datos).eq("id", paciente_id).execute().data


def registrar_nuevo_paciente(nombre, apellido, email, password, fecha_nacimiento="", genero="", telefono="",
                             obra_social="", num_afiliado=""):
    """Orquesta la creación completa de un paciente."""
    try:
        usuario_data = crear_usuario(email=email, password=password, tipo='paciente', nombre=nombre, apellido=apellido)
        if not usuario_data:
            raise Exception("No se pudo crear el registro de usuario para el paciente.")

        nuevo_usuario_id = usuario_data[0]['id']
        paciente_creado = crear_paciente(
            usuario_id=nuevo_usuario_id, fecha_nacimiento=fecha_nacimiento, genero=genero,
            telefono=telefono, obra_social=obra_social, num_afiliado=num_afiliado,
        )
        if not paciente_creado:
            raise Exception("El usuario fue creado, pero el paciente no pudo registrarse.")
        return paciente_creado
    except Exception as e:
        print(f"Error en el proceso de registro de paciente: {e}")
        raise e


# ====================================
# SECCIÓN: GESTIÓN DE MEDICOS
# ====================================
def crear_medico(usuario_id, especialidad, matricula, institucion_id=None, duracion_turno=None):
    """Crea un nuevo médico."""
    data = {
        "usuario_id": usuario_id, "especialidad": especialidad, "matricula": matricula,
        "institucion_id": institucion_id, "duracion_turno": duracion_turno,
    }
    return supabase.table("medicos").insert(data).execute().data


def obtener_medico_id_por_usuario_id(usuario_id: str) -> str | None:
    """Busca en la tabla 'medicos' y devuelve el ID del médico (PK) basado en el ID del usuario (FK)."""
    if not usuario_id:
        return None
    try:
        response = supabase.table("medicos").select("id").eq("usuario_id", usuario_id).single().execute()
        return response.data.get('id') if response.data else None
    except Exception as e:
        print(f"Error al buscar médico por usuario_id ({usuario_id}): {e}")
        return None


def obtener_medicos():
    """Obtiene todos los médicos."""
    return supabase.table("medicos").select(
        "*, usuario:usuarios(nombre, apellido, email), institucion:instituciones(nombre)").execute().data


def actualizar_medico(medico_id, nuevos_datos):
    """Actualiza los datos de un médico."""
    nuevos_datos["actualizado_en"] = fecha_hora_actual_utc()
    return supabase.table("medicos").update(nuevos_datos).eq("id", medico_id).execute().data


def registrar_nuevo_medico(nombre, apellido, email, password, especialidad, matricula, institucion_id=None,
                           duracion_turno=None):
    """Orquesta la creación completa de un médico."""
    try:
        usuario_data = crear_usuario(email=email, password=password, tipo='medico', nombre=nombre, apellido=apellido)
        if not usuario_data:
            raise Exception("No se pudo crear el registro de usuario para el médico.")
        nuevo_usuario_id = usuario_data[0]['id']
        medico_creado = crear_medico(
            usuario_id=nuevo_usuario_id, especialidad=especialidad, matricula=matricula,
            institucion_id=institucion_id, duracion_turno=duracion_turno
        )
        if not medico_creado:
            raise Exception("El usuario fue creado, pero el médico no pudo registrarse.")
        return medico_creado
    except Exception as e:
        print(f"Error en el proceso de registro de médico: {e}")
        raise e


# ====================================
# SECCIÓN: OBTENCIÓN DE INFORMACIÓN DETALLADA
# ====================================
def obtener_info_completa_medico(usuario_id):
    """Obtiene información completa y formateada de un médico."""
    return supabase.table("medicos").select("*, institucion:instituciones(nombre)").eq("usuario_id", usuario_id).limit(
        1).execute().data


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
all_methods = {
    'crear_usuario': crear_usuario,
    'obtener_usuarios': obtener_usuarios,
    'actualizar_usuario': actualizar_usuario,
    'borrar_usuario': borrar_usuario,
    'admin_actualizar_password_usuario': admin_actualizar_password_usuario,
    'crear_institucion': crear_institucion,
    'obtener_instituciones': obtener_instituciones,
    'actualizar_institucion': actualizar_institucion,
    'registrar_nueva_institucion': registrar_nueva_institucion,
    'crear_paciente': crear_paciente,
    'actualizar_paciente': actualizar_paciente,
    'registrar_nuevo_paciente': registrar_nuevo_paciente,
    'crear_medico': crear_medico,
    'obtener_medico_id_por_usuario_id': obtener_medico_id_por_usuario_id,
    'obtener_medicos': obtener_medicos,
    'actualizar_medico': actualizar_medico,
    'registrar_nuevo_medico': registrar_nuevo_medico,
    'obtener_info_completa_medico': obtener_info_completa_medico,
    'obtener_info_paciente': obtener_info_paciente,
    'obtener_info_institucion': obtener_info_institucion,
    'obtener_estadisticas_sistema': obtener_estadisticas_sistema,
}

for method_name, method_func in all_methods.items():
    setattr(AdminController, method_name, staticmethod(method_func))