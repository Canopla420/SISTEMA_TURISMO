#!/usr/bin/env python3
"""
Script para configurar PostgreSQL con Docker para el Sistema de Turismo
"""

import os
import subprocess
import time
try:
    import psycopg2
    PSYCOPG2_AVAILABLE = True
except ImportError:
    PSYCOPG2_AVAILABLE = False
    print("⚠️ psycopg2 no está instalado. Se instalará automáticamente.")

try:
    from dotenv import load_dotenv
    PYTHON_DOTENV_AVAILABLE = True
except ImportError:
    PYTHON_DOTENV_AVAILABLE = False
    print("⚠️ python-dotenv no está instalado. Se instalará automáticamente.")

def verificar_docker():
    """Verifica que Docker esté instalado y funcionando"""
    try:
        result = subprocess.run(['docker', '--version'], 
                              capture_output=True, text=True, check=True)
        print(f"✅ Docker encontrado: {result.stdout.strip()}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Docker no está instalado o no está en el PATH")
        print("   Instala Docker Desktop desde: https://www.docker.com/products/docker-desktop")
        return False

def verificar_docker_compose():
    """Verifica que Docker Compose esté disponible"""
    try:
        result = subprocess.run(['docker', 'compose', 'version'], 
                              capture_output=True, text=True, check=True)
        print(f"✅ Docker Compose encontrado: {result.stdout.strip()}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Docker Compose no está disponible")
        return False

def configurar_postgresql():
    """Configura PostgreSQL con Docker"""
    
    print("🐘 CONFIGURANDO POSTGRESQL CON DOCKER")
    print("=" * 60)
    
    # 1. Verificar Docker
    print("\n1️⃣ VERIFICANDO DOCKER...")
    if not verificar_docker() or not verificar_docker_compose():
        return False
    
    # 2. Parar contenedores existentes
    print("\n2️⃣ LIMPIANDO CONFIGURACIÓN ANTERIOR...")
    try:
        subprocess.run(['docker', 'compose', 'down', '-v'], 
                      capture_output=True, check=False)
        print("   🧹 Contenedores anteriores eliminados")
    except (OSError, subprocess.SubprocessError):
        print("   ℹ️ No había contenedores anteriores")
    
    # 3. Configurar variables de entorno
    print("\n3️⃣ CONFIGURANDO VARIABLES DE ENTORNO...")
    
    # Copiar archivo de configuración
    if os.path.exists('.env.postgres'):
        if os.path.exists('.env'):
            os.rename('.env', '.env.backup')
            print("   💾 Respaldo de .env anterior creado")
        
        os.rename('.env.postgres', '.env')
        print("   ✅ Configuración PostgreSQL activada")
    
    # Cargar variables
    if PYTHON_DOTENV_AVAILABLE:
        load_dotenv()
    else:
        print("   ⚠️ python-dotenv no disponible, usando variables del sistema")
    
    # 4. Levantar contenedores
    print("\n4️⃣ LEVANTANDO CONTENEDORES...")
    
    try:
        print("   🚀 Iniciando PostgreSQL...")
        subprocess.run(['docker', 'compose', 'up', '-d', 'postgres_turismo'], 
                      capture_output=True, text=True, check=True)
        print("   ✅ PostgreSQL iniciado")
        
        # Esperar a que PostgreSQL esté listo
        print("   ⏳ Esperando que PostgreSQL esté listo...")
        max_attempts = 30
        for attempt in range(max_attempts):
            try:
                conn = psycopg2.connect(
                    host='localhost',
                    port=5432,
                    database='turismo_esperanza',
                    user='admin_turismo',
                    password='TurismoEsperanza2024!'
                )
                conn.close()
                print(f"   ✅ PostgreSQL listo después de {attempt + 1} intentos")
                break
            except psycopg2.OperationalError:
                time.sleep(2)
                if attempt == max_attempts - 1:
                    print("   ❌ PostgreSQL no respondió en tiempo esperado")
                    return False
        
        # Iniciar Adminer
        print("   🌐 Iniciando Adminer...")
        subprocess.run(['docker', 'compose', 'up', '-d', 'adminer'], 
                      capture_output=True, text=True, check=True)
        print("   ✅ Adminer iniciado en http://localhost:8080")
        
    except subprocess.CalledProcessError as e:
        print(f"   ❌ Error al iniciar contenedores: {e}")
        return False
    
    # 5. Instalar dependencia de PostgreSQL
    print("\n5️⃣ INSTALANDO DEPENDENCIAS PYTHON...")
    
    try:
        subprocess.run(['pip', 'install', 'psycopg2-binary'], 
                      capture_output=True, text=True, check=True)
        print("   ✅ psycopg2-binary instalado")
    except subprocess.CalledProcessError:
        print("   ⚠️ Error instalando psycopg2-binary, intentando con psycopg2...")
        try:
            subprocess.run(['pip', 'install', 'psycopg2'], 
                          capture_output=True, text=True, check=True)
            print("   ✅ psycopg2 instalado")
        except subprocess.CalledProcessError as e:
            print(f"   ❌ Error instalando driver PostgreSQL: {e}")
            return False
    
    # 6. Crear estructura de base de datos
    print("\n6️⃣ CREANDO ESTRUCTURA DE BASE DE DATOS...")
    
    try:
        from app import app, db
        
        with app.app_context():
            print(f"   🔧 Conectando a: {app.config['SQLALCHEMY_DATABASE_URI']}")
            
            # Crear todas las tablas
            db.create_all()
            print("   ✅ Tablas creadas exitosamente")
            
            # Verificar tablas usando inspector
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tabla_names = inspector.get_table_names()
            print(f"   📊 Tablas creadas: {len(tabla_names)}")
            for tabla in tabla_names:
                print(f"      - {tabla}")
            
    except (ImportError, ValueError, TypeError, OSError) as e:
        print(f"   ❌ Error creando estructura: {e}")
        return False
    
    # 7. Poblar con datos de ejemplo
    print("\n7️⃣ POBLANDO CON DATOS DE EJEMPLO...")
    
    try:
        poblar_datos_postgresql()
        print("   ✅ Datos de ejemplo creados")
    except (ImportError, ValueError, TypeError, OSError) as e:
        print(f"   ❌ Error poblando datos: {e}")
        return False
    
    print("\n🎉 POSTGRESQL CONFIGURADO EXITOSAMENTE!")
    print("=" * 60)
    print("✅ PostgreSQL ejecutándose en Docker")
    print("✅ Base de datos creada y poblada")
    print("✅ Estructura optimizada para producción")
    
    print("\n🔗 ACCESOS:")
    print("   🖥️  Aplicación: http://localhost:5000")
    print("   🗄️  Adminer: http://localhost:8080")
    print("   📊 pgAdmin: http://localhost:5050 (opcional)")
    
    print("\n📋 CREDENCIALES:")
    print("   DB Host: localhost:5432")
    print("   Database: turismo_esperanza")
    print("   User: admin_turismo")
    print("   Password: TurismoEsperanza2024!")
    
    print("\n🚀 PARA EJECUTAR LA APLICACIÓN:")
    print("   python app.py")
    
    return True

def poblar_datos_postgresql():
    """Puebla la base de datos PostgreSQL con datos de ejemplo"""
    
    from app import app, db, EmpresaTuristica, SolicitudVisita, Usuario
    from datetime import date, time as dt_time
    
    with app.app_context():
        # Limpiar datos existentes
        db.session.query(SolicitudVisita).delete()
        db.session.query(EmpresaTuristica).delete()
        db.session.query(Usuario).delete()
        
        # EMPRESAS DE TURISMO DE IDENTIDAD (para instituciones locales)
        empresas_identidad = [
            EmpresaTuristica(
                nombre='Museo Histórico de la Colonización Esperanza',
                correo='educacion@museoesperanza.gov.ar',
                telefono='+54 3496 421100',
                direccion='Plaza San Martín 150, Esperanza, Santa Fe',
                servicios_ofrecidos='Visitas guiadas especializadas, talleres de historia local, exhibiciones interactivas, archivo histórico',
                descripcion='Principal museo de la ciudad dedicado a preservar y difundir la historia de la colonización suiza',
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
                servicios_ofrecidos='Talleres artísticos, exposiciones temporales, actividades culturales, biblioteca',
                descripcion='Centro neurálgico de la actividad cultural esperancense en histórica casa colonial',
                categoria_turismo='identidad',
                nivel_educativo_objetivo='Primario',
                capacidad_maxima=45,
                horarios_atencion='Lunes a Viernes 8:00-18:00, Sábados 9:00-13:00',
                costo_por_persona=200.00,
                requiere_reserva=True,
                activa=True
            ),
            EmpresaTuristica(
                nombre='Cooperativa Agrícola de Esperanza Ltda',
                correo='educativo@coopagriesperanza.com.ar',
                telefono='+54 3496 421300',
                direccion='Ruta Provincial 6 Km 12, Esperanza, Santa Fe',
                servicios_ofrecidos='Recorrido por instalaciones, charlas cooperativismo, proceso productivo, degustación',
                descripcion='Cooperativa centenaria modelo de la región, pionera en actividad agropecuaria cooperativa',
                categoria_turismo='identidad',
                nivel_educativo_objetivo='Secundario',
                capacidad_maxima=40,
                horarios_atencion='Lunes a Viernes 9:00-16:00',
                costo_por_persona=450.00,
                requiere_reserva=True,
                activa=True
            )
        ]
        
        # EMPRESAS DE TURISMO EDUCATIVO (para instituciones externas)
        empresas_educativo = [
            EmpresaTuristica(
                nombre='Complejo Educativo Rural La Esperanza',
                correo='educacion@laesperanza.edu.ar',
                telefono='+54 342 4561000',
                direccion='Ruta 11 Km 448, Santa Fe Capital',
                servicios_ofrecidos='Granja educativa, huerta orgánica, elaboración artesanal, contacto con animales',
                descripcion='Centro educativo rural integral que ofrece experiencias de vida en el campo',
                categoria_turismo='educativo',
                nivel_educativo_objetivo='Primario',
                capacidad_maxima=120,
                horarios_atencion='Lunes a Viernes 8:00-17:00',
                costo_por_persona=850.00,
                requiere_reserva=True,
                activa=True
            ),
            EmpresaTuristica(
                nombre='Acuario del Río Paraná',
                correo='educacion@acuarioparana.org.ar',
                telefono='+54 342 4567890',
                direccion='Costanera Este 1200, Santa Fe Capital',
                servicios_ofrecidos='Recorrido especializado, charlas científicas, laboratorio interactivo, observación',
                descripcion='Principal centro de interpretación de la fauna ictícola del río Paraná',
                categoria_turismo='educativo',
                nivel_educativo_objetivo='Ambos',
                capacidad_maxima=150,
                horarios_atencion='Martes a Domingo 9:00-18:00',
                costo_por_persona=750.00,
                requiere_reserva=True,
                activa=True
            ),
            EmpresaTuristica(
                nombre='Planetario Municipal Dr. Carlos Varsavsky',
                correo='reservas@planetariosf.gov.ar',
                telefono='+54 342 4570123',
                direccion='Parque Federal 2500, Santa Fe Capital',
                servicios_ofrecidos='Funciones inmersivas, observatorio astronómico, talleres científicos, laboratorio espacial',
                descripcion='Moderno planetario con tecnología de última generación para educación astronómica',
                categoria_turismo='educativo',
                nivel_educativo_objetivo='Secundario',
                capacidad_maxima=180,
                horarios_atencion='Miércoles a Domingo 14:00-21:00',
                costo_por_persona=950.00,
                requiere_reserva=True,
                activa=True
            )
        ]
        
        # Agregar empresas
        for empresa in empresas_identidad + empresas_educativo:
            db.session.add(empresa)
        
        # USUARIOS DEL SISTEMA
        usuarios = [
            Usuario(
                username='admin_turismo',
                email='admin@turismo.esperanza.gov.ar',
                password_hash='$2b$12$hash_seguro_admin',
                nombre_completo='Director de Turismo',
                rol='admin',
                activo=True
            ),
            Usuario(
                username='operador1',
                email='operador1@turismo.esperanza.gov.ar',
                password_hash='$2b$12$hash_seguro_op1',
                nombre_completo='María García - Operadora',
                rol='operador',
                activo=True
            )
        ]
        
        for usuario in usuarios:
            db.session.add(usuario)
        
        # SOLICITUDES DE EJEMPLO
        solicitudes = [
            SolicitudVisita(
                nombre_institucion='Escuela Primaria N° 1255 Domingo F. Sarmiento',
                localidad='Esperanza, Santa Fe',
                tipo_institucion='local',
                es_de_esperanza=True,
                director='Prof. Ana María Fernández',
                correo_institucional='direccion@ep1255esperanza.edu.ar',
                telefono_institucion='+54 3496 421555',
                contacto_principal='Lic. Roberto Martínez',
                telefono_contacto_principal='+54 3496 421556',
                relacion_contacto='Coordinador Pedagógico',
                nivel_educativo='Primario',
                cantidad_alumnos=28,
                edad_alumnos='8 a 10 años',
                discapacidad='No',
                empresas_seleccionadas='Museo Histórico de la Colonización Esperanza,Centro Cultural Municipal Casa Diefenbach',
                fecha_visita=date(2025, 9, 15),
                hora_grupo1=dt_time(9, 0),
                hora_grupo2=dt_time(14, 0),
                observaciones='Grupo interesado en historia local. Requieren actividades interactivas.',
                estado='Confirmada'
            ),
            SolicitudVisita(
                nombre_institucion='Instituto Técnico San José - Rafaela',
                localidad='Rafaela, Santa Fe',
                tipo_institucion='externa',
                es_de_esperanza=False,
                director='Ing. Pedro González',
                correo_institucional='direccion@itsanjose.edu.ar',
                telefono_institucion='+54 3492 432100',
                contacto_principal='Prof. Silvia Castro',
                telefono_contacto_principal='+54 3492 432101',
                relacion_contacto='Coordinadora de Visitas',
                nivel_educativo='Secundario',
                cantidad_alumnos=35,
                edad_alumnos='15 a 17 años',
                discapacidad='No',
                empresas_seleccionadas='Planetario Municipal Dr. Carlos Varsavsky,Acuario del Río Paraná',
                fecha_visita=date(2025, 10, 8),
                hora_grupo1=dt_time(10, 0),
                observaciones='Estudiantes de especialidad técnica. Interés en ciencias.',
                estado='Pendiente'
            )
        ]
        
        for solicitud in solicitudes:
            db.session.add(solicitud)
        
        # Confirmar cambios
        db.session.commit()
        
        print(f"   ✅ {len(empresas_identidad + empresas_educativo)} empresas creadas")
        print(f"   ✅ {len(usuarios)} usuarios creados") 
        print(f"   ✅ {len(solicitudes)} solicitudes de ejemplo creadas")

def mostrar_comandos_utiles():
    """Muestra comandos útiles para Docker"""
    
    print("\n📋 COMANDOS ÚTILES DE DOCKER:")
    print("   docker compose up -d          # Iniciar todos los servicios")
    print("   docker compose down           # Parar todos los servicios")
    print("   docker compose logs postgres  # Ver logs de PostgreSQL")
    print("   docker compose restart        # Reiniciar servicios")
    print("   docker compose ps             # Ver estado de contenedores")
    
    print("\n🔧 COMANDOS DE MANTENIMIENTO:")
    print("   docker volume prune           # Limpiar volúmenes no usados")
    print("   docker system prune           # Limpiar sistema Docker")

if __name__ == "__main__":
    if configurar_postgresql():
        mostrar_comandos_utiles()
    else:
        print("\n❌ La configuración falló. Revisa los errores anteriores.")
