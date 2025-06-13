# Archivo: auth_controller.py (o donde lo tengas)
# VERSIÓN FINAL CON LÓGICA DE MIGRACIÓN

import hashlib
from database.db_manager import DatabaseManager
from utils.security_utils import hash_password, verify_password


class AuthController:
    """Controlador de autenticación con migración de contraseñas."""

    def __init__(self):
        self.db_table = DatabaseManager().get_table("usuarios")

    def _update_password_hash(self, user_id, plain_password):
        """Función auxiliar para actualizar el hash a bcrypt."""
        new_hashed_password = hash_password(plain_password)
        self.db_table.update({"password": new_hashed_password}).eq("id", user_id).execute()
        print(f"Contraseña del usuario {user_id} migrada exitosamente a bcrypt.")

    def login(self, email: str, password: str):
        """
        Inicia sesión de usuario de forma segura con migración automática
        de hashes antiguos (sha256) a bcrypt.
        """
        # Paso 1: Buscar al usuario solo por su email.
        result = self.db_table.select("*").eq("email", email).limit(1).execute()

        if not result.data:
            return None  # Usuario no encontrado

        user = result.data[0]
        hashed_password_from_db = user.get("password")

        # Paso 2: Intentar verificar con el método nuevo y seguro (bcrypt).
        try:
            if verify_password(password, hashed_password_from_db):
                # Si tiene éxito, es una cuenta moderna. Login normal.
                return user
        except ValueError:
            # Un ValueError aquí es una señal fuerte de que el hash no es de bcrypt.
            # Procedemos a verificar con el método antiguo como plan B.
            pass

        # --- LÓGICA DE MIGRACIÓN (PLAN B) ---
        # Verificar con el método antiguo (sha256).
        old_hashed_password = hashlib.sha256(password.encode()).hexdigest()

        if old_hashed_password == hashed_password_from_db:
            # ¡Éxito! La contraseña es correcta según el método antiguo.
            # Es nuestra oportunidad para migrar el hash.
            try:
                self._update_password_hash(user["id"], password)
            except Exception as e:
                # Si la actualización falla, al menos dejamos que el usuario entre.
                # Es importante registrar este error para investigarlo.
                print(f"¡ALERTA DE SEGURIDAD! No se pudo migrar la contraseña del usuario {user['id']}. Error: {e}")

            # Devolvemos los datos del usuario para completar el login.
            return user

        # Si ninguna de las verificaciones funcionó, la contraseña es incorrecta.
        return None

    def register(self, user_data: dict):
        """Registra un nuevo usuario, siempre usando el método seguro bcrypt."""
        plain_password = user_data["password"]
        hashed_password = hash_password(plain_password)
        user_data["password"] = hashed_password
        result = self.db_table.insert(user_data).execute()
        return result.data[0] if result.data else None