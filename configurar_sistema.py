"""
Script para configurar el sistema desde cero con SQLite
"""

import os
import sqlite3
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def configurar_sistema():
    """Configura el sistema desde cero"""
    print("🔧 CONFIGURANDO SISTEMA DESDE CERO")
    print("=" * 50)
    
    # 1. Asegurar que el directorio instance existe
    instance_dir = 'instance'
    if os.path.exists(instance_dir):
        print(f"📁 Directorio {instance_dir} existe")
    else:
        os.makedirs(instance_dir)
        print(f"📁 Directorio {instance_dir} creado")
    
    # 2. Eliminar base de datos existente si está corrupta
    db_path = os.path.join(instance_dir, 'visitas.db')
    if os.path.exists(db_path):
        try:
            os.remove(db_path)
            print(f"🗑️ Archivo de BD anterior eliminado: {db_path}")
        except Exception as e:
            print(f"⚠️ No se pudo eliminar BD anterior: {e}")
    
    # 3. Crear base de datos SQLite nueva
    try:
        # Crear archivo de base de datos vacío
        conn = sqlite3.connect(db_path)
        conn.close()
        print(f"✅ Nueva base de datos SQLite creada: {db_path}")
    except Exception as e:
        print(f"❌ Error al crear BD SQLite: {e}")
        return False
    
    # 4. Configurar la aplicación Flask
    try:
        from app import app, db, EmpresaTuristica
        
        with app.app_context():
            print(f"🔧 Configuración de la app: {app.config['SQLALCHEMY_DATABASE_URI']}")
            
            # Crear todas las tablas
            db.create_all()
            print("✅ Tablas de la base de datos creadas")
            
            # Verificar que se puede consultar
            count = EmpresaTuristica.query.count()
            print(f"📊 Empresas en BD: {count}")
            
            # Crear empresas de ejemplo si no hay ninguna
            if count == 0:
                print("➕ Creando empresas de ejemplo...")
                
                # Empresa de identidad
                empresa1 = EmpresaTuristica(
                    nombre="Museo de la Colonización",
                    correo="museo@esperanza.gov.ar",
                    telefono="03496-123456",
                    direccion="Av. San Martín 123, Esperanza",
                    servicios_ofrecidos="Visitas guiadas, exhibiciones interactivas",
                    descripcion="Museo histórico sobre la colonización",
                    categoria_turismo="identidad",
                    nivel_educativo_objetivo="Ambos",
                    capacidad_maxima=50,
                    costo_por_persona=100.0,
                    requiere_reserva=True,
                    activa=True
                )
                
                # Empresa educativa
                empresa2 = EmpresaTuristica(
                    nombre="Granja Educativa Los Ñandúes",
                    correo="info@granjalosnanques.com",
                    telefono="03496-789012",
                    direccion="Ruta 70 Km 15, Esperanza",
                    servicios_ofrecidos="Actividades rurales, contacto con animales",
                    descripcion="Granja educativa para conocer la vida rural",
                    categoria_turismo="educativo",
                    nivel_educativo_objetivo="Primario",
                    capacidad_maxima=40,
                    costo_por_persona=200.0,
                    requiere_reserva=True,
                    activa=True
                )
                
                # Más empresas...
                empresa3 = EmpresaTuristica(
                    nombre="Casa de la Cultura",
                    correo="cultura@esperanza.gov.ar",
                    categoria_turismo="identidad",
                    nivel_educativo_objetivo="Primario",
                    activa=True
                )
                
                empresa4 = EmpresaTuristica(
                    nombre="Centro de Innovación Tecnológica",
                    correo="tech@esperanza.edu.ar",
                    categoria_turismo="educativo",
                    nivel_educativo_objetivo="Secundario",
                    activa=True
                )
                
                db.session.add_all([empresa1, empresa2, empresa3, empresa4])
                db.session.commit()
                
                count = EmpresaTuristica.query.count()
                print(f"✅ {count} empresas de ejemplo creadas")
                
                # Mostrar empresas por categoría
                identidad_count = EmpresaTuristica.query.filter_by(categoria_turismo='identidad').count()
                educativo_count = EmpresaTuristica.query.filter_by(categoria_turismo='educativo').count()
                
                print(f"   🏛️ Identidad: {identidad_count}")
                print(f"   🎓 Educativo: {educativo_count}")
    
    except Exception as e:
        print(f"❌ Error al configurar la aplicación: {e}")
        return False
    
    print("\n🎉 SISTEMA CONFIGURADO EXITOSAMENTE!")
    print("✅ Base de datos SQLite funcionando")
    print("✅ Empresas de ejemplo creadas")
    print("✅ Sistema listo para usar")
    print("\n🚀 Para ejecutar:")
    print("   python app.py")
    print("   Luego ve a: http://localhost:5000")
    
    return True

if __name__ == "__main__":
    configurar_sistema()
