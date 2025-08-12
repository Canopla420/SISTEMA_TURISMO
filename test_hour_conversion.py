#!/usr/bin/env python3
"""
Script de prueba para verificar la conversión de horas
"""
from datetime import datetime

def convertir_hora(hora_str):
    """Función auxiliar para convertir hora - misma lógica que en app.py"""
    if not hora_str:
        return None
    try:
        # Intentar primero con formato HH:MM:SS
        return datetime.strptime(hora_str, '%H:%M:%S').time()
    except ValueError:
        try:
            # Si falla, intentar con formato HH:MM
            return datetime.strptime(hora_str, '%H:%M').time()
        except ValueError:
            return None

# Casos de prueba
test_cases = [
    "14:30",        # Formato sin segundos (input HTML)
    "14:30:00",     # Formato con segundos (base de datos)
    "09:15",        # Otro caso sin segundos
    "09:15:30",     # Otro caso con segundos
    "",             # Cadena vacía
    None,           # None
    "invalid",      # Formato inválido
]

print("Pruebas de conversión de hora:")
print("="*40)

for test_input in test_cases:
    result = convertir_hora(test_input)
    print(f"Input: {test_input!r:12} -> Output: {result}")
    
print("\nPruebas de formateo para template HTML:")
print("="*40)

# Probar formateo como en el template
for test_input in ["14:30", "14:30:00", "09:15:30"]:
    hora_obj = convertir_hora(test_input)
    if hora_obj:
        formatted = hora_obj.strftime('%H:%M')
        print(f"Input: {test_input!r:12} -> Object: {hora_obj} -> HTML: {formatted}")
    else:
        print(f"Input: {test_input!r:12} -> Object: None -> HTML: ''")
