#!/usr/bin/env python3
"""
Script para crear tablas en PostgreSQL de manera robusta
"""
import psycopg2
from psycopg2 import sql
import sys

def crear_tablas_postgresql():
    """Crear tablas directamente con psycopg2"""
    
    # Configuración de conexión
    config = {
        'host': 'localhost',
        'port': 5432,
        'database': 'turismo_esperanza',
        'user': 'admin_turismo',
        'password': 'TurismoEsperanza2024!'
    }
    
    print("🔌 Conectando a PostgreSQL...")
    
    try:
        # Conectar a PostgreSQL
        conn = psycopg2.connect(**config)
        conn.autocommit = True
        cur = conn.cursor()
        
        print("✅ Conexión establecida")
        
        # Crear tabla de usuarios
        print("📋 Creando tabla usuarios...")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS usuario (
                id SERIAL PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL,
                email VARCHAR(120) UNIQUE NOT NULL,
                contraseña VARCHAR(255) NOT NULL,
                activo BOOLEAN DEFAULT TRUE,
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        # Crear tabla de empresas turísticas
        print("🏢 Creando tabla empresas_turisticas...")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS empresa_turistica (
                id SERIAL PRIMARY KEY,
                nombre VARCHAR(200) NOT NULL,
                direccion TEXT,
                telefono VARCHAR(20),
                email VARCHAR(120),
                sitio_web VARCHAR(255),
                categoria VARCHAR(50) NOT NULL CHECK (categoria IN ('Turismo de Identidad', 'Turismo Educativo')),
                descripcion TEXT,
                servicios TEXT,
                horarios TEXT,
                precio_entrada DECIMAL(10,2),
                activo BOOLEAN DEFAULT TRUE,
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        # Crear tabla de solicitudes de visita
        print("📝 Creando tabla solicitudes_visita...")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS solicitud_visita (
                id SERIAL PRIMARY KEY,
                nombre_institucion VARCHAR(200) NOT NULL,
                nombre_referente VARCHAR(100) NOT NULL,
                telefono_referente VARCHAR(20) NOT NULL,
                email_referente VARCHAR(120) NOT NULL,
                cantidad_alumnos INTEGER NOT NULL,
                cantidad_acompanantes INTEGER NOT NULL,
                edad_alumnos VARCHAR(50),
                discapacidad VARCHAR(10) DEFAULT 'No',
                empresas_seleccionadas TEXT,
                fecha_visita DATE,
                hora_grupo1 TIME,
                hora_grupo2 TIME,
                observaciones TEXT,
                estado VARCHAR(20) DEFAULT 'Pendiente' CHECK (estado IN ('Pendiente', 'Confirmada', 'Rechazada', 'Completada')),
                fecha_solicitud TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                fecha_respuesta TIMESTAMP
            );
        """)
        
        print("✅ Todas las tablas creadas exitosamente")
        
        # Verificar tablas creadas
        cur.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' AND table_type = 'BASE TABLE';
        """)
        
        tablas = cur.fetchall()
        print(f"📊 Tablas en la base de datos: {[t[0] for t in tablas]}")
        
        cur.close()
        conn.close()
        
        return True
        
    except psycopg2.Error as e:
        print(f"❌ Error de PostgreSQL: {e}")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

def poblar_datos_ejemplo():
    """Poblar con datos de ejemplo"""
    
    config = {
        'host': 'localhost',
        'port': 5432,
        'database': 'turismo_esperanza',
        'user': 'admin_turismo',
        'password': 'TurismoEsperanza2024!'
    }
    
    try:
        conn = psycopg2.connect(**config)
        cur = conn.cursor()
        
        print("📋 Poblando datos de ejemplo...")
        
        # Insertar empresas de ejemplo
        empresas = [
            ('Museo Histórico de la Colonización Esperanza', 'Av. San Martín 1050', '03496-420147', 'museo@esperanza.gov.ar', 'www.museohispericoesperanza.gob.ar', 'Turismo de Identidad', 'Museo que preserva la historia de la colonización suiza en Esperanza', 'Visitas guiadas, exposiciones permanentes, talleres educativos', 'Lunes a Viernes 8:00-12:00 y 14:00-18:00', 0.00),
            ('Centro Cultural Municipal Casa Diefenbach', 'Av. San Martín 1045', '03496-420147', 'cultura@esperanza.gov.ar', '', 'Turismo de Identidad', 'Casa histórica convertida en centro cultural', 'Exposiciones de arte, eventos culturales, talleres', 'Lunes a Viernes 8:00-12:00 y 14:00-18:00', 0.00),
            ('Parque Histórico Dr. Julio Marc', 'Av. San Martín y Bv. Racedo', '03496-420147', 'turismo@esperanza.gov.ar', '', 'Turismo de Identidad', 'Parque histórico con monumentos de la colonización', 'Caminatas, actividades recreativas', 'Todos los días 24 horas', 0.00),
            ('Estación del Ferrocarril Belgrano', 'Av. Estación', '03496-420147', 'patrimonio@esperanza.gov.ar', '', 'Turismo de Identidad', 'Estación histórica del ferrocarril', 'Visitas al patrimonio ferroviario', 'Coordinar previamente', 0.00),
            ('Granja Educativa Los Aromos', 'Ruta Provincial 70 Km 15', '03496-15-234567', 'info@granjaeducativa.com', 'www.granjaeducativa.com', 'Turismo Educativo', 'Granja educativa con animales de campo', 'Interacción con animales, talleres rurales', 'Martes a Domingos 9:00-17:00', 150.00)
        ]
        
        for empresa in empresas:
            cur.execute("""
                INSERT INTO empresa_turistica 
                (nombre, direccion, telefono, email, sitio_web, categoria, descripcion, servicios, horarios, precio_entrada)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (nombre) DO NOTHING;
            """, empresa)
        
        # Insertar usuario administrador
        cur.execute("""
            INSERT INTO usuario (nombre, email, contraseña)
            VALUES ('Administrador', 'admin@esperanza.gov.ar', 'admin123')
            ON CONFLICT (email) DO NOTHING;
        """)
        
        conn.commit()
        print("✅ Datos de ejemplo insertados")
        
        cur.close()
        conn.close()
        
        return True
        
    except psycopg2.Error as e:
        print(f"❌ Error poblando datos: {e}")
        return False

if __name__ == "__main__":
    print("🐘 CONFIGURANDO POSTGRESQL")
    print("=" * 50)
    
    if crear_tablas_postgresql():
        print("\n📊 POBLANDO DATOS DE EJEMPLO")
        print("=" * 50)
        if poblar_datos_ejemplo():
            print("\n🎉 BASE DE DATOS CONFIGURADA EXITOSAMENTE!")
            print("=" * 50)
            print("✅ PostgreSQL funcionando")
            print("✅ Tablas creadas")
            print("✅ Datos de ejemplo insertados")
            print("\n🌐 Puedes acceder a:")
            print("• Adminer: http://localhost:8080")
            print("• PgAdmin: http://localhost:5050")
        else:
            print("❌ Error poblando datos")
            sys.exit(1)
    else:
        print("❌ Error creando tablas")
        sys.exit(1)
