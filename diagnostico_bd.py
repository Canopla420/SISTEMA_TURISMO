"""
Script de diagnóstico para la base de datos
"""
import os
import sqlite3
from datetime import datetime

def diagnosticar_bd():
    """Diagnosticar problemas con la base de datos"""
    print("🔍 DIAGNÓSTICO DE BASE DE DATOS")
    print("=" * 50)
    
    # Verificar variables de entorno
    print(f"📁 Directorio actual: {os.getcwd()}")
    print(f"🔧 FLASK_CONFIG: {os.getenv('FLASK_CONFIG', 'No definido')}")
    print(f"💾 DATABASE_URL: {os.getenv('DATABASE_URL', 'No definido')}")
    
    # Verificar archivos de BD
    instance_dir = os.path.join(os.getcwd(), 'instance')
    print(f"\n📂 Directorio instance: {instance_dir}")
    print(f"📂 Existe directorio instance: {os.path.exists(instance_dir)}")
    
    if os.path.exists(instance_dir):
        archivos = os.listdir(instance_dir)
        print(f"📋 Archivos en instance: {archivos}")
        
        for archivo in archivos:
            if archivo.endswith('.db'):
                ruta_archivo = os.path.join(instance_dir, archivo)
                tamaño = os.path.getsize(ruta_archivo)
                print(f"   💽 {archivo}: {tamaño} bytes")
                
                # Intentar conectar a la BD
                try:
                    conn = sqlite3.connect(ruta_archivo)
                    cursor = conn.cursor()
                    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                    tablas = cursor.fetchall()
                    conn.close()
                    print(f"   ✅ {archivo}: Conexión exitosa")
                    print(f"   📊 Tablas: {[tabla[0] for tabla in tablas]}")
                except Exception as e:
                    print(f"   ❌ {archivo}: Error al conectar - {e}")
    
    # Probar la configuración de Flask
    print(f"\n🧪 PROBANDO CONFIGURACIÓN DE FLASK")
    print("=" * 40)
    
    try:
        # Importar la configuración
        from config import config
        from dotenv import load_dotenv
        
        load_dotenv()
        config_name = os.getenv('FLASK_CONFIG', 'development')
        
        print(f"📋 Configuración activa: {config_name}")
        
        config_obj = config[config_name]
        db_uri = config_obj.SQLALCHEMY_DATABASE_URI
        print(f"🔗 URI de BD: {db_uri}")
        
        # Extraer la ruta del archivo de la URI
        if db_uri.startswith('sqlite:///'):
            db_path = db_uri[10:]  # Remover 'sqlite:///'
            print(f"📍 Ruta de archivo: {db_path}")
            print(f"📁 Ruta absoluta: {os.path.abspath(db_path)}")
            print(f"✅ Archivo existe: {os.path.exists(db_path)}")
            
            if os.path.exists(db_path):
                # Verificar permisos
                print(f"📖 Lectura: {os.access(db_path, os.R_OK)}")
                print(f"✏️  Escritura: {os.access(db_path, os.W_OK)}")
            
    except Exception as e:
        print(f"❌ Error al probar configuración: {e}")
    
    # Probar conexión directa con SQLAlchemy
    print(f"\n🔗 PROBANDO SQLALCHEMY")
    print("=" * 30)
    
    try:
        from sqlalchemy import create_engine
        from config import config
        
        config_name = os.getenv('FLASK_CONFIG', 'development')
        config_obj = config[config_name]
        
        engine = create_engine(config_obj.SQLALCHEMY_DATABASE_URI)
        connection = engine.connect()
        result = connection.execute("SELECT 1")
        connection.close()
        print("✅ Conexión SQLAlchemy: OK")
        
    except Exception as e:
        print(f"❌ Error SQLAlchemy: {e}")

if __name__ == "__main__":
    diagnosticar_bd()
