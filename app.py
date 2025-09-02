#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Forzar UTF-8 y locale en Windows
import sys
import os
if sys.platform.startswith('win'):
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    os.environ['LC_ALL'] = 'es_AR.UTF-8'
    os.environ['LANG'] = 'es_AR.UTF-8'

from flask import Flask, request, jsonify, render_template, redirect, url_for, send_file
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
import io
from datetime import datetime
from reportlab.lib.pagesizes import letter
import os

app = Flask(__name__)

# Configuración simple y directa
app.config['SECRET_KEY'] = 'clave-super-secreta-para-desarrollo-2024'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///turismo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = True

# Configuración de correo
# Para activar el envío real de correos, completa estos datos:
MAIL_USERNAME = "canoezequiel7802@gmail.com"  # Tu Gmail real
MAIL_PASSWORD = "adgj kgvv raua hcxl"   # Contraseña de aplicación (16 caracteres)

# Configuración automática
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = MAIL_USERNAME
app.config['MAIL_PASSWORD'] = MAIL_PASSWORD
app.config['MAIL_DEFAULT_SENDER'] = MAIL_USERNAME

# Si las credenciales son válidas, habilitamos el envío real
MAIL_ENABLED = MAIL_USERNAME != "tu_gmail_personal@gmail.com" and MAIL_PASSWORD != "tu_password_de_aplicacion"

db = SQLAlchemy(app)
mail = Mail(app)

migrate = Migrate(app, db)
# ------------------------------
# Definición de los modelos
# ------------------------------

class Usuario(db.Model):
    __tablename__ = 'usuario'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    rol = db.Column(db.String(50), nullable=False, default='Usuario')
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)

class SolicitudVisita(db.Model):
    __tablename__ = 'solicitud_visita'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre_institucion = db.Column(db.String(200), nullable=False)
    responsable = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    cantidad_alumnos = db.Column(db.Integer, nullable=False)
    edad_alumnos = db.Column(db.String(50), nullable=True)
    discapacidad = db.Column(db.String(10), default='No')
    empresas_seleccionadas = db.Column(db.Text, nullable=True)
    fecha_visita = db.Column(db.Date, nullable=True)
    hora_grupo1 = db.Column(db.Time, nullable=True)
    hora_grupo2 = db.Column(db.Time, nullable=True)
    observaciones = db.Column(db.Text, nullable=True)
    estado = db.Column(db.String(50), default='Pendiente')
    fecha_solicitud = db.Column(db.DateTime, default=datetime.utcnow)

class EmpresaTuristica(db.Model):
    __tablename__ = 'empresa_turistica'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200), nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    direccion = db.Column(db.String(200), nullable=True)
    telefono = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(120), nullable=True)
    categoria = db.Column(db.String(50), nullable=False)
    capacidad_maxima = db.Column(db.Integer, nullable=True)
    duracion_visita = db.Column(db.String(50), nullable=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)

class ConsultaEmpresa(db.Model):
    __tablename__ = 'consulta_empresa'
    
    id = db.Column(db.Integer, primary_key=True)
    empresa_id = db.Column(db.Integer, db.ForeignKey('empresa_turistica.id'), nullable=False)
    fecha_consulta = db.Column(db.Date, nullable=False)
    hora_consulta = db.Column(db.Time, nullable=False)
    comentarios = db.Column(db.Text, nullable=True)
    estado = db.Column(db.String(20), default='Pendiente')  # Pendiente, Confirmada, Rechazada
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relación con empresa
    empresa = db.relationship('EmpresaTuristica', backref='consultas')

# Comentado temporalmente para evitar errores
# class VisitaRealizada(db.Model):
#     __tablename__ = 'visitas_realizadas'
#     __tablename__ = 'consultas_empresas'
# 
# class Itinerario(db.Model):
#     __tablename__ = 'itinerarios'

# ------------------------------
# Configuración de migraciones
# ------------------------------
migrate = Migrate(app, db)

# Nota: Para crear las tablas, usar los comandos:
# flask db init (solo la primera vez)
# flask db migrate -m "Crear tablas iniciales"
# flask db upgrade

# Configuración de Flask-Mail
mail = Mail(app)

# ------------------------------
# Rutas principales
# ------------------------------

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/diagnostico')
def diagnostico():
    """Ruta para diagnosticar el estado de la base de datos"""
    try:
        # Verificar conexión
        result = db.session.execute(db.text("SELECT 1"))
        conexion_ok = True
        
        # Contar registros
        empresas_count = db.session.execute(db.text("SELECT COUNT(*) FROM empresa_turistica")).scalar()
        solicitudes_count = db.session.execute(db.text("SELECT COUNT(*) FROM solicitud_visita")).scalar()
        usuarios_count = db.session.execute(db.text("SELECT COUNT(*) FROM usuario")).scalar()
        
        # Obtener algunas empresas
        empresas_result = db.session.execute(db.text("SELECT nombre FROM empresa_turistica LIMIT 3"))
        empresas_nombres = [row[0] for row in empresas_result]
        
        diagnostico_info = f"""
        🔍 DIAGNÓSTICO DE BASE DE DATOS
        ================================
        ✅ Conexión: {'OK' if conexion_ok else 'ERROR'}
        
        📊 CONTADORES:
        - Empresas: {empresas_count}
        - Solicitudes: {solicitudes_count}  
        - Usuarios: {usuarios_count}
        
        📝 EMPRESAS ENCONTRADAS:
        {chr(10).join(['- ' + nombre for nombre in empresas_nombres]) if empresas_nombres else 'Ninguna'}
        
        🔧 ACCIONES:
        - <a href="/cargar_datos_iniciales">Cargar datos iniciales</a>
        - <a href="/gestionar_empresas">Ver gestión de empresas</a>
        - <a href="/">Volver al inicio</a>
        """
        
        return f"<pre>{diagnostico_info}</pre>"
        
    except Exception as e:
        return f"❌ Error en diagnóstico: {e}"

