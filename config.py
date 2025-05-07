# Configuración de la aplicación y Supabase
import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Cargar variables de entorno
load_dotenv()

# Configuración de Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Configuración de la aplicación
APP_NAME = "Sistema de Turnos Médicos"
APP_VERSION = "1.0.0"

def get_supabase_client() -> Client:
    """Obtener cliente de Supabase"""
    return create_client(SUPABASE_URL, SUPABASE_KEY)