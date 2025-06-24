# Archivo: utils/security_utils.py

import bcrypt

def hash_password(plain_text_password):
    """Hashea una contraseña en texto plano usando bcrypt."""
    password_bytes = plain_text_password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_bytes = bcrypt.hashpw(password_bytes, salt)
    return hashed_bytes.decode('utf-8')

def verify_password(plain_text_password, hashed_password_from_db):
    """Verifica si una contraseña en texto plano coincide con un hash de la BD."""
    try:
        plain_password_bytes = plain_text_password.encode('utf-8')
        hashed_password_bytes = hashed_password_from_db.encode('utf-8')
        return bcrypt.checkpw(plain_password_bytes, hashed_password_bytes)
    except (ValueError, TypeError):
        return False