import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Cargar variables de entorno
load_dotenv()

# Obtener las variables de entorno
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Crear el cliente de Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Intentar obtener datos de la tabla 'usuarios'
try:
    response = supabase.table("usuarios").select("*").limit(1).execute()
    if response.data:
        print("✅ Conexión exitosa. Datos obtenidos:")
        print(response.data)
    else:
        print("✅ Conexión exitosa, pero la tabla 'usuarios' está vacía.")
except Exception as e:
    print("❌ Error al conectar o consultar la base de datos:")
    print(e)