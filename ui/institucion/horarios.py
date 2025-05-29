# institucion/horarios.py

def formatear_horarios_para_display(texto_horarios_db):
    """
    Formatea el string de horarios para una mejor visualización si es necesario.
    Por ahora, solo devuelve el texto como está si es simple.
    Si fuera un JSON o una estructura más compleja, aquí se parsearía.
    """
    if not texto_horarios_db:
        return "Horarios no especificados."
    
    # Ejemplo: si quisieras reemplazar un separador por saltos de línea
    # return texto_horarios_db.replace(";", "\n")
    
    return texto_horarios_db

def validar_formato_horarios(texto_horarios_ingresado):
    """
    Valida si el texto ingresado para horarios tiene un formato aceptable.
    Retorna True si es válido, False si no (o un mensaje de error).
    Esto es opcional y depende de tus reglas de negocio.
    """
    # Ejemplo simple: verificar que no esté vacío si es obligatorio
    # if not texto_horarios_ingresado.strip():
    #    return False, "Los horarios no pueden estar vacíos."
    return True, "" # Por ahora, siempre válido