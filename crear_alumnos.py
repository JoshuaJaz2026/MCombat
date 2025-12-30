import os
import django
import random

# 1. Configuración para que este script entienda a Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MCombat.settings')
django.setup()

from asistencia.models import Alumno

# 2. Listas de datos falsos para mezclar
nombres = ["Miguel", "Andrea", "Lucas", "Lucía", "Carlos", "María", "Jorge", "Elena", "Pedro", "Sofía", "Raúl", "Paula", "Diego", "Valentina", "Javier"]
apellidos = ["García", "Rodríguez", "López", "Martínez", "González", "Pérez", "Sánchez", "Romero", "Díaz", "Flores", "Torres", "Ruiz"]

print("🥊 Iniciando la creación de alumnos...")

# 3. El Bucle: Repetir 20 veces
for i in range(20):
    nombre_azar = random.choice(nombres)
    apellido_azar = random.choice(apellidos)
    
    # Creamos un DNI falso que no se repita (ej: 10000, 10001, 10002...)
    dni_falso = f"88800{i}" 
    
    # Creamos el alumno en la Base de Datos
    # Usamos 'get_or_create' para que no de error si corres el script dos veces
    alumno, creado = Alumno.objects.get_or_create(
        dni=dni_falso,
        defaults={
            'nombre': nombre_azar,
            'apellido': apellido_azar,
            'telefono': f"9990000{i}"
        }
    )

    if creado:
        print(f"✅ Creado: {nombre_azar} {apellido_azar} (DNI: {dni_falso})")
    else:
        print(f"⚠️ Ya existe: {nombre_azar} {apellido_azar}")

print("🎉 ¡Listo! 20 alumnos generados.")