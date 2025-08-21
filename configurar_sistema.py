#!/usr/bin/env python3
"""
Script de configuración para el Sistema de Gestión de Visitas Turísticas
PostgreSQL + Docker
"""

import subprocess
import time
from datetime import date, time as dt_time

def verificar_docker():
    """Verifica que Docker esté instalado y funcionando"""
    try:
        subprocess.run(['docker', '--version'], 
                      capture_output=True, text=True, check=True)
        print("✅ Docker instalado")
        
        subprocess.run(['docker', 'compose', 'version'], 
                      capture_output=True, text=True, check=True)
        print("✅ Docker Compose disponible")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Docker no está instalado o no está disponible")
        print("   Instala Docker Desktop desde: https://www.docker.com/products/docker-desktop")
        return False

def configurar_postgresql():
    """Configura PostgreSQL con Docker"""
    
    print("🐘 CONFIGURANDO POSTGRESQL CON DOCKER")
    print("=" * 60)
    
    # 1. Verificar Docker
    if not verificar_docker():
        return False
    
    # 2. Limpiar contenedores anteriores
    print("\n🧹 Limpiando configuración anterior...")
    try:
        subprocess.run(['docker', 'compose', 'down', '-v'], 
                      capture_output=True, check=False)
        print("   ✅ Contenedores anteriores eliminados")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("   ℹ️ No había contenedores anteriores")
    
    # 3. Iniciar PostgreSQL
    print("\n🚀 Iniciando PostgreSQL...")
    try:
        subprocess.run(['docker', 'compose', 'up', '-d', 'postgres_turismo'], 
                      capture_output=True, text=True, check=True)
        print("   ✅ PostgreSQL iniciado")
        
        # Esperar a que PostgreSQL esté listo
        print("   ⏳ Esperando que PostgreSQL esté listo...")
        time.sleep(10)
        
        # Iniciar Adminer
        subprocess.run(['docker', 'compose', 'up', '-d', 'adminer'], 
                      capture_output=True, text=True, check=True)
        print("   ✅ Adminer iniciado")
        
    except subprocess.CalledProcessError as e:
        print(f"   ❌ Error al iniciar contenedores: {e}")
        return False
    
    # 4. Instalar dependencias Python
    print("\n📦 Instalando dependencias Python...")
    try:
        subprocess.run(['pip', 'install', '-r', 'requirements.txt'], 
                      capture_output=True, text=True, check=True)
        print("   ✅ Dependencias instaladas")
    except subprocess.CalledProcessError as e:
        print(f"   ❌ Error instalando dependencias: {e}")
        return False
    
    # 5. Crear estructura de base de datos
    print("\n🏗️ Creando estructura de base de datos...")
    try:
        from app import app, db
        
        with app.app_context():
            # Crear todas las tablas
            db.create_all()
            print("   ✅ Tablas creadas")
            
            # Verificar tablas creadas
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tablas = inspector.get_table_names()
            print(f"   📊 Tablas: {', '.join(tablas)}")
            
    except (ImportError, AttributeError, ValueError) as e:
        print(f"   ❌ Error creando estructura: {e}")
        return False
    
    # 6. Poblar con datos de ejemplo
    print("\n📋 Poblando con datos de ejemplo...")
    try:
        poblar_datos_ejemplo()
        print("   ✅ Datos de ejemplo creados")
    except (ImportError, AttributeError, ValueError) as e:
        print(f"   ❌ Error poblando datos: {e}")
        return False
    
    print("\n🎉 SISTEMA CONFIGURADO EXITOSAMENTE!")
    print("=" * 60)
    print("✅ PostgreSQL ejecutándose en Docker")
    print("✅ Base de datos creada y poblada")
    print("✅ Sistema listo para usar")
    
    print("\n🔗 ACCESOS:")
    print("   🖥️  Aplicación: http://localhost:5000")
    print("   🗄️  Adminer: http://localhost:8080")
    
    print("\n🚀 PARA EJECUTAR EL SISTEMA:")
    print("   python app.py")
    
    return True