@app.route('/cargar_datos_iniciales')
def cargar_datos_iniciales():
    """Ruta especial para cargar datos iniciales en la base de datos"""
    try:
        # Verificar si ya hay datos
        empresas_count = EmpresaTuristica.query.count()
        if empresas_count > 0:
            return f"✅ Ya hay {empresas_count} empresas en la base de datos. No es necesario cargar datos."
        empresas_data = [
            {
                'nombre': 'Museo Historico',
                'descripcion': 'Museo que preserva la historia local',
                'direccion': 'Av. San Martin 402',
                'telefono': '03496-420789',
                'email': 'museo@esperanza.gov.ar',
                'categoria': 'Turismo de Identidad',
                'capacidad_maxima': 40,
                'duracion_visita': '90 minutos'
            },
            {
                'nombre': 'Centro Cultural Casa Diefenbach',
                'descripcion': 'Centro cultural en edificio historico',
                'direccion': 'Calle 25 de Mayo 356',
                'telefono': '03496-420123',
                'email': 'cultura@esperanza.gov.ar',
                'categoria': 'Turismo de Identidad',
                'capacidad_maxima': 60,
                'duracion_visita': '75 minutos'
            },
            {
                'nombre': 'Iglesia San Pedro',
                'descripcion': 'Primera iglesia de la colonia suiza',
                'direccion': 'Plaza San Martin',
                'telefono': '03496-420456',
                'email': 'sanpedro@esperanza.gov.ar',
                'categoria': 'Turismo de Identidad',
                'capacidad_maxima': 80,
                'duracion_visita': '60 minutos'
            }
        ]
        
        # Insertar empresas
        for empresa_data in empresas_data:
            empresa = EmpresaTuristica(**empresa_data)
            db.session.add(empresa)
        
        # Crear solicitud de ejemplo
        solicitud = SolicitudVisita(
            nombre_institucion='Escuela Primaria Nacional Esperanza',
            responsable='María González',
            telefono='(03496) 420-999',
            email='direccion@escuelaesperanza.edu.ar',
            cantidad_alumnos=25,
            edad_alumnos='8 a 10 años',
            discapacidad='No',
            empresas_seleccionadas='Museo Histórico de la Colonización Esperanza,Centro Cultural Municipal Casa Diefenbach',
            observaciones='Grupo interesado en historia local.',
            estado='Confirmada'
        )
        db.session.add(solicitud)
        
        # Guardar cambios
        db.session.commit()
        
        return "✅ ¡Datos cargados exitosamente! Ahora puedes ver las empresas y visitas en la aplicación."
        
    except Exception as e:
        db.session.rollback()
        return f"❌ Error cargando datos: {e}"

@app.route('/institucion/solicitar_visita', methods=['GET', 'POST'])
def solicitar_visita_institucion():
    """Formulario público para que las instituciones soliciten una visita"""
    if request.method == 'POST':
        # Convertir fecha de string a date
        fecha_str = request.form.get('fecha_visita')
        fecha_visita = datetime.strptime(fecha_str, '%Y-%m-%d').date() if fecha_str else None
        
        # Convertir horas de string a time
        hora1_str = request.form.get('hora_grupo1')
        hora2_str = request.form.get('hora_grupo2')
        
        # Función auxiliar para convertir hora
        def convertir_hora(hora_str):
            if not hora_str:
                return None
            try:
                # Intentar primero con formato HH:MM:SS
                return datetime.strptime(hora_str, '%H:%M:%S').time()
            except ValueError:
                try:
                    # Si falla, intentar con formato HH:MM
                    return datetime.strptime(hora_str, '%H:%M').time()
                except ValueError:
                    return None
        
        hora_grupo1 = convertir_hora(hora1_str)
        hora_grupo2 = convertir_hora(hora2_str)
        
        # Determinar el tipo de institución basado en la localidad
        localidad = request.form.get('localidad', '').strip().lower()
        es_de_esperanza = 'esperanza' in localidad
        tipo_institucion = 'local' if es_de_esperanza else 'externa'
        
        # Obtener empresas seleccionadas
        empresas_seleccionadas_ids = request.form.getlist('empresas_seleccionadas')
        empresas_seleccionadas_str = ",".join(empresas_seleccionadas_ids)
        print(f"🔍 DEBUG: Empresas seleccionadas: {empresas_seleccionadas_str}")
        
        # Capturar los datos del formulario
        solicitud = SolicitudVisita(
            nombre_institucion=request.form.get('nombre_institucion'),
            responsable=request.form.get('contacto_principal', ''),
            telefono=request.form.get('telefono_contacto_principal', ''),
            email=request.form.get('correo_institucional', ''),
            cantidad_alumnos=int(request.form.get('cantidad_alumnos', 0)),
            edad_alumnos=request.form.get('edad_alumnos', ''),
            discapacidad=request.form.get('discapacidad', 'No'),
            empresas_seleccionadas=empresas_seleccionadas_str,
            fecha_visita=fecha_visita,
            hora_grupo1=hora_grupo1,
            hora_grupo2=hora_grupo2,
            observaciones=request.form.get('observaciones')
        )

        # Guardar en la base de datos
        try:
            db.session.add(solicitud)
            db.session.commit()
            return redirect(url_for('confirmacion_visita'))
        except (ValueError, TypeError, OSError) as e:
            db.session.rollback()
            print(f"Error al guardar solicitud: {e}")
            return "Error al procesar la solicitud", 500

    # Renderizar el formulario si es una solicitud GET
    # Obtener todas las empresas para mostrar en el formulario
    empresas = EmpresaTuristica.query.all()
    return render_template('nueva_visita.html', empresas=empresas)

