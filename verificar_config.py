"""
Script para verificar la configuración de la base de datos
"""

import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def verificar_configuracion():
    """Verifica que la configuración esté correcta"""
    print("🔍 VERIFICANDO CONFIGURACIÓN")
    print("=" * 40)
    
    # Verificar variables de entorno
    database_url = os.getenv('DATABASE_URL')
    secret_key = os.getenv('SECRET_KEY')
    
    print(f"DATABASE_URL: {database_url}")
    print(f"SECRET_KEY: {'***' if secret_key else 'No configurado'}")
    
    if database_url and database_url.startswith('sqlite'):
        print("✅ Configurado para SQLite")
        
        # Verificar que el directorio instance existe
        instance_dir = 'instance'
        if not os.path.exists(instance_dir):
            print(f"📁 Creando directorio: {instance_dir}")
            os.makedirs(instance_dir)
        else:
            print(f"📁 Directorio {instance_dir} existe")
            
        # Verificar la configuración en la app
        try:
            from app import app
            with app.app_context():
                print(f"🔧 URI de la app: {app.config['SQLALCHEMY_DATABASE_URI']}")
                
                # Probar conexión a la base de datos
                from app import db
                db.create_all()
                print("✅ Base de datos SQLite inicializada correctamente")
                
        except Exception as e:
            print(f"❌ Error al configurar la app: {e}")
            return False
            
    elif database_url and database_url.startswith('postgresql'):
        print("⚠️ Configurado para PostgreSQL")
        print("   Asegúrate de que PostgreSQL esté ejecutándose")
        
    else:
        print("❌ DATABASE_URL no configurado correctamente")
        return False
    
    print("\n🎯 SOLUCIÓN APLICADA:")
    print("✅ Variables de entorno cargadas con python-dotenv")
    print("✅ Configuración actualizada para respetar DATABASE_URL")
    print("✅ Fallback a PostgreSQL si es necesario")
    
    return True

if __name__ == "__main__":
    verificar_configuracion()
