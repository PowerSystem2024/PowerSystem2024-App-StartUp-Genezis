from datetime import datetime, timezone

def fecha_hora_actual_utc():
    """Devuelve la fecha y hora actual en formato ISO 8601 con zona horaria UTC."""
    return datetime.now(timezone.utc).isoformat()