def poblar_datos_ejemplo():
    """Puebla la base de datos con datos de ejemplo"""
    
    from app import app, db, EmpresaTuristica, SolicitudVisita
    
    with app.app_context():
        # Verificar si ya hay datos
        if EmpresaTuristica.query.count() > 0:
            print("   ℹ️ Base de datos ya tiene datos")
            return
        
        # EMPRESAS DE TURISMO DE IDENTIDAD (para instituciones locales)
        empresas_identidad = [
            EmpresaTuristica(
                nombre='Museo Histórico de la Colonización Esperanza',
                correo='educacion@museoesperanza.gov.ar',
                telefono='+54 3496 421100',
                direccion='Plaza San Martín 150, Esperanza, Santa Fe',
                servicios_ofrecidos='Visitas guiadas especializadas, talleres de historia local, exhibiciones interactivas',
                descripcion='Principal museo de la ciudad dedicado a preservar la historia de la colonización suiza',
                categoria_turismo='identidad',
                nivel_educativo_objetivo='Ambos',
                capacidad_maxima=60,
                horarios_atencion='Martes a Domingo 9:00-17:00',
                costo_por_persona=350.00,
                requiere_reserva=True,
                activa=True
            ),
            EmpresaTuristica(
                nombre='Centro Cultural Municipal Casa Diefenbach',
                correo='cultura@esperanza.gov.ar',
                telefono='+54 3496 421200',
                direccion='Av. San Martín 456, Esperanza, Santa Fe',
                servicios_ofrecidos='Talleres artísticos, exposiciones temporales, actividades culturales',
                descripcion='Centro neurálgico de la actividad cultural esperancense',
                categoria_turismo='identidad',
                nivel_educativo_objetivo='Primario',
                capacidad_maxima=45,
                horarios_atencion='Lunes a Viernes 8:00-18:00',
                costo_por_persona=200.00,
                requiere_reserva=True,
                activa=True
            )
        ]
        
        # EMPRESAS DE TURISMO EDUCATIVO (para instituciones externas)
        empresas_educativo = [
            EmpresaTuristica(
                nombre='Granja Educativa "El Campo"',
                correo='visitas@granjaelcampo.com.ar',
                telefono='+54 3496 445566',
                direccion='Ruta Provincial 6 Km 8, Esperanza',
                servicios_ofrecidos='Actividades rurales, contacto con animales, talleres de agricultura',
                descripcion='Experiencia educativa en ambiente rural con actividades prácticas',
                categoria_turismo='educativo',
                nivel_educativo_objetivo='Primario',
                capacidad_maxima=50,
                horarios_atencion='Martes a Sábado 9:00-16:00',
                costo_por_persona=400.00,
                requiere_reserva=True,
                activa=True
            ),
            EmpresaTuristica(
                nombre='Centro de Innovación Tecnológica',
                correo='educacion@centrotech.edu.ar',
                telefono='+54 3496 333444',
                direccion='Parque Tecnológico, Esperanza',
                servicios_ofrecidos='Talleres de robótica, programación, ciencias aplicadas',
                descripcion='Centro de vanguardia en tecnología educativa',
                categoria_turismo='educativo',
                nivel_educativo_objetivo='Secundario',
                capacidad_maxima=30,
                horarios_atencion='Lunes a Viernes 8:00-17:00',
                costo_por_persona=500.00,
                requiere_reserva=True,
                activa=True
            )
        ]
        
        # Agregar todas las empresas
        for empresa in empresas_identidad + empresas_educativo:
            db.session.add(empresa)
        
        # Crear una solicitud de ejemplo
        solicitud_ejemplo = SolicitudVisita(
            nombre_institucion='Escuela Primaria N° 123',
            localidad='Esperanza, Santa Fe',
            tipo_institucion='local',
            es_de_esperanza=True,
            director='María González',
            correo_institucional='direccion@escuela123.edu.ar',
            telefono_institucion='+54 3496 111222',
            contacto_principal='Ana López',
            telefono_contacto_principal='+54 3496 111223',
            relacion_contacto='Maestra de 5° grado',
            nivel_educativo='Primario',
            cantidad_alumnos=25,
            edad_alumnos='10 a 11 años',
            discapacidad='No',
            empresas_seleccionadas='Museo Histórico de la Colonización Esperanza',
            fecha_visita=date(2025, 9, 15),
            hora_grupo1=dt_time(9, 0),
            observaciones='Primera visita del año escolar',
            estado='Pendiente'
        )
        
        db.session.add(solicitud_ejemplo)
        db.session.commit()
        
        print(f"   📊 {len(empresas_identidad + empresas_educativo)} empresas creadas")
        print("   📋 1 solicitud de ejemplo creada")

if __name__ == "__main__":
    configurar_postgresql()