@app.route('/modificar_visita/<int:visita_id>', methods=['GET', 'POST'])
def modificar_visita(visita_id):
    """Modificar una visita existente"""
    visita = SolicitudVisita.query.get_or_404(visita_id)  # Buscar la visita por ID

    if request.method == 'POST':
        try:
            # Debug: mostrar todos los datos recibidos
            print("🔍 Datos recibidos del formulario:")
            for key, value in request.form.items():
                print(f"  {key}: {value}")
            
            # Actualizar todos los datos de la visita con los valores enviados desde el formulario
            visita.nombre_institucion = request.form.get('nombre_institucion')
            visita.responsable = request.form.get('contacto_principal', '')
            visita.telefono = request.form.get('telefono_contacto_principal', '')
            visita.email = request.form.get('correo_institucional', '')
            
            # Convertir cantidad_alumnos a entero
            cantidad_str = request.form.get('cantidad_alumnos')
            visita.cantidad_alumnos = int(cantidad_str) if cantidad_str and cantidad_str.strip() else 0
            
            visita.edad_alumnos = request.form.get('edad_alumnos')
            visita.discapacidad = request.form.get('discapacidad')
            visita.empresas_seleccionadas = ",".join(request.form.getlist('lugares[]'))  # Corregido nombre de campo
            
            # Convertir fecha de string a date object
            fecha_str = request.form.get('fecha_visita')
            if fecha_str:
                visita.fecha_visita = datetime.strptime(fecha_str, '%Y-%m-%d').date()
            
            # Función auxiliar para convertir hora
            def convertir_hora(hora_str):
                if not hora_str or not hora_str.strip():
                    return None
                try:
                    # Intentar primero con formato HH:MM:SS
                    return datetime.strptime(hora_str, '%H:%M:%S').time()
                except ValueError:
                    try:
                        # Si falla, intentar con formato HH:MM
                        return datetime.strptime(hora_str, '%H:%M').time()
                    except ValueError:
                        return None
            
            # Convertir horas de string a time objects
            hora1_str = request.form.get('hora_grupo1')
            visita.hora_grupo1 = convertir_hora(hora1_str)
                
            hora2_str = request.form.get('hora_grupo2')
            visita.hora_grupo2 = convertir_hora(hora2_str)
                
            visita.observaciones = request.form.get('observaciones')

            # Guardar los cambios en la base de datos
            db.session.commit()
            return redirect(url_for('consultar_visitas'))  # Redirigir a la página de consultar visitas
            
        except (ValueError, TypeError) as e:
            db.session.rollback()
            print(f"Error al modificar visita: {e}")
            return f"Error al modificar visita: {e}", 500

    # Renderizar el formulario con los datos actuales de la visita
    return render_template('modificar_visita_nuevo.html', visita=visita)


@app.route('/confirmacion_visita', methods=['GET'])
def confirmacion_visita():
    """Página de confirmación después de enviar una solicitud"""
    return render_template('confirmacion_carga_visita.html')

@app.route('/eliminar_visita/<int:visita_id>', methods=['POST'])
def eliminar_visita(visita_id):
    """Eliminar una visita por su ID"""
    try:
        # Buscar la visita por ID
        visita = SolicitudVisita.query.get_or_404(visita_id)
        
        # Eliminar la visita
        db.session.delete(visita)
        db.session.commit()  # Confirmar los cambios en la base de datos
        
        # Redirigir a la página de consultar visitas
        return redirect(url_for('consultar_visitas'))
    except (ValueError, TypeError, OSError) as e:
        db.session.rollback()
        print(f"Error al eliminar visita: {e}")
        return redirect(url_for('consultar_visitas'))

@app.route('/nueva_visita')
def nueva_visita():
    """Formulario para registrar una nueva visita"""
    print("🔍 DEBUG: Accediendo a nueva_visita")
    try:
        # Obtener todas las empresas para mostrar en el formulario
        empresas = EmpresaTuristica.query.all()
        print(f"🔍 DEBUG: Se encontraron {len(empresas)} empresas")
        
        print("🔍 DEBUG: Intentando renderizar nueva_visita.html")
        return render_template('nueva_visita.html', empresas=empresas)
    except Exception as e:
        print(f"❌ ERROR en nueva_visita: {e}")
        return f"Error en nueva_visita: {e}", 500

@app.route('/confirmar_visita/<int:visita_id>', methods=['POST'])
def confirmar_visita(visita_id):
    """Confirmar una visita por su ID"""
    try:
        visita = SolicitudVisita.query.get_or_404(visita_id)
        visita.estado = "Confirmada"
        db.session.commit()
        return redirect(url_for('consultar_visitas'))
    except (ValueError, TypeError, OSError) as e:
        db.session.rollback()
        print(f"Error al confirmar visita: {e}")
        return redirect(url_for('consultar_visitas'))

@app.route('/rechazar_visita/<int:visita_id>', methods=['POST'])
def rechazar_visita(visita_id):
    """Rechazar una visita por su ID"""
    try:
        visita = SolicitudVisita.query.get_or_404(visita_id)
        visita.estado = "Rechazada"
        db.session.commit()
        return redirect(url_for('consultar_visitas'))
    except (ValueError, TypeError, OSError) as e:
        db.session.rollback()
        print(f"Error al rechazar visita: {e}")
        return redirect(url_for('consultar_visitas'))

@app.route('/pendiente_visita/<int:visita_id>', methods=['POST'])
def pendiente_visita(visita_id):
    """Volver una visita a estado Pendiente"""
    try:
        visita = SolicitudVisita.query.get_or_404(visita_id)
        visita.estado = "Pendiente"
        db.session.commit()
        return redirect(url_for('consultar_visitas'))
    except (ValueError, TypeError, OSError) as e:
        db.session.rollback()
        print(f"Error al cambiar visita a pendiente: {e}")
        return redirect(url_for('consultar_visitas'))

@app.route('/consultar_visitas', methods=['GET', 'POST'])
def consultar_visitas():
    """Pantalla para consultar visitas"""
    nombre_institucion = ''
    estado = ''
    
    try:
        if request.method == 'POST':
            nombre_institucion = request.form.get('nombre_institucion', '').strip()
            estado = request.form.get('estado', '').strip()
            
            # Construir la consulta con filtros
            query = SolicitudVisita.query
            
            if nombre_institucion:
                query = query.filter(SolicitudVisita.nombre_institucion.ilike(f'%{nombre_institucion}%'))
            
            if estado:
                query = query.filter(SolicitudVisita.estado == estado)
                
            visitas = query.all()
        else:
            # Obtener todas las visitas si es GET
            visitas = SolicitudVisita.query.all()
        
        return render_template('consultar_visitas.html', 
                             visitas=visitas, 
                             nombre_institucion=nombre_institucion, 
                             estado=estado)
    except (ValueError, TypeError, OSError) as e:
        print(f"Error en consultar_visitas: {e}")
        # Devolver una página con lista vacía en caso de error
        return render_template('consultar_visitas.html', 
                             visitas=[], 
                             nombre_institucion=nombre_institucion, 
                             estado=estado)


# ------------------------------
# Rutas relacionadas con empresas
# ------------------------------

@app.route('/consultar_empresas', methods=['GET'])
def consultar_empresas():
    """Pantalla para consultar empresas"""
    try:
        empresas = EmpresaTuristica.query.all()
        empresas_js = [
            {
                'id': e.id,
                'nombre': e.nombre,
                'email': e.email,
                'categoria': e.categoria
            } for e in empresas
        ]
        print(f"🔍 DEBUG: Encontradas {len(empresas)} empresas para consultar")
        return render_template('consultar_empresas.html', empresas=empresas, empresas_js=empresas_js)
    except Exception as e:
        print(f"❌ ERROR en consultar_empresas: {e}")
        return render_template('consultar_empresas.html', empresas=[])

@app.route('/todas_empresas', methods=['GET'])
def todas_empresas():
    """Devuelve la lista de empresas en formato JSON"""
    try:
        empresas = EmpresaTuristica.query.all()
        empresas_json = []
        for empresa in empresas:
            empresas_json.append({
                "id": empresa.id,
                "nombre": empresa.nombre,
                "email": empresa.email,
                "telefono": empresa.telefono,
                "direccion": empresa.direccion,
                "categoria": empresa.categoria,
                "capacidad_maxima": empresa.capacidad_maxima,
                "duracion_visita": empresa.duracion_visita
            })
        return jsonify(empresas_json)
    except (ValueError, TypeError, OSError) as e:
        print(f"Error al obtener empresas: {e}")
        return jsonify([])

@app.route('/empresas_filtradas', methods=['GET'])
def empresas_filtradas():
    """Devuelve empresas filtradas según el tipo de institución y nivel educativo"""
    try:
        # Obtener parámetros de filtrado
        es_de_esperanza = request.args.get('es_de_esperanza', 'false').lower() == 'true'
        nivel_educativo = request.args.get('nivel_educativo', '')
        
        # Determinar la categoría de turismo según el origen
        categoria_turismo = 'identidad' if es_de_esperanza else 'educativo'
        
        # Construir query base
        query = EmpresaTuristica.query.filter_by(categoria=categoria_turismo)
        
        # Filtrar por nivel educativo
        if nivel_educativo in ['Primario', 'Secundario']:
            query = query.filter(
                (EmpresaTuristica.nivel_educativo_objetivo == nivel_educativo) |
                (EmpresaTuristica.nivel_educativo_objetivo == 'Ambos')
            )
        
        empresas = query.all()
        empresas_json = []
        
        for empresa in empresas:
            empresas_json.append({
                "id": empresa.id,
                "nombre": empresa.nombre,
                "email": empresa.email,
                "telefono": empresa.telefono,
                "direccion": empresa.direccion,
                "descripcion": empresa.descripcion,
                "categoria": empresa.categoria,
                "capacidad_maxima": empresa.capacidad_maxima,
                "duracion_visita": empresa.duracion_visita
            })
        
        return jsonify(empresas_json)
    except (ValueError, TypeError, OSError) as e:
        print(f"Error al filtrar empresas: {e}")
        return jsonify([])

@app.route('/buscar_empresa')
def buscar_empresa():
    """Busca empresas por nombre (búsqueda dinámica)"""
    try:
        query = request.args.get("q", "").lower()
        empresas = EmpresaTuristica.query.filter(
            EmpresaTuristica.nombre.ilike(f'%{query}%')
        ).all()
        
        coincidencias = []
        for empresa in empresas:
            coincidencias.append({
                "id": empresa.id,
                "nombre": empresa.nombre,
                "email": empresa.email,
                "telefono": empresa.telefono
            })
        return jsonify(coincidencias)
    except (ValueError, TypeError, OSError) as e:
        print(f"Error en búsqueda de empresas: {e}")
        return jsonify([])

