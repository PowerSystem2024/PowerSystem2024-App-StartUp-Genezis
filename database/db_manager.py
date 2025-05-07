from supabase import Client
from config import get_supabase_client

class DatabaseManager:
    """Clase para manejar la conexión con Supabase"""
    
    def __init__(self):
        self.client = get_supabase_client()
    
    def get_table(self, table_name: str):
        """Obtener referencia a una tabla"""
        return self.client.table(table_name)
    
    def fetch_all(self, table_name: str, query=None):
        """Obtener todos los registros de una tabla"""
        table = self.get_table(table_name)
        if query:
            return query.execute()
        return table.select("*").execute()
    
    def fetch_by_id(self, table_name: str, id):
        """Obtener un registro por ID"""
        return self.get_table(table_name).select("*").eq("id", id).execute()
    
    def insert(self, table_name: str, data: dict):
        """Insertar un nuevo registro"""
        return self.get_table(table_name).insert(data).execute()
    
    def update(self, table_name: str, id, data: dict):
        """Actualizar un registro existente"""
        return self.get_table(table_name).update(data).eq("id", id).execute()
    
    def delete(self, table_name: str, id):
        """Eliminar un registro"""
        return self.get_table(table_name).delete().eq("id", id).execute()