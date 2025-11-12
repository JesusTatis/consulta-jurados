"""
Utilidades de validación
"""

def validar_cedula(cedula: str) -> tuple[bool, str]:
    """
    Valida que la cédula tenga formato correcto
    
    Args:
        cedula: Número de cédula a validar
        
    Returns:
        tuple: (es_valida, mensaje_error)
    """
    cedula = cedula.strip()
    
    if not cedula:
        return False, "La cédula no puede estar vacía"
    
    if not cedula.isdigit():
        return False, "La cédula debe contener solo números"
    
    if len(cedula) < 6 or len(cedula) > 10:
        return False, "La cédula debe tener entre 6 y 10 dígitos"
    
    return True, ""