@app.route('/enviar_consulta', methods=['POST'])
def enviar_consulta():
    """Procesa el formulario y envía un correo a la empresa seleccionada"""
    try:
        empresa_nombre = request.form.get('empresa')
        correo = request.form.get('correo')
        fecha_str = request.form.get('fecha')
        hora_str = request.form.get('hora')
        comentarios = request.form.get('comentarios', '')

        print(f"🔍 DEBUG: Procesando consulta para empresa: {empresa_nombre}")
        print(f"🔍 DEBUG: Correo: {correo}, Fecha: {fecha_str}, Hora: {hora_str}")

        if not (empresa_nombre and correo and fecha_str and hora_str):
            return jsonify({"error": "Faltan datos obligatorios (empresa, correo, fecha y hora)"}), 400

        # Buscar la empresa en la base de datos
        empresa = EmpresaTuristica.query.filter_by(nombre=empresa_nombre).first()
        if not empresa:
            return jsonify({"error": "Empresa no encontrada"}), 404

        # Convertir fecha y hora
        try:
            fecha_consulta = datetime.strptime(fecha_str, '%Y-%m-%d').date()
            hora_consulta = datetime.strptime(hora_str, '%H:%M').time()
        except ValueError as e:
            return jsonify({"error": f"Formato de fecha u hora inválido: {e}"}), 400

        # Guardar la consulta en la base de datos
        consulta = ConsultaEmpresa(
            empresa_id=empresa.id,
            fecha_consulta=fecha_consulta,
            hora_consulta=hora_consulta,
            comentarios=comentarios
        )
        db.session.add(consulta)
        db.session.commit()

        print(f"✅ DEBUG: Consulta guardada con ID: {consulta.id}")

        # Crear y enviar el correo
        mensaje_correo = ""
        try:
            # Formatear fecha y hora para el correo
            fecha_formatted = fecha_consulta.strftime("%d/%m/%Y")
            hora_formatted = hora_consulta.strftime("%H:%M")
            
            # Crear el mensaje
            asunto = f"Consulta de disponibilidad - {fecha_formatted}"
            
            cuerpo_mensaje = f"""
<html>
    <body style="font-family: Arial, Helvetica, sans-serif; color: #222; background: #f8f9fa; margin:0; padding:0;">
        <table width="100%" cellpadding="0" cellspacing="0" style="max-width: 600px; margin: 30px auto; background: #fff; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.05);">
                    <tr>
                        <td style="padding: 24px 32px 12px 32px; border-bottom: 2px solid #005f73; background: #fff;">
                            <h2 style="margin:0; color:#005f73; font-size:1.6em; font-weight:700; letter-spacing:1px;">Municipalidad de Esperanza</h2>
                            <div style="font-size:1.15em; color:#005f73; font-weight:500; margin-top:4px;">Dirección de Turismo</div>
                        </td>
                    </tr>
            <tr>
                <td style="padding: 24px 32px;">
                    <p style="margin-top:0;">Estimados responsables de <strong>{empresa.nombre}</strong>:</p>
                    <p>Nos comunicamos para consultar la <b>disponibilidad</b> de su establecimiento para una visita institucional.</p>
                    <table style="width:100%; background:#f1f5f9; border-radius:8px; margin:18px 0; font-size:1em;">
                        <tr><td style="padding:8px;"><strong>Fecha solicitada:</strong></td><td style="padding:8px;">{fecha_formatted}</td></tr>
                        <tr><td style="padding:8px;"><strong>Hora solicitada:</strong></td><td style="padding:8px;">{hora_formatted}</td></tr>
                        <tr><td style="padding:8px;"><strong>Empresa:</strong></td><td style="padding:8px;">{empresa.nombre}</td></tr>
                        <tr><td style="padding:8px;"><strong>Comentarios:</strong></td><td style="padding:8px;">{comentarios if comentarios else 'Ninguno'}</td></tr>
                    </table>
                    <p>Por favor, confirme la disponibilidad respondiendo a este correo. Ante cualquier duda, puede comunicarse con la Dirección de Turismo.</p>
                </td>
            </tr>
            <tr>
                <td style="padding: 18px 32px; background: #f1f5f9; color: #333; border-radius: 0 0 10px 10px; font-size:0.98em;">
                    Atentamente,<br>
                    <strong>Dirección de Turismo - Municipalidad de Esperanza</strong><br>
                    Consulta ID: {consulta.id}<br>
                    Dirección: Av. Principal 123, Ciudad Turística<br>
                    Teléfono: (03456) 123456<br>
                    Email: turismo@municipalidad.gob.ar
                </td>
            </tr>
        </table>
    </body>
</html>
"""

            # Verificar si el correo está habilitado
            if MAIL_ENABLED:
                # Crear y enviar el mensaje
                print(f"🔄 DEBUG: Intentando enviar correo desde {MAIL_USERNAME} hacia {correo}")
                msg = Message(
                    subject=asunto,
                    recipients=[correo],
                    html=cuerpo_mensaje
                )
                
                # Intentar enviar el correo
                mail.send(msg)
                print(f"✅ DEBUG: Correo enviado exitosamente a {correo}")
                mensaje_correo = "✅ Correo enviado exitosamente"
            else:
                print(f"⚠️ DEBUG: Configuración de correo no disponible. Simulando envío a {correo}")
                print(f"📧 CONTENIDO DEL CORREO:\n{cuerpo_mensaje}")
                mensaje_correo = "📧 Consulta registrada (correo simulado - configurar MAIL_USERNAME y MAIL_PASSWORD para envío real)"
            
            return jsonify({
                "mensaje": "Consulta enviada exitosamente", 
                "empresa": empresa_nombre,
                "fecha": fecha_formatted,
                "hora": hora_formatted,
                "correo": correo,
                "estado_correo": mensaje_correo
            }), 200
            
        except Exception as mail_error:
            print(f"❌ ERROR al enviar correo: {mail_error}")
            # Aunque falle el correo, la consulta ya está guardada
            return jsonify({
                "mensaje": "Consulta registrada correctamente, pero hubo un problema al enviar el correo",
                "error_correo": str(mail_error),
                "empresa": empresa_nombre,
                "fecha": fecha_formatted,
                "hora": hora_formatted
            }), 200
        
    except Exception as e:
        print(f"❌ ERROR general en enviar_consulta: {e}")
        db.session.rollback()
        return jsonify({"error": f"Error interno del servidor: {str(e)}"}), 500
        
    except (ValueError, TypeError, OSError) as e:
        db.session.rollback()
        print(f"Error al procesar consulta: {e}")
        return jsonify({"error": "No se pudo procesar la consulta"}), 500

