"""
Script para crear la base de datos con la nueva estructura
"""
import os
import sys

# Agregar el directorio del proyecto al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db

def crear_base_datos():
    """Crear todas las tablas de la base de datos"""
    with app.app_context():
        try:
            # Crear todas las tablas
            db.create_all()
            print("✅ Base de datos creada exitosamente")
            print("📊 Tablas creadas:")
            
            # Verificar las tablas creadas
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tablas = inspector.get_table_names()
            
            for tabla in tablas:
                print(f"   - {tabla}")
                
        except (ValueError, TypeError, OSError) as e:
            print(f"❌ Error al crear la base de datos: {e}")
            return False
    
    return True

def agregar_datos_ejemplo():
    """Agregar algunos datos de ejemplo para probar el sistema"""
    from app import EmpresaTuristica
    
    with app.app_context():
        try:
            # Verificar si ya hay datos
            if EmpresaTuristica.query.count() > 0:
                print("📋 Ya existen datos en la base de datos")
                return True
            
            # Crear empresas de ejemplo
            empresas_ejemplo = [
                EmpresaTuristica(
                    nombre="Turismo Esperanza",
                    correo="info@turismoesperanza.com",
                    telefono="3496-123456",
                    direccion="Av. Principal 123, Esperanza",
                    servicios_ofrecidos="Tours por la ciudad, visitas a museos, recorridos históricos",
                    descripcion="Empresa local especializada en turismo de identidad",
                    categoria_turismo="identidad",
                    nivel_educativo_objetivo="Ambos",
                    capacidad_maxima=50,
                    horarios_atencion="9:00 - 17:00",
                    costo_por_persona=1500.00,
                    requiere_reserva=True
                ),
                EmpresaTuristica(
                    nombre="EcoTurismo Santa Fe",
                    correo="contacto@ecoturismosf.com",
                    telefono="342-987654",
                    direccion="Ruta 11 Km 445",
                    servicios_ofrecidos="Visitas a parques naturales, actividades ecológicas",
                    descripcion="Turismo educativo enfocado en la naturaleza",
                    categoria_turismo="educativo",
                    nivel_educativo_objetivo="Primario",
                    capacidad_maxima=40,
                    horarios_atencion="8:00 - 16:00",
                    costo_por_persona=2000.00,
                    requiere_reserva=True
                ),
                EmpresaTuristica(
                    nombre="Aventura Norte",
                    correo="info@aventuranorte.com",
                    telefono="3496-555123",
                    direccion="Zona Industrial Norte",
                    servicios_ofrecidos="Actividades de aventura y deportes",
                    descripcion="Empresa especializada en turismo aventura para jóvenes",
                    categoria_turismo="educativo",
                    nivel_educativo_objetivo="Secundario",
                    capacidad_maxima=30,
                    horarios_atencion="9:00 - 18:00",
                    costo_por_persona=2500.00,
                    requiere_reserva=True
                )
            ]
            
            for empresa in empresas_ejemplo:
                db.session.add(empresa)
            
            db.session.commit()
            print("✅ Datos de ejemplo agregados exitosamente")
            print(f"📊 Se agregaron {len(empresas_ejemplo)} empresas de ejemplo")
            
        except (ValueError, TypeError, OSError) as e:
            db.session.rollback()
            print(f"❌ Error al agregar datos de ejemplo: {e}")
            return False
    
    return True

if __name__ == "__main__":
    print("🚀 Iniciando creación de base de datos...")
    print("=" * 50)
    
    # Crear el directorio instance si no existe
    instance_dir = os.path.join(os.path.dirname(__file__), 'instance')
    if not os.path.exists(instance_dir):
        os.makedirs(instance_dir)
        print(f"📁 Directorio 'instance' creado: {instance_dir}")
    
    # Crear base de datos
    if crear_base_datos():
        print()
        print("¿Deseas agregar datos de ejemplo? (s/n): ", end="")
        respuesta = input().lower().strip()
        
        if respuesta in ['s', 'si', 'sí', 'y', 'yes']:
            agregar_datos_ejemplo()
    
    print()
    print("=" * 50)
    print("🎉 Proceso completado!")
    print("💡 Ahora puedes ejecutar la aplicación con: python app.py")
