#!/usr/bin/env python3
"""
Script para crear las tablas de la base de datos PostgreSQL
"""
import os
import sys

def crear_tablas():
    """Crear todas las tablas en PostgreSQL"""
    print("🏗️ CREANDO TABLAS EN POSTGRESQL")
    print("=" * 50)
    
    try:
        # Importar la aplicación y la base de datos
        from app import app, db
        
        print("✅ Aplicación importada correctamente")
        
        # Crear contexto de aplicación
        with app.app_context():
            print("🔧 Creando tablas...")
            
            # Crear todas las tablas
            db.create_all()
            
            print("✅ Tablas creadas exitosamente")
            
            # Verificar que las tablas se crearon
            from sqlalchemy import text
            result = db.session.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name;
            """))
            
            tablas = [row[0] for row in result]
            
            if tablas:
                print(f"\n📊 Tablas creadas ({len(tablas)}):")
                for tabla in tablas:
                    print(f"   • {tabla}")
            else:
                print("⚠️ No se encontraron tablas")
                
            return True
            
    except Exception as e:
        print(f"❌ Error creando tablas: {e}")
        return False

def poblar_datos_ejemplo():
    """Agregar datos de ejemplo"""
    print("\n📋 POBLANDO CON DATOS DE EJEMPLO")
    print("=" * 50)
    
    try:
        from app import app, db, EmpresaTuristica, SolicitudVisita, Usuario
        from datetime import date, time
        
        with app.app_context():
            # Verificar si ya hay datos
            if EmpresaTuristica.query.first():
                print("ℹ️ Ya existen datos en la base de datos")
                return True
            
            print("🏢 Creando empresas de ejemplo...")
            
            # Empresas de turismo de identidad (locales)
            empresas_identidad = [
                EmpresaTuristica(
                    nombre="Museo Histórico de la Colonización Esperanza",
                    descripcion="Museo que preserva la historia de la colonización suiza-alemana",
                    direccion="Av. San Martín 402",
                    telefono="(03496) 420-789",
                    email="museo@esperanza.gov.ar",
                    categoria="Turismo de Identidad",
                    capacidad_maxima=40,
                    duracion_visita="90 minutos"
                ),
                EmpresaTuristica(
                    nombre="Centro Cultural Municipal Casa Diefenbach",
                    descripcion="Centro cultural en edificio histórico de 1920",
                    direccion="Calle 25 de Mayo 356",
                    telefono="(03496) 420-123",
                    email="cultura@esperanza.gov.ar",
                    categoria="Turismo de Identidad",
                    capacidad_maxima=60,
                    duracion_visita="75 minutos"
                ),
                EmpresaTuristica(
                    nombre="Iglesia San Pedro",
                    descripcion="Primera iglesia de la colonia suiza, construida en 1862",
                    direccion="Plaza San Martín s/n",
                    telefono="(03496) 420-456",
                    email="sanpedro@esperanza.gov.ar",
                    categoria="Turismo de Identidad",
                    capacidad_maxima=80,
                    duracion_visita="60 minutos"
                )
            ]
            
            # Empresas de turismo educativo (externas)
            empresas_educativo = [
                EmpresaTuristica(
                    nombre="Granja Educativa Los Aromos",
                    descripcion="Experiencia educativa en granja con animales de granja",
                    direccion="Ruta Provincial 70 Km 8",
                    telefono="(03496) 421-555",
                    email="info@granjalosaromos.com",
                    categoria="Turismo Educativo",
                    capacidad_maxima=50,
                    duracion_visita="3 horas"
                ),
                EmpresaTuristica(
                    nombre="Reserva Natural Municipal",
                    descripcion="Reserva natural con senderos interpretativos y fauna nativa",
                    direccion="Camino Rural al Río Salado",
                    telefono="(03496) 421-777",
                    email="reserva@esperanza.gov.ar",
                    categoria="Turismo Educativo",
                    capacidad_maxima=35,
                    duracion_visita="2.5 horas"
                )
            ]
            
            # Agregar todas las empresas
            todas_empresas = empresas_identidad + empresas_educativo
            for empresa in todas_empresas:
                db.session.add(empresa)
            
            print(f"✅ Creadas {len(todas_empresas)} empresas")
            
            # Crear algunos usuarios de ejemplo
            print("👥 Creando usuarios de ejemplo...")
            
            usuarios = [
                Usuario(
                    username="admin",
                    email="admin@esperanza.gov.ar",
                    rol="Administrador"
                ),
                Usuario(
                    username="coordinador",
                    email="coordinador@esperanza.gov.ar", 
                    rol="Coordinador"
                )
            ]
            
            for usuario in usuarios:
                db.session.add(usuario)
                
            print(f"✅ Creados {len(usuarios)} usuarios")
            
            # Crear algunas solicitudes de ejemplo
            print("📝 Creando solicitudes de ejemplo...")
            
            solicitudes = [
                SolicitudVisita(
                    nombre_institucion="Escuela Primaria Nacional Esperanza",
                    responsable="María González",
                    telefono="(03496) 420-999",
                    email="direccion@escuelaesperanza.edu.ar",
                    cantidad_alumnos=25,
                    edad_alumnos="8 a 10 años",
                    discapacidad="No",
                    empresas_seleccionadas="Museo Histórico de la Colonización Esperanza,Centro Cultural Municipal Casa Diefenbach",
                    fecha_visita=date(2025, 9, 15),
                    hora_grupo1=time(9, 0),
                    hora_grupo2=time(14, 0),
                    observaciones="Grupo interesado en historia local.",
                    estado="Confirmada"
                )
            ]
            
            for solicitud in solicitudes:
                db.session.add(solicitud)
                
            print(f"✅ Creadas {len(solicitudes)} solicitudes")
            
            # Confirmar todos los cambios
            db.session.commit()
            print("\n🎉 ¡Datos de ejemplo creados exitosamente!")
            
            return True
            
    except Exception as e:
        print(f"❌ Error poblando datos: {e}")
        db.session.rollback()
        return False

if __name__ == "__main__":
    print("🚀 CONFIGURANDO BASE DE DATOS POSTGRESQL")
    print("=" * 60)
    
    # Crear tablas
    if crear_tablas():
        # Poblar con datos de ejemplo
        poblar_datos_ejemplo()
        
        print("\n🎉 CONFIGURACIÓN COMPLETADA")
        print("=" * 60)
        print("✅ Tablas creadas")
        print("✅ Datos de ejemplo agregados")
        print("🌐 Adminer: http://localhost:8080")
        print("🚀 Aplicación lista para ejecutar")
    else:
        print("\n❌ Error en la configuración")