# Nuevas rutas para gestión de empresas
@app.route('/gestionar_empresas', methods=['GET'])
def gestionar_empresas():
    """Pantalla para gestionar empresas (CRUD)"""
    print("🔍 DEBUG: Accediendo a gestionar_empresas")
    try:
        print("🔍 DEBUG: Consultando empresas...")
        empresas = EmpresaTuristica.query.all()
        print(f"🔍 DEBUG: Encontradas {len(empresas)} empresas")
        print("🔍 DEBUG: Intentando renderizar gestionar_empresas.html")
        return render_template('gestionar_empresas.html', empresas=empresas)
    except Exception as e:
        print(f"❌ ERROR en gestionar_empresas: {e}")
        # Devolver una página con lista vacía en caso de error
        return f"Error en gestionar_empresas: {e}", 500

@app.route('/agregar_empresa', methods=['GET', 'POST'])
def agregar_empresa():
    """Agregar una nueva empresa"""
    if request.method == 'POST':
        try:
            # Solo tomar los campos válidos del modelo
            empresa = EmpresaTuristica(
                nombre=request.form.get('nombre'),
                descripcion=request.form.get('descripcion'),
                direccion=request.form.get('direccion'),
                telefono=request.form.get('telefono'),
                email=request.form.get('email'),
                categoria=request.form.get('categoria'),
                capacidad_maxima=int(request.form.get('capacidad_maxima', 0)) if request.form.get('capacidad_maxima') else None,
                duracion_visita=request.form.get('duracion_visita')
            )
            db.session.add(empresa)
            db.session.commit()
            return redirect(url_for('gestionar_empresas'))
        except Exception as e:
            db.session.rollback()
            import traceback
            print(f"Error al agregar empresa: {e}")
            print(traceback.format_exc())
            # Mostrar los datos recibidos para depuración
            datos = {k: v for k, v in request.form.items()}
            return f"Error al agregar empresa: {e}<br>Datos recibidos: {datos}", 500
    
    return render_template('agregar_empresa.html')

@app.route('/editar_empresa/<int:empresa_id>', methods=['GET', 'POST'])
def editar_empresa(empresa_id):
    """Editar una empresa existente"""
    empresa = EmpresaTuristica.query.get_or_404(empresa_id)
    
    if request.method == 'POST':
        try:
            costo_str = request.form.get('costo_por_persona')
            costo = float(costo_str) if costo_str and costo_str.strip() else None
            
            capacidad_str = request.form.get('capacidad_maxima')
            capacidad = int(capacidad_str) if capacidad_str and capacidad_str.strip() else None
            
            empresa.nombre = request.form.get('nombre')
            empresa.email = request.form.get('email')
            empresa.telefono = request.form.get('telefono')
            empresa.direccion = request.form.get('direccion')
            empresa.descripcion = request.form.get('descripcion')
            empresa.categoria = request.form.get('categoria')
            
            # Validar capacidad
            capacidad_str = request.form.get('capacidad_maxima', '').strip()
            capacidad = int(capacidad_str) if capacidad_str and capacidad_str.isdigit() else None
            empresa.capacidad_maxima = capacidad
            
            empresa.duracion_visita = request.form.get('duracion_visita')
            
            db.session.commit()
            return redirect(url_for('gestionar_empresas'))
        except (ValueError, TypeError, OSError) as e:
            db.session.rollback()
            print(f"Error al editar empresa: {e}")
            return "Error al editar empresa", 500
    
    return render_template('editar_empresa.html', empresa=empresa)

@app.route('/eliminar_empresa/<int:empresa_id>', methods=['POST'])
def eliminar_empresa(empresa_id):
    """Eliminar una empresa definitivamente"""
    try:
        empresa = EmpresaTuristica.query.get_or_404(empresa_id)
        db.session.delete(empresa)
        db.session.commit()
        return redirect(url_for('gestionar_empresas'))
    except (ValueError, TypeError, OSError) as e:
        db.session.rollback()
        print(f"Error al eliminar empresa: {e}")
        return redirect(url_for('gestionar_empresas'))

# ------------------------------
# Rutas relacionadas con visitas
# ------------------------------

