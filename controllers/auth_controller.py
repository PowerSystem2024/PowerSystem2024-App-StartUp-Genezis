# Archivo: controllers/auth_controller.py

import hashlib
from database.db_manager import DatabaseManager
from utils.security_utils import hash_password, verify_password  # Asegúrate de que verify_password esté aquí


class AuthController:
    """Controlador para la autenticación y gestión de usuarios/pacientes."""

    def __init__(self):
        db = DatabaseManager()
        self.user_table = db.get_table("usuarios")
        self.patient_table = db.get_table("pacientes")

    def login(self, email: str, password: str):
        """
        Verifica las credenciales de un usuario.
        """
        # 1. Busca un usuario con el email proporcionado.
        result = self.user_table.select("*").eq("email", email).limit(1).execute()

        # 2. Si se encontró un usuario, ahora verifica la contraseña.
        if result.data:
            user = result.data[0]
            stored_password_hash = user['password']  # Obtiene el hash de la contraseña desde la BD

            # 3. Compara la contraseña del formulario con el hash almacenado.  <--- CAMBIO CLAVE AQUÍ
            if verify_password(password, stored_password_hash):
                # Si la contraseña es correcta, devuelve los datos del usuario.

                # Opcional: Si todavía tienes contraseñas en MD5, puedes migrarlas aquí.
                # Esta lógica detecta si el hash no es de bcrypt y lo actualiza.
                if stored_password_hash.startswith("$2b$") is False:
                    print(f"Migrando contraseña para el usuario: {user['id']}")
                    self._update_password_hash(user['id'], password)

                return user

        # 4. Si el email no se encontró O la contraseña no coincidió, devuelve None.
        return None

    def _update_password_hash(self, user_id, plain_password):
        """Actualiza el hash de la contraseña de un usuario a bcrypt."""
        new_hashed_password = hash_password(plain_password)
        self.user_table.update({"password": new_hashed_password}).eq("id", user_id).execute()
        print(f"Contraseña del usuario {user_id} migrada exitosamente a bcrypt.")

    # --- Tus otros métodos (register_user_and_paciente, etc.) se mantienen igual ---
    # (El resto de tu código es correcto y maneja bien el registro)

    def register_user_and_paciente(self, user_data: dict, paciente_data: dict):
        """
        Registra un nuevo usuario y su perfil de paciente asociado.
        Este método orquesta la creación en ambas tablas.
        """
        # 1. Hashear la contraseña antes de guardar
        plain_password = user_data["password"]
        hashed_password = hash_password(plain_password)
        user_data["password"] = hashed_password

        # 2. Insertar el usuario en la tabla 'usuarios'
        try:
            user_result = self.user_table.insert(user_data).execute()
            if not user_result.data:
                print("Error: No se pudo crear el registro en la tabla 'usuarios'.")
                return None
            new_user = user_result.data[0]
        except Exception as e:
            # Aquí podrías loggear el error específico de la base de datos
            print(f"Ocurrió un error al registrar el usuario: {e}")
            return None

        # 3. Si el usuario se creó, obtener su ID y crear el paciente
        usuario_id = new_user['id']

        # 4. Llamar al método para crear el paciente
        paciente_creado = self.crear_paciente(usuario_id, paciente_data)

        if not paciente_creado:
            # ¡IMPORTANTE! Si falla la creación del paciente, deberíamos idealmente
            # borrar el usuario que acabamos de crear para no dejar datos huérfanos.
            # Esto se llama "rollback" manual.
            print(f"Error al crear el paciente. Revirtiendo creación de usuario con ID: {usuario_id}")
            self.user_table.delete().eq("id", usuario_id).execute()
            return None

        # 5. Si todo salió bien, devolvemos el usuario creado.
        return new_user

    def crear_paciente(self, usuario_id: int, paciente_data: dict):
        """
        Crea un registro de paciente asociado a un usuario_id.
        Recibe un diccionario para mantener la consistencia.
        """
        # Añadimos el usuario_id al diccionario de datos del paciente
        paciente_data["usuario_id"] = usuario_id

        try:
            result = self.patient_table.insert(paciente_data).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"Ocurrió un error al crear el paciente: {e}")
            return None

    def register(self, user_data: dict):
        """Registra un nuevo usuario genérico."""
        plain_password = user_data["password"]
        hashed_password = hash_password(plain_password)
        user_data["password"] = hashed_password
        result = self.user_table.insert(user_data).execute()
        return result.data[0] if result.data else None