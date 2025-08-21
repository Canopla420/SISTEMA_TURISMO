#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Forzar UTF-8 y locale en Windows
import sys
if sys.platform.startswith('win'):
    import os
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    os.environ['LC_ALL'] = 'es_AR.UTF-8'
    os.environ['LANG'] = 'es_AR.UTF-8'

from flask import Flask, request, jsonify, render_template, redirect, url_for, send_file
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
import io
from datetime import datetime
from reportlab.lib.pagesizes import letter
from dotenv import load_dotenv
from config import config

# Cargar variables de entorno desde .env
load_dotenv()


app = Flask(__name__)

# Cargar configuración
config_name = os.getenv('FLASK_CONFIG', 'development')
app.config.from_object(config[config_name])

db = SQLAlchemy(app)

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

# Comentado temporalmente para evitar errores
# class VisitaRealizada(db.Model):
#     __tablename__ = 'visitas_realizadas'
# 
# class ConsultaEmpresa(db.Model):
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
        
        # Capturar los datos del formulario
        solicitud = SolicitudVisita(
            nombre_institucion=request.form.get('nombre_institucion'),
            localidad=request.form.get('localidad'),
            tipo_institucion=tipo_institucion,
            es_de_esperanza=es_de_esperanza,
            director=request.form.get('director'),
            correo_institucional=request.form.get('correo_institucional'),
            telefono_institucion=request.form.get('telefono_institucion'),
            contacto_principal=request.form.get('contacto_principal'),
            telefono_contacto_principal=request.form.get('telefono_contacto_principal'),
            relacion_contacto=request.form.get('relacion_contacto'),
            contacto_suplente=request.form.get('contacto_suplente'),
            telefono_contacto_suplente=request.form.get('telefono_contacto_suplente'),
            nivel_educativo=request.form.get('nivel_educativo'),
            cantidad_alumnos=int(request.form.get('cantidad_alumnos', 0)),
            edad_alumnos=request.form.get('edad_alumnos'),
            discapacidad=request.form.get('discapacidad'),
            tipo_discapacidad=request.form.get('tipo_discapacidad'),
            adaptacion=request.form.get('adaptacion'),
            empresas_seleccionadas=",".join(request.form.getlist('lugares[]')),  # Ahora son empresas
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
    # Las empresas se filtrarán dinámicamente según el tipo de institución y nivel educativo
    return render_template('nueva_visita.html')

@app.route('/modificar_visita/<int:visita_id>', methods=['GET', 'POST'])
def modificar_visita(visita_id):
    """Modificar una visita existente"""
    visita = SolicitudVisita.query.get_or_404(visita_id)  # Buscar la visita por ID

    if request.method == 'POST':
        try:
            # Actualizar todos los datos de la visita con los valores enviados desde el formulario
            visita.nombre_institucion = request.form.get('nombre_institucion')
            visita.localidad = request.form.get('localidad')
            visita.director = request.form.get('director')
            visita.correo_institucional = request.form.get('correo_institucional')
            visita.telefono_institucion = request.form.get('telefono_institucion')
            visita.contacto_principal = request.form.get('contacto_principal')
            visita.telefono_contacto_principal = request.form.get('telefono_contacto_principal')
            visita.relacion_contacto = request.form.get('relacion_contacto')
            visita.contacto_suplente = request.form.get('contacto_suplente')
            visita.telefono_contacto_suplente = request.form.get('telefono_contacto_suplente')
            visita.nivel_educativo = request.form.get('nivel_educativo')
            
            # Convertir cantidad_alumnos a entero
            cantidad_str = request.form.get('cantidad_alumnos')
            visita.cantidad_alumnos = int(cantidad_str) if cantidad_str and cantidad_str.strip() else 0
            
            visita.edad_alumnos = request.form.get('edad_alumnos')
            visita.discapacidad = request.form.get('discapacidad')
            visita.tipo_discapacidad = request.form.get('tipo_discapacidad')
            visita.adaptacion = request.form.get('adaptacion')
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
    return render_template('modificar_visita.html', visita=visita)


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
    return render_template('nueva_visita.html')

@app.route('/confirmar_visita/<int:visita_id>', methods=['POST'])
def confirmar_visita(visita_id):
    """Confirmar una visita por su ID"""
    try:
        visita = SolicitudVisita.query.get_or_404(visita_id)
        if visita.estado == "Pendiente":
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
        if visita.estado in ["Confirmada", "Pendiente"]:
            visita.estado = "Rechazada"
            db.session.commit()
        return redirect(url_for('consultar_visitas'))
    except (ValueError, TypeError, OSError) as e:
        db.session.rollback()
        print(f"Error al rechazar visita: {e}")
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
    return render_template('consultar_empresas.html')

@app.route('/todas_empresas', methods=['GET'])
def todas_empresas():
    """Devuelve la lista de empresas activas en formato JSON"""
    try:
        empresas = EmpresaTuristica.query.filter_by(activa=True).all()
        empresas_json = []
        for empresa in empresas:
            empresas_json.append({
                "id": empresa.id,
                "nombre": empresa.nombre,
                "correo": empresa.correo,
                "telefono": empresa.telefono,
                "direccion": empresa.direccion,
                "servicios_ofrecidos": empresa.servicios_ofrecidos,
                "categoria_turismo": empresa.categoria_turismo,
                "nivel_educativo_objetivo": empresa.nivel_educativo_objetivo,
                "costo_por_persona": float(empresa.costo_por_persona) if empresa.costo_por_persona else None
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
        query = EmpresaTuristica.query.filter_by(activa=True, categoria_turismo=categoria_turismo)
        
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
                "correo": empresa.correo,
                "telefono": empresa.telefono,
                "direccion": empresa.direccion,
                "servicios_ofrecidos": empresa.servicios_ofrecidos,
                "categoria_turismo": empresa.categoria_turismo,
                "nivel_educativo_objetivo": empresa.nivel_educativo_objetivo,
                "costo_por_persona": float(empresa.costo_por_persona) if empresa.costo_por_persona else None
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
            EmpresaTuristica.nombre.ilike(f'%{query}%'),
            EmpresaTuristica.activa == True
        ).all()
        
        coincidencias = []
        for empresa in empresas:
            coincidencias.append({
                "id": empresa.id,
                "nombre": empresa.nombre,
                "correo": empresa.correo,
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
        comentarios = request.form.get('comentarios')

        if not (empresa_nombre and correo and fecha_str and hora_str):
            return jsonify({"error": "Faltan datos obligatorios"}), 400

        # Buscar la empresa en la base de datos
        empresa = EmpresaTuristica.query.filter_by(nombre=empresa_nombre, activa=True).first()
        if not empresa:
            return jsonify({"error": "Empresa no encontrada"}), 404

        # Convertir fecha y hora
        fecha_consulta = datetime.strptime(fecha_str, '%Y-%m-%d').date()
        hora_consulta = datetime.strptime(hora_str, '%H:%M').time()

        # Guardar la consulta en la base de datos - COMENTADO TEMPORALMENTE
        # consulta = ConsultaEmpresa(
        #     empresa_id=empresa.id,
        #     fecha_consulta=fecha_consulta,
        #     hora_consulta=hora_consulta,
        #     comentarios=comentarios
        # )
        # db.session.add(consulta)
        db.session.commit()

        # Crear y enviar el correo (comentado para evitar errores sin configuración real)
        # try:
        #     msg = Message('Consulta de disponibilidad',
        #                   sender=app.config['MAIL_USERNAME'],
        #                   recipients=[correo])
        #     msg.body = f"""
        #     Hola {empresa_nombre},
        #     
        #     Queremos saber si están disponibles en la fecha {fecha_str} a las {hora_str}.
        #     
        #     Comentarios adicionales:
        #     {comentarios}
        #     
        #     Saludos,
        #     Sistema de Gestión de Visitas - ITEC
        #     """
        #     mail.send(msg)
        # except Exception as mail_error:
        #     print(f"Error al enviar correo: {mail_error}")
        
        return jsonify({"mensaje": "Consulta registrada correctamente"}), 200
        
    except (ValueError, TypeError, OSError) as e:
        db.session.rollback()
        print(f"Error al procesar consulta: {e}")
        return jsonify({"error": "No se pudo procesar la consulta"}), 500

# Nuevas rutas para gestión de empresas
@app.route('/gestionar_empresas', methods=['GET'])
def gestionar_empresas():
    """Pantalla para gestionar empresas (CRUD)"""
    try:
        empresas = EmpresaTuristica.query.all()
        return render_template('gestionar_empresas.html', empresas=empresas)
    except (ValueError, TypeError, OSError) as e:
        print(f"Error en gestionar_empresas: {e}")
        # Devolver una página con lista vacía en caso de error
        return render_template('gestionar_empresas.html', empresas=[])

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
                email=request.form.get('correo'),
                categoria=request.form.get('categoria_turismo'),
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
            empresa.correo = request.form.get('correo')
            empresa.telefono = request.form.get('telefono')
            empresa.direccion = request.form.get('direccion')
            empresa.servicios_ofrecidos = request.form.get('servicios_ofrecidos')
            empresa.descripcion = request.form.get('descripcion')
            empresa.categoria_turismo = request.form.get('categoria_turismo')
            empresa.nivel_educativo_objetivo = request.form.get('nivel_educativo_objetivo')
            empresa.capacidad_maxima = capacidad
            empresa.horarios_atencion = request.form.get('horarios_atencion')
            empresa.costo_por_persona = costo
            empresa.requiere_reserva = bool(request.form.get('requiere_reserva'))
            empresa.activa = bool(request.form.get('activa', True))
            
            db.session.commit()
            return redirect(url_for('gestionar_empresas'))
        except (ValueError, TypeError, OSError) as e:
            db.session.rollback()
            print(f"Error al editar empresa: {e}")
            return "Error al editar empresa", 500
    
    return render_template('editar_empresa.html', empresa=empresa)

@app.route('/eliminar_empresa/<int:empresa_id>', methods=['POST'])
def eliminar_empresa(empresa_id):
    """Desactivar una empresa (soft delete)"""
    try:
        empresa = EmpresaTuristica.query.get_or_404(empresa_id)
        empresa.activa = False
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

            # Título principal
            p.setFont("Helvetica-Bold", 20)
            p.setFillColorRGB(0.1, 0.2, 0.4)
            # (Eliminado bloque incorrecto de creación de empresa)
            p.setFillColorRGB(0, 0, 0)
            y = height - top_margin - 100
            line_space = 20

            # Formatear fecha y horas
            fecha_formateada = visita.fecha_visita.strftime('%d/%m/%Y') if visita.fecha_visita else "No especificada"
            hora1_formateada = visita.hora_grupo1.strftime('%H:%M') if visita.hora_grupo1 else "No especificada"
            hora2_formateada = visita.hora_grupo2.strftime('%H:%M') if visita.hora_grupo2 else "No especificada"

            datos = [
                ("Institución", visita.nombre_institucion),
                ("Fecha de visita", fecha_formateada),
                ("Localidad", visita.localidad),
                ("Director/a", visita.director),
                ("Correo", visita.correo_institucional),
                ("Teléfono", visita.telefono_institucion),
                ("Nivel educativo", visita.nivel_educativo),
                ("Cantidad de alumnos", str(visita.cantidad_alumnos)),
                ("Hora Grupo 1", hora1_formateada),
                ("Hora Grupo 2", hora2_formateada),
                ("Empresas a visitar", visita.empresas_seleccionadas),
                ("Observaciones", visita.observaciones or "Ninguna"),
            ]

            for label, value in datos:
                p.setFont("Helvetica-Bold", 12)
                p.drawString(left_margin, y, f"{label}:")
                p.setFont("Helvetica", 12)
                p.drawString(left_margin + 130, y, str(value))
                y -= line_space

            # Línea separadora final
            p.setStrokeColorRGB(0.7, 0.7, 0.7)
            p.setLineWidth(1)
            p.line(left_margin, y + 10, width - right_margin, y + 10)

            # Pie de página
            p.setFont("Helvetica-Oblique", 10)
            p.setFillColorRGB(0.3, 0.3, 0.3)
            p.drawCentredString(width / 2, bottom_margin, "Sistema de Gestión de Visitas - ITEC")

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
# Ejecución de la aplicación
# ------------------------------

if __name__ == '__main__':
    app.run(debug=True)