@app.route('/crear_itinerario', methods=['GET', 'POST'])
def crear_itinerario():
    if request.method == 'POST':
        try:
            visita_id = request.form['visita_id']
            visita = SolicitudVisita.query.get(visita_id)
            if not visita:
                return "Visita no encontrada", 404


            buffer = io.BytesIO()
            p = canvas.Canvas(buffer, pagesize=letter)
            width, height = letter

            # Márgenes
            left_margin = right_margin = top_margin = bottom_margin = inch

            # --- Encabezado institucional ---
            logo_path = os.path.join('static', 'img', 'logo_esperanza.png')
            if os.path.exists(logo_path):
                p.drawImage(logo_path, left_margin, height - top_margin - 60, width=70, height=70, mask='auto')
            p.setFont("Helvetica-Bold", 18)
            p.setFillColorRGB(0.1, 0.2, 0.4)
            p.drawString(left_margin + 80, height - top_margin - 20, "Municipalidad de Esperanza")
            p.setFont("Helvetica", 13)
            p.setFillColorRGB(0.1, 0.2, 0.4)
            p.drawString(left_margin + 80, height - top_margin - 40, "Dirección de Turismo")
            p.setStrokeColorRGB(0.1, 0.2, 0.4)
            p.setLineWidth(2)
            p.line(left_margin, height - top_margin - 70, width - right_margin, height - top_margin - 70)

            # --- Título central ---
            p.setFont("Helvetica-Bold", 17)
            p.setFillColorRGB(0, 0, 0)
            p.drawCentredString(width / 2, height - top_margin - 90, "Itinerario de Visita Turística")

            # --- Datos de la visita ---
            y = height - top_margin - 130
            line_space = 22
            fecha_formateada = visita.fecha_visita.strftime('%d/%m/%Y') if visita.fecha_visita else "No especificada"
            hora1_formateada = visita.hora_grupo1.strftime('%H:%M') if visita.hora_grupo1 else "No especificada"
            hora2_formateada = visita.hora_grupo2.strftime('%H:%M') if visita.hora_grupo2 else "No especificada"


            # Obtener datos detallados de empresas
            empresas_detalle = []
            empresas_nombres = visita.empresas_seleccionadas
            # Intentar obtener por IDs
            ids = [eid.strip() for eid in empresas_nombres.split(',') if eid.strip().isdigit()]
            if ids:
                empresas = EmpresaTuristica.query.filter(EmpresaTuristica.id.in_(ids)).all()
                for e in empresas:
                    empresas_detalle.append({
                        'nombre': e.nombre,
                        'direccion': e.direccion or '-',
                        'telefono': e.telefono or '-',
                        'email': e.email or '-',
                        'categoria': e.categoria or '-'
                    })
            else:
                # Si no hay IDs, asumir que son nombres separados por coma
                nombres = [n.strip() for n in empresas_nombres.split(',') if n.strip()]
                if nombres:
                    empresas = EmpresaTuristica.query.filter(EmpresaTuristica.nombre.in_(nombres)).all()
                    for e in empresas:
                        empresas_detalle.append({
                            'nombre': e.nombre,
                            'direccion': e.direccion or '-',
                            'telefono': e.telefono or '-',
                            'email': e.email or '-',
                            'categoria': e.categoria or '-'
                        })
                # Si tampoco hay coincidencias, mostrar los nombres tal cual
                if not empresas_detalle and nombres:
                    for n in nombres:
                        empresas_detalle.append({'nombre': n, 'direccion': '-', 'telefono': '-', 'email': '-', 'categoria': '-'})

            datos = [
                ("Institución", visita.nombre_institucion),
                ("Fecha de visita", fecha_formateada),
                ("Responsable", visita.responsable),
                ("Correo", visita.email),
                ("Teléfono", visita.telefono),
                ("Cantidad de alumnos", str(visita.cantidad_alumnos)),
                ("Hora Grupo 1", hora1_formateada),
                ("Hora Grupo 2", hora2_formateada),
                ("Observaciones", visita.observaciones or "Ninguna"),
            ]

            for label, value in datos:
                p.setFont("Helvetica-Bold", 12)
                p.drawString(left_margin, y, f"{label}:")
                p.setFont("Helvetica", 12)
                p.drawString(left_margin + 150, y, str(value))
                y -= line_space

            # Sección de empresas a visitar
            if empresas_detalle:
                y -= 10
                p.setFont("Helvetica-Bold", 13)
                p.setFillColorRGB(0.1, 0.2, 0.4)
                p.drawString(left_margin, y, "Empresas a Visitar:")
                y -= line_space
                p.setFillColorRGB(0, 0, 0)
                for emp in empresas_detalle:
                    p.setFont("Helvetica-Bold", 12)
                    p.drawString(left_margin + 10, y, f"• {emp['nombre']}")
                    y -= line_space - 6
                    p.setFont("Helvetica", 11)
                    p.drawString(left_margin + 30, y, f"Dirección: {emp['direccion']}")
                    y -= line_space - 10
                    p.drawString(left_margin + 30, y, f"Teléfono: {emp['telefono']}   Email: {emp['email']}")
                    y -= line_space - 10
                    p.drawString(left_margin + 30, y, f"Categoría: {emp['categoria']}")
                    y -= line_space

            # Línea separadora final
            p.setStrokeColorRGB(0.7, 0.7, 0.7)
            p.setLineWidth(1)
            p.line(left_margin, y + 10, width - right_margin, y + 10)

            # --- Pie de página ---
            p.setFont("Helvetica-Oblique", 10)
            p.setFillColorRGB(0.3, 0.3, 0.3)
            p.drawCentredString(width / 2, bottom_margin + 20, "Sistema de Gestión de Visitas Turísticas - Municipalidad de Esperanza")
            p.setFont("Helvetica", 11)
            p.setFillColorRGB(0, 0, 0)
            p.drawString(left_margin, bottom_margin + 40, "Firma y Sello: ............................................................")

            p.save()
            
            # Guardar registro del itinerario en la base de datos - COMENTADO TEMPORALMENTE
            # itinerario = Itinerario(
            #     solicitud_id=visita.id,
            #     observaciones_itinerario="Itinerario generado automáticamente",
            #     creado_por="Sistema"
            # )
            # db.session.add(itinerario)
            # db.session.commit()
            
            buffer.seek(0)
            return send_file(buffer, as_attachment=True, download_name="itinerario.pdf", mimetype='application/pdf')
            
        except (ValueError, TypeError, OSError) as e:
            print(f"Error al crear itinerario: {e}")
            return "Error al generar itinerario", 500

    # GET: mostrar solo visitas confirmadas
    try:
        visitas = SolicitudVisita.query.filter_by(estado="Confirmada").all()
        return render_template('crear_itinerario.html', visitas=visitas)
    except (ValueError, TypeError, OSError) as e:
        print(f"Error al obtener visitas: {e}")
        return render_template('crear_itinerario.html', visitas=[])



