from database.db_manager import DatabaseManager
import hashlib

class AuthController:
    """Controlador de autenticación"""
    
    def __init__(self):
        self.db = DatabaseManager()
    
    def _hash_password(self, password: str) -> str:
        """Hashear contraseña para almacenamiento seguro"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def login(self, email: str, password: str):
        """Iniciar sesión de usuario"""
        hashed_password = self._hash_password(password)
        
        # Buscar usuario por email y password
        result = self.db.get_table("usuarios").select("*").eq("email", email).eq("password", hashed_password).execute()
        
        if len(result.data) == 0:
            return None
        
        return result.data[0]
    
    def register(self, user_data: dict):
        """Registrar un nuevo usuario"""
        # Hashear contraseña
        user_data["password"] = self._hash_password(user_data["password"])
        
        # Insertar usuario
        result = self.db.insert("usuarios", user_data)
        
        return result.data[0] if result.data else None