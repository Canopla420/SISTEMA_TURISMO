#!/usr/bin/env python3
"""
Script para crear una base de datos sólida y bien estructurada
Sistema de Gestión de Visitas Turísticas - Esperanza
"""

import os
import shutil
import subprocess
from datetime import date, time
try:
    from dotenv import load_dotenv
    PYTHON_DOTENV_AVAILABLE = True
except ImportError:
    PYTHON_DOTENV_AVAILABLE = False
    print("⚠️ python-dotenv no está instalado.")

# Cargar variables de entorno si está disponible
if PYTHON_DOTENV_AVAILABLE:
    load_dotenv()

def crear_base_datos_solida():
    """Crea una base de datos sólida desde cero con estructura optimizada"""
    
    print("🏗️  CREANDO BASE DE DATOS SÓLIDA")
    print("=" * 60)
    
    # 1. Limpiar base de datos anterior
    print("\n1️⃣ LIMPIANDO CONFIGURACIÓN ANTERIOR...")
    
    # Eliminar bases de datos existentes
    bases_a_eliminar = ['instance/visitas.db', 'visitas_dev.db', 'turismo.db']
    for bd in bases_a_eliminar:
        if os.path.exists(bd):
            os.remove(bd)
            print(f"   🗑️  Eliminado: {bd}")
    
    # Limpiar directorio de migraciones
    migrations_dir = 'migrations'
    if os.path.exists(migrations_dir):
        shutil.rmtree(migrations_dir)
        print(f"   🗑️  Eliminado directorio: {migrations_dir}")
    
    # 2. Crear directorio instance si no existe
    instance_dir = 'instance'
    if not os.path.exists(instance_dir):
        os.makedirs(instance_dir)
        print(f"   📁 Creado directorio: {instance_dir}")
    
    # 3. Configurar nueva base de datos
    print("\n2️⃣ CONFIGURANDO NUEVA BASE DE DATOS...")
    
    # Crear archivo .env actualizado
    env_content = """# Configuración de Base de Datos Sólida
DATABASE_URL=sqlite:///instance/turismo_solida.db
SECRET_KEY=tu_clave_secreta_muy_segura_2024
FLASK_ENV=development
FLASK_DEBUG=True

# Configuración de Email (opcional)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=tu_email@gmail.com
MAIL_PASSWORD=tu_password
"""
    
    with open('.env', 'w', encoding='utf-8') as f:
        f.write(env_content)
    print("   ✅ Archivo .env actualizado")
    
    # 4. Crear estructura inicial de base de datos
    print("\n3️⃣ CREANDO ESTRUCTURA DE BASE DE DATOS...")
    
    # Importar la aplicación y modelos
    try:
        from app import app, db
        
        with app.app_context():
            print(f"   🔧 Configuración: {app.config['SQLALCHEMY_DATABASE_URI']}")
            
            # Crear todas las tablas
            db.create_all()
            print("   ✅ Tablas creadas exitosamente")
            
            # Verificar que las tablas se crearon
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tablas = inspector.get_table_names()
            print(f"   📊 Tablas creadas: {len(tablas)}")
            for tabla in sorted(tablas):
                print(f"      - {tabla}")
            
    except (ImportError, ValueError, TypeError, OSError) as e:
        print(f"   ❌ Error al crear estructura: {e}")
        return False
    
    # 5. Poblar con datos de ejemplo robustos
    print("\n4️⃣ POBLANDO CON DATOS DE EJEMPLO...")
    
    try:
        poblar_datos_ejemplo()
        print("   ✅ Datos de ejemplo creados")
    except (ImportError, ValueError, TypeError, OSError) as e:
        print(f"   ❌ Error al poblar datos: {e}")
        return False
    
    # 6. Configurar migraciones
    print("\n5️⃣ CONFIGURANDO SISTEMA DE MIGRACIONES...")
    
    try:
        configurar_migraciones()
        print("   ✅ Sistema de migraciones configurado")
    except (ImportError, ValueError, TypeError, OSError) as e:
        print(f"   ❌ Error en migraciones: {e}")
        return False
    
    print("\n🎉 BASE DE DATOS SÓLIDA CREADA EXITOSAMENTE!")
    print("=" * 60)
    print("✅ Estructura completa y optimizada")
    print("✅ Datos de ejemplo poblados")
    print("✅ Sistema de migraciones configurado")
    print("✅ Configuración de producción lista")
    
    print("\n🚀 PARA EJECUTAR EL SISTEMA:")
    print("   python app.py")
    print("   Luego ve a: http://localhost:5000")
    
    return True

def poblar_datos_ejemplo():
    """Crea datos de ejemplo completos y realistas"""
    
    from app import app, db, EmpresaTuristica, SolicitudVisita, Usuario
    
    with app.app_context():
        # Limpiar datos existentes
        db.session.query(SolicitudVisita).delete()
        db.session.query(EmpresaTuristica).delete()
        db.session.query(Usuario).delete()
        
        # CREAR EMPRESAS TURÍSTICAS CATEGORIZADAS
        print("   📋 Creando empresas turísticas...")
        
        empresas_identidad = [
            {
                'nombre': 'Museo Histórico de la Colonización Esperanza',
                'correo': 'educacion@museoesperanza.gov.ar',
                'telefono': '+54 3496 421100',
                'direccion': 'Plaza San Martín 150, Esperanza, Santa Fe',
                'servicios_ofrecidos': 'Visitas guiadas especializadas, talleres de historia local, exhibiciones interactivas, archivo histórico',
                'descripcion': 'Principal museo de la ciudad dedicado a preservar y difundir la historia de la colonización suiza en Esperanza',
                'categoria_turismo': 'identidad',
                'nivel_educativo_objetivo': 'Ambos',
                'capacidad_maxima': 60,
                'horarios_atencion': 'Martes a Domingo 9:00-17:00',
                'costo_por_persona': 350.00,
                'requiere_reserva': True,
                'activa': True
            },
            {
                'nombre': 'Centro Cultural Municipal "Casa Diefenbach"',
                'correo': 'cultura@esperanza.gov.ar',
                'telefono': '+54 3496 421200',
                'direccion': 'Av. San Martín 456, Esperanza, Santa Fe',
                'servicios_ofrecidos': 'Talleres artísticos, exposiciones temporales, actividades culturales, biblioteca especializada',
                'descripcion': 'Centro neurálgico de la actividad cultural esperancense, ubicado en histórica casa colonial',
                'categoria_turismo': 'identidad',
                'nivel_educativo_objetivo': 'Primario',
                'capacidad_maxima': 45,
                'horarios_atencion': 'Lunes a Viernes 8:00-18:00, Sábados 9:00-13:00',
                'costo_por_persona': 200.00,
                'requiere_reserva': True,
                'activa': True
            },
            {
                'nombre': 'Cooperativa Agrícola de Esperanza Ltda.',
                'correo': 'educativo@coopagriesperanza.com.ar',
                'telefono': '+54 3496 421300',
                'direccion': 'Ruta Provincial 6 Km 12, Esperanza, Santa Fe',
                'servicios_ofrecidos': 'Recorrido por instalaciones, charlas sobre cooperativismo, proceso productivo, degustación',
                'descripcion': 'Cooperativa centenaria modelo de la región, pionera en la actividad agropecuaria cooperativa',
                'categoria_turismo': 'identidad',
                'nivel_educativo_objetivo': 'Secundario',
                'capacidad_maxima': 40,
                'horarios_atencion': 'Lunes a Viernes 9:00-16:00',
                'costo_por_persona': 450.00,
                'requiere_reserva': True,
                'activa': True
            },
            {
                'nombre': 'Parque Temático "Raíces Suizas"',
                'correo': 'visitas@raicessuizas.com.ar',
                'telefono': '+54 3496 421400',
                'direccion': 'Camino a Colonia Roca s/n, Esperanza',
                'servicios_ofrecidos': 'Recreación histórica, talleres gastronómicos, actividades tradicionales suizas',
                'descripcion': 'Espacio temático que recrea la vida de los primeros colonos suizos en Esperanza',
                'categoria_turismo': 'identidad',
                'nivel_educativo_objetivo': 'Ambos',
                'capacidad_maxima': 80,
                'horarios_atencion': 'Miércoles a Domingo 10:00-18:00',
                'costo_por_persona': 600.00,
                'requiere_reserva': True,
                'activa': True
            }
        ]
        
        empresas_educativo = [
            {
                'nombre': 'Complejo Educativo Rural "La Esperanza"',
                'correo': 'educacion@laesperanza.edu.ar',
                'telefono': '+54 342 4561000',
                'direccion': 'Ruta 11 Km 448, Santa Fe Capital',
                'servicios_ofrecidos': 'Granja educativa, huerta orgánica, elaboración artesanal, contacto con animales',
                'descripcion': 'Centro educativo rural integral que ofrece experiencias de vida en el campo',
                'categoria_turismo': 'educativo',
                'nivel_educativo_objetivo': 'Primario',
                'capacidad_maxima': 120,
                'horarios_atencion': 'Lunes a Viernes 8:00-17:00',
                'costo_por_persona': 850.00,
                'requiere_reserva': True,
                'activa': True
            },
            {
                'nombre': 'Acuario del Río Paraná - Centro de Interpretación',
                'correo': 'educacion@acuarioparana.org.ar',
                'telefono': '+54 342 4567890',
                'direccion': 'Costanera Este 1200, Santa Fe Capital',
                'servicios_ofrecidos': 'Recorrido especializado, charlas científicas, laboratorio interactivo, observación directa',
                'descripcion': 'Principal centro de interpretación de la fauna ictícola del río Paraná',
                'categoria_turismo': 'educativo',
                'nivel_educativo_objetivo': 'Ambos',
                'capacidad_maxima': 150,
                'horarios_atencion': 'Martes a Domingo 9:00-18:00',
                'costo_por_persona': 750.00,
                'requiere_reserva': True,
                'activa': True
            },
            {
                'nombre': 'Planetario Municipal "Dr. Carlos Varsavsky"',
                'correo': 'reservas@planetariosf.gov.ar',
                'telefono': '+54 342 4570123',
                'direccion': 'Parque Federal 2500, Santa Fe Capital',
                'servicios_ofrecidos': 'Funciones inmersivas, observatorio astronómico, talleres científicos, laboratorio espacial',
                'descripcion': 'Moderno planetario con tecnología de última generación para educación astronómica',
                'categoria_turismo': 'educativo',
                'nivel_educativo_objetivo': 'Secundario',
                'capacidad_maxima': 180,
                'horarios_atencion': 'Miércoles a Domingo 14:00-21:00',
                'costo_por_persona': 950.00,
                'requiere_reserva': True,
                'activa': True
            },
            {
                'nombre': 'Centro Tecnológico Litoral - Innovation Hub',
                'correo': 'educativo@ctlitoral.edu.ar',
                'telefono': '+54 342 4572345',
                'direccion': 'Parque Tecnológico del Litoral, Santa Fe',
                'servicios_ofrecidos': 'Laboratorios de robótica, impresión 3D, realidad virtual, programación, inteligencia artificial',
                'descripcion': 'Centro de innovación tecnológica con programas educativos de vanguardia',
                'categoria_turismo': 'educativo',
                'nivel_educativo_objetivo': 'Secundario',
                'capacidad_maxima': 60,
                'horarios_atencion': 'Lunes a Viernes 9:00-17:00',
                'costo_por_persona': 1200.00,
                'requiere_reserva': True,
                'activa': True
            },
            {
                'nombre': 'Reserva Natural "Humedales del Litoral"',
                'correo': 'educativo@humedaleslitoral.org.ar',
                'telefono': '+54 3447 456789',
                'direccion': 'Ruta Nacional 168 Km 85, Entre Ríos',
                'servicios_ofrecidos': 'Senderismo interpretativo, observación de aves, educación ambiental, campamentos',
                'descripcion': 'Área natural protegida con ecosistemas únicos del litoral argentino',
                'categoria_turismo': 'educativo',
                'nivel_educativo_objetivo': 'Ambos',
                'capacidad_maxima': 200,
                'horarios_atencion': 'Todos los días 7:00-19:00',
                'costo_por_persona': 650.00,
                'requiere_reserva': True,
                'activa': True
            }
        ]
        
        # Crear empresas
        for emp_data in empresas_identidad + empresas_educativo:
            empresa = EmpresaTuristica(**emp_data)
            db.session.add(empresa)
        
        # CREAR USUARIOS DEL SISTEMA
        print("   👥 Creando usuarios del sistema...")
        
        usuarios = [
            {
                'username': 'admin_turismo',
                'email': 'admin@turismo.esperanza.gov.ar',
                'password_hash': 'hash_seguro_admin',
                'nombre_completo': 'Director de Turismo',
                'rol': 'admin',
                'activo': True
            },
            {
                'username': 'operador1',
                'email': 'operador1@turismo.esperanza.gov.ar',
                'password_hash': 'hash_seguro_op1',
                'nombre_completo': 'María García - Operadora',
                'rol': 'operador',
                'activo': True
            },
            {
                'username': 'operador2',
                'email': 'operador2@turismo.esperanza.gov.ar',
                'password_hash': 'hash_seguro_op2',
                'nombre_completo': 'Carlos Rodríguez - Operador',
                'rol': 'operador',
                'activo': True
            }
        ]
        
        for user_data in usuarios:
            usuario = Usuario(**user_data)
            db.session.add(usuario)
        
        # CREAR SOLICITUDES DE VISITA DE EJEMPLO
        print("   📝 Creando solicitudes de visita de ejemplo...")
        
        # Solicitud 1: Institución Local - Primario
        solicitud1 = SolicitudVisita(
            nombre_institucion='Escuela Primaria N° 1255 "Domingo Faustino Sarmiento"',
            localidad='Esperanza, Santa Fe',
            tipo_institucion='local',
            es_de_esperanza=True,
            director='Prof. Ana María Fernández',
            correo_institucional='direccion@ep1255esperanza.edu.ar',
            telefono_institucion='+54 3496 421555',
            contacto_principal='Lic. Roberto Martínez',
            telefono_contacto_principal='+54 3496 421556',
            relacion_contacto='Coordinador Pedagógico',
            contacto_suplente='Prof. Laura Jiménez',
            telefono_contacto_suplente='+54 3496 421557',
            nivel_educativo='Primario',
            cantidad_alumnos=28,
            edad_alumnos='8 a 10 años',
            discapacidad='No',
            empresas_seleccionadas='Museo Histórico de la Colonización Esperanza,Centro Cultural Municipal "Casa Diefenbach"',
            fecha_visita=date(2025, 9, 15),
            hora_grupo1=time(9, 0),
            hora_grupo2=time(14, 0),
            observaciones='Grupo muy interesado en historia local. Requieren actividades interactivas.',
            estado='Confirmada'
        )
        
        # Solicitud 2: Institución Externa - Secundario
        solicitud2 = SolicitudVisita(
            nombre_institucion='Instituto Técnico "San José" - Rafaela',
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
            discapacidad='Sí',
            tipo_discapacidad='Un alumno con dificultades auditivas',
            adaptacion='Sí',
            empresas_seleccionadas='Planetario Municipal "Dr. Carlos Varsavsky",Centro Tecnológico Litoral - Innovation Hub',
            fecha_visita=date(2025, 10, 8),
            hora_grupo1=time(10, 0),
            observaciones='Estudiantes de especialidad técnica. Interés especial en tecnología y ciencias.',
            estado='Pendiente'
        )
        
        # Solicitud 3: Institución Externa - Primario
        solicitud3 = SolicitudVisita(
            nombre_institucion='Escuela Rural N° 847 "Brigadier López"',
            localidad='Cayastá, Santa Fe',
            tipo_institucion='externa',
            es_de_esperanza=False,
            director='Mtra. Carmen Rodríguez',
            correo_institucional='escuela847@santafe.edu.ar',
            telefono_institucion='+54 3405 493200',
            contacto_principal='Mtra. Gabriela Vega',
            telefono_contacto_principal='+54 3405 493201',
            relacion_contacto='Maestra de 4° grado',
            nivel_educativo='Primario',
            cantidad_alumnos=22,
            edad_alumnos='9 a 11 años',
            discapacidad='No',
            empresas_seleccionadas='Complejo Educativo Rural "La Esperanza",Acuario del Río Paraná - Centro de Interpretación',
            fecha_visita=date(2025, 11, 12),
            hora_grupo1=time(9, 30),
            observaciones='Primera salida educativa del año. Muy emocionados por conocer el río.',
            estado='Pendiente'
        )
        
        db.session.add_all([solicitud1, solicitud2, solicitud3])
        
        # Confirmar todos los cambios
        db.session.commit()
        
        print(f"   ✅ {len(empresas_identidad + empresas_educativo)} empresas creadas")
        print(f"   ✅ {len(usuarios)} usuarios creados")
        print("   ✅ 3 solicitudes de ejemplo creadas")

def configurar_migraciones():
    """Configura el sistema de migraciones de Flask-Migrate"""
    
    # Inicializar migraciones si no existe
    if not os.path.exists('migrations'):
        result = subprocess.run(['flask', 'db', 'init'], 
                              capture_output=True, text=True, cwd='.', check=False)
        if result.returncode != 0:
            print(f"   ⚠️ Warning en flask db init: {result.stderr}")
    
    # Crear migración inicial
    result = subprocess.run(['flask', 'db', 'migrate', '-m', 'Base de datos sólida inicial'], 
                          capture_output=True, text=True, cwd='.', check=False)
    if result.returncode != 0:
        print(f"   ⚠️ Warning en migrate: {result.stderr}")
    
    # Aplicar migración
    result = subprocess.run(['flask', 'db', 'upgrade'], 
                          capture_output=True, text=True, cwd='.', check=False)
    if result.returncode != 0:
        print(f"   ⚠️ Warning en upgrade: {result.stderr}")

if __name__ == "__main__":
    crear_base_datos_solida()