# ------------------------------
# Ruta para ver datos de la base de datos
# ------------------------------

@app.route('/ver_datos')
def ver_datos():
    """Página para visualizar todos los datos de la base de datos"""
    try:
        # Obtener datos de todas las tablas
        empresas = EmpresaTuristica.query.all()
        visitas = SolicitudVisita.query.all()
        consultas = ConsultaEmpresa.query.all()
        usuarios = Usuario.query.all()
        
        datos = {
            'empresas': empresas,
            'visitas': visitas,
            'consultas': consultas,
            'usuarios': usuarios
        }
        
        return render_template('ver_datos.html', datos=datos)
    except Exception as e:
        return f"Error al obtener datos: {e}", 500

@app.route('/ver_datos_json')
def ver_datos_json():
    """API para ver todos los datos en formato JSON"""
    try:
        # Empresas
        empresas = []
        for empresa in EmpresaTuristica.query.all():
            empresas.append({
                'id': empresa.id,
                'nombre': empresa.nombre,
                'email': empresa.email,
                'telefono': empresa.telefono,
                'categoria': empresa.categoria,
                'fecha_creacion': empresa.fecha_creacion.strftime('%Y-%m-%d %H:%M:%S') if empresa.fecha_creacion else None
            })
        
        # Visitas
        visitas = []
        for visita in SolicitudVisita.query.all():
            visitas.append({
                'id': visita.id,
                'institucion': visita.nombre_institucion,
                'responsable': visita.responsable,
                'email': visita.email,
                'cantidad_alumnos': visita.cantidad_alumnos,
                'estado': visita.estado,
                'fecha_visita': visita.fecha_visita.strftime('%Y-%m-%d') if visita.fecha_visita else None,
                'fecha_solicitud': visita.fecha_solicitud.strftime('%Y-%m-%d %H:%M:%S') if visita.fecha_solicitud else None
            })
        
        # Consultas
        consultas = []
        for consulta in ConsultaEmpresa.query.all():
            consultas.append({
                'id': consulta.id,
                'empresa_id': consulta.empresa_id,
                'empresa_nombre': consulta.empresa.nombre if consulta.empresa else 'N/A',
                'fecha_consulta': consulta.fecha_consulta.strftime('%Y-%m-%d') if consulta.fecha_consulta else None,
                'hora_consulta': consulta.hora_consulta.strftime('%H:%M') if consulta.hora_consulta else None,
                'comentarios': consulta.comentarios,
                'estado': consulta.estado,
                'fecha_creacion': consulta.fecha_creacion.strftime('%Y-%m-%d %H:%M:%S') if consulta.fecha_creacion else None
            })
        
        return jsonify({
            'empresas': empresas,
            'visitas': visitas,
            'consultas': consultas,
            'resumen': {
                'total_empresas': len(empresas),
                'total_visitas': len(visitas),
                'total_consultas': len(consultas)
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ------------------------------
# Funciones auxiliares
# ------------------------------

def obtener_nombres_empresas(empresas_ids_str):
    """
    Convierte una cadena de IDs de empresas separados por comas
    en una lista de nombres de empresas
    """
    if not empresas_ids_str:
        return []
    
    try:
        # Convertir string de IDs a lista de enteros
        ids_empresas = [int(id_str.strip()) for id_str in empresas_ids_str.split(',') if id_str.strip()]
        
        # Buscar las empresas por ID
        empresas = EmpresaTuristica.query.filter(EmpresaTuristica.id.in_(ids_empresas)).all()
        
        # Retornar lista de nombres
        return [empresa.nombre for empresa in empresas]
    except (ValueError, TypeError) as e:
        print(f"Error al obtener nombres de empresas: {e}")
        return []

# Registrar función para usar en templates
@app.template_filter('empresas_nombres')
def empresas_nombres_filter(empresas_ids_str):
    """Filtro para templates que convierte IDs de empresas a nombres"""
    nombres = obtener_nombres_empresas(empresas_ids_str)
    if nombres:
        return ', '.join(nombres)
    return 'Ninguna empresa seleccionada'


# ------------------------------
# Ejecución de la aplicación
# ------------------------------

if __name__ == '__main__':
    with app.app_context():
        # Crear las tablas automáticamente
        db.create_all()
        print("✅ Base de datos lista")
        
        # Mostrar estado del correo
        if MAIL_ENABLED:
            print(f"📧 Correo ACTIVADO - Enviando desde: {MAIL_USERNAME}")
            print(f"🔐 Contraseña configurada: {'Sí' if MAIL_PASSWORD != 'tu_password_de_aplicacion' else 'No'}")
        else:
            print("⚠️  Correo en MODO SIMULADO")
            print("Para activar envío real:")
            print("1. Edita app.py líneas 31-32")
            print("2. Coloca tu Gmail y contraseña de aplicación")
            print("3. Reinicia la aplicación")
    
    print("🌐 Aplicación corriendo en http://localhost:5000")
    app.run(host='127.0.0.1', port=5000, debug=True)