from flask import Flask, request, jsonify, render_template, redirect, url_for, send_file
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
import io
import os
from datetime import datetime, date
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

class SolicitudVisita(db.Model):
    __tablename__ = 'solicitudes_visita'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre_institucion = db.Column(db.String(100), nullable=False)
    localidad = db.Column(db.String(100), nullable=False)
    # Nuevo campo para categorizar el tipo de institución
    tipo_institucion = db.Column(db.String(20), nullable=False)  # 'local' o 'externa'
    es_de_esperanza = db.Column(db.Boolean, default=False)  # True si es de Esperanza (nuestra identidad)
    director = db.Column(db.String(100), nullable=False)
    correo_institucional = db.Column(db.String(100), nullable=False)
    telefono_institucion = db.Column(db.String(20), nullable=False)
    contacto_principal = db.Column(db.String(100), nullable=False)
    telefono_contacto_principal = db.Column(db.String(20), nullable=False)
    relacion_contacto = db.Column(db.String(50), nullable=False)
    contacto_suplente = db.Column(db.String(100), nullable=True)
    telefono_contacto_suplente = db.Column(db.String(20), nullable=True)
    nivel_educativo = db.Column(db.String(50), nullable=False)  # 'Primario' o 'Secundario'
    cantidad_alumnos = db.Column(db.Integer, nullable=False)
    edad_alumnos = db.Column(db.String(50), nullable=False)
    discapacidad = db.Column(db.String(10), nullable=False)
    tipo_discapacidad = db.Column(db.String(100), nullable=True)
    adaptacion = db.Column(db.String(10), nullable=True)
    empresas_seleccionadas = db.Column(db.Text, nullable=False)  # JSON string con empresas seleccionadas
    fecha_visita = db.Column(db.Date, nullable=False)
    hora_grupo1 = db.Column(db.Time, nullable=True)
    hora_grupo2 = db.Column(db.Time, nullable=True)
    observaciones = db.Column(db.Text, nullable=True)
    estado = db.Column(db.String(20), default="Pendiente")  # Pendiente, Confirmada, Realizada, Cancelada
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_actualizacion = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    visitas_realizadas = db.relationship('VisitaRealizada', backref='solicitud', lazy=True, cascade='all, delete-orphan')
    itinerarios = db.relationship('Itinerario', backref='solicitud', lazy=True, cascade='all, delete-orphan')

class EmpresaTuristica(db.Model):
    __tablename__ = 'empresas_turisticas'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True)
    correo = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(20), nullable=True)
    direccion = db.Column(db.String(200), nullable=True)
    servicios_ofrecidos = db.Column(db.Text, nullable=True)
    descripcion = db.Column(db.Text, nullable=True)
    
    # Nuevos campos para categorización
    categoria_turismo = db.Column(db.String(20), nullable=False)  # 'identidad' o 'educativo'
    nivel_educativo_objetivo = db.Column(db.String(50), nullable=False)  # 'Primario', 'Secundario', 'Ambos'
    
    # Campos adicionales
    capacidad_maxima = db.Column(db.Integer, nullable=True)
    horarios_atencion = db.Column(db.String(100), nullable=True)
    costo_por_persona = db.Column(db.Numeric(10, 2), nullable=True)
    requiere_reserva = db.Column(db.Boolean, default=True)
    activa = db.Column(db.Boolean, default=True)
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_actualizacion = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    consultas = db.relationship('ConsultaEmpresa', backref='empresa', lazy=True, cascade='all, delete-orphan')
    visitas_realizadas = db.relationship('VisitaRealizada', backref='empresa', lazy=True)

class VisitaRealizada(db.Model):
    __tablename__ = 'visitas_realizadas'
    
    id = db.Column(db.Integer, primary_key=True)
    solicitud_id = db.Column(db.Integer, db.ForeignKey('solicitudes_visita.id'), nullable=False)
    empresa_id = db.Column(db.Integer, db.ForeignKey('empresas_turisticas.id'), nullable=True)
    fecha_realizada = db.Column(db.Date, nullable=False)
    hora_inicio = db.Column(db.Time, nullable=True)
    hora_fin = db.Column(db.Time, nullable=True)
    calificacion = db.Column(db.Integer, nullable=True)  # 1-5 estrellas
    comentarios_finales = db.Column(db.Text, nullable=True)
    costo_total = db.Column(db.Numeric(10, 2), nullable=True)
    cantidad_participantes_real = db.Column(db.Integer, nullable=True)
    guia_asignado = db.Column(db.String(100), nullable=True)
    clima = db.Column(db.String(50), nullable=True)
    incidentes = db.Column(db.Text, nullable=True)
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)

class ConsultaEmpresa(db.Model):
    __tablename__ = 'consultas_empresas'
    
    id = db.Column(db.Integer, primary_key=True)
    empresa_id = db.Column(db.Integer, db.ForeignKey('empresas_turisticas.id'), nullable=False)
    fecha_consulta = db.Column(db.Date, nullable=False)
    hora_consulta = db.Column(db.Time, nullable=False)
    comentarios = db.Column(db.Text, nullable=True)
    fecha_envio = db.Column(db.DateTime, default=datetime.utcnow)
    respondida = db.Column(db.Boolean, default=False)
    respuesta = db.Column(db.Text, nullable=True)
    fecha_respuesta = db.Column(db.DateTime, nullable=True)
    estado = db.Column(db.String(20), default="Enviada")  # Enviada, Respondida, Sin respuesta

class Itinerario(db.Model):
    __tablename__ = 'itinerarios'
    
    id = db.Column(db.Integer, primary_key=True)
    solicitud_id = db.Column(db.Integer, db.ForeignKey('solicitudes_visita.id'), nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    ruta_archivo = db.Column(db.String(200), nullable=True)
    observaciones_itinerario = db.Column(db.Text, nullable=True)
    version = db.Column(db.Integer, default=1)
    creado_por = db.Column(db.String(100), nullable=True)

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    nombre_completo = db.Column(db.String(100), nullable=False)
    rol = db.Column(db.String(20), default="operador")  # admin, operador
    activo = db.Column(db.Boolean, default=True)
    ultimo_acceso = db.Column(db.DateTime, nullable=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    
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
        except Exception as e:
            db.session.rollback()
            print(f"Error al guardar solicitud: {e}")
            return "Error al procesar la solicitud", 500

    # Renderizar el formulario si es una solicitud GET
    # Las empresas se filtrarán dinámicamente según el tipo de institución y nivel educativo
    return render_template('nueva_visita.html')

@app.route('/modificar_visita/<int:id>', methods=['GET', 'POST'])
def modificar_visita(id):
    """Modificar una visita existente"""
    visita = SolicitudVisita.query.get_or_404(id)  # Buscar la visita por ID

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
            
        except Exception as e:
            db.session.rollback()
            print(f"Error al modificar visita: {e}")
            return f"Error al modificar visita: {e}", 500

    # Renderizar el formulario con los datos actuales de la visita
    return render_template('modificar_visita.html', visita=visita)


@app.route('/confirmacion_visita', methods=['GET'])
def confirmacion_visita():
    """Página de confirmación después de enviar una solicitud"""
    return render_template('confirmacion_carga_visita.html')

@app.route('/eliminar_visita/<int:id>', methods=['POST'])
def eliminar_visita(id):
    """Eliminar una visita por su ID"""
    try:
        # Buscar la visita por ID
        visita = SolicitudVisita.query.get_or_404(id)
        
        # Eliminar la visita
        db.session.delete(visita)
        db.session.commit()  # Confirmar los cambios en la base de datos
        
        # Redirigir a la página de consultar visitas
        return redirect(url_for('consultar_visitas'))
    except Exception as e:
        db.session.rollback()
        print(f"Error al eliminar visita: {e}")
        return redirect(url_for('consultar_visitas'))

@app.route('/nueva_visita')
def nueva_visita():
    """Formulario para registrar una nueva visita"""
    return render_template('nueva_visita.html')

@app.route('/confirmar_visita/<int:id>', methods=['POST'])
def confirmar_visita(id):
    """Confirmar una visita por su ID"""
    try:
        visita = SolicitudVisita.query.get_or_404(id)
        if visita.estado == "Pendiente":
            visita.estado = "Confirmada"
            db.session.commit()
        return redirect(url_for('consultar_visitas'))
    except Exception as e:
        db.session.rollback()
        print(f"Error al confirmar visita: {e}")
        return redirect(url_for('consultar_visitas'))

@app.route('/rechazar_visita/<int:id>', methods=['POST'])
def rechazar_visita(id):
    """Rechazar una visita por su ID"""
    try:
        visita = SolicitudVisita.query.get_or_404(id)
        if visita.estado in ["Confirmada", "Pendiente"]:
            visita.estado = "Rechazada"
            db.session.commit()
        return redirect(url_for('consultar_visitas'))
    except Exception as e:
        db.session.rollback()
        print(f"Error al rechazar visita: {e}")
        return redirect(url_for('consultar_visitas'))

@app.route('/consultar_visitas', methods=['GET', 'POST'])
def consultar_visitas():
    """Pantalla para consultar visitas"""
    nombre_institucion = ''
    estado = ''
    
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
    except Exception as e:
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
    except Exception as e:
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
    except Exception as e:
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

        # Guardar la consulta en la base de datos
        consulta = ConsultaEmpresa(
            empresa_id=empresa.id,
            fecha_consulta=fecha_consulta,
            hora_consulta=hora_consulta,
            comentarios=comentarios
        )
        db.session.add(consulta)
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
        
    except Exception as e:
        db.session.rollback()
        print(f"Error al procesar consulta: {e}")
        return jsonify({"error": "No se pudo procesar la consulta"}), 500

# Nuevas rutas para gestión de empresas
@app.route('/gestionar_empresas', methods=['GET'])
def gestionar_empresas():
    """Pantalla para gestionar empresas (CRUD)"""
    empresas = EmpresaTuristica.query.all()
    return render_template('gestionar_empresas.html', empresas=empresas)

@app.route('/agregar_empresa', methods=['GET', 'POST'])
def agregar_empresa():
    """Agregar una nueva empresa"""
    if request.method == 'POST':
        try:
            costo_str = request.form.get('costo_por_persona')
            costo = float(costo_str) if costo_str and costo_str.strip() else None
            
            capacidad_str = request.form.get('capacidad_maxima')
            capacidad = int(capacidad_str) if capacidad_str and capacidad_str.strip() else None
            
            empresa = EmpresaTuristica(
                nombre=request.form.get('nombre'),
                correo=request.form.get('correo'),
                telefono=request.form.get('telefono'),
                direccion=request.form.get('direccion'),
                servicios_ofrecidos=request.form.get('servicios_ofrecidos'),
                descripcion=request.form.get('descripcion'),
                categoria_turismo=request.form.get('categoria_turismo'),  # 'identidad' o 'educativo'
                nivel_educativo_objetivo=request.form.get('nivel_educativo_objetivo'),  # 'Primario', 'Secundario', 'Ambos'
                capacidad_maxima=capacidad,
                horarios_atencion=request.form.get('horarios_atencion'),
                costo_por_persona=costo,
                requiere_reserva=bool(request.form.get('requiere_reserva'))
            )
            db.session.add(empresa)
            db.session.commit()
            return redirect(url_for('gestionar_empresas'))
        except Exception as e:
            db.session.rollback()
            print(f"Error al agregar empresa: {e}")
            return "Error al agregar empresa", 500
    
    return render_template('agregar_empresa.html')

@app.route('/editar_empresa/<int:id>', methods=['GET', 'POST'])
def editar_empresa(id):
    """Editar una empresa existente"""
    empresa = EmpresaTuristica.query.get_or_404(id)
    
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
        except Exception as e:
            db.session.rollback()
            print(f"Error al editar empresa: {e}")
            return "Error al editar empresa", 500
    
    return render_template('editar_empresa.html', empresa=empresa)

@app.route('/eliminar_empresa/<int:id>', methods=['POST'])
def eliminar_empresa(id):
    """Desactivar una empresa (soft delete)"""
    try:
        empresa = EmpresaTuristica.query.get_or_404(id)
        empresa.activa = False
        db.session.commit()
        return redirect(url_for('gestionar_empresas'))
    except Exception as e:
        db.session.rollback()
        print(f"Error al eliminar empresa: {e}")
        return redirect(url_for('gestionar_empresas'))

# ------------------------------
# Rutas relacionadas con visitas
# ------------------------------

@app.route('/guardar_visita', methods=['POST'])
def guardar_visita():
    """Guarda los datos de una nueva visita"""
    # Aquí podrías guardar los datos en una base de datos o archivo
    # datos = request.form (si lo necesitás)
    return redirect(url_for('nueva_visita', exito=True))


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
            p.drawCentredString(width / 2, height - top_margin - 30, "Itinerario de Visita")

            # Línea separadora
            p.setStrokeColorRGB(0.1, 0.2, 0.4)
            p.setLineWidth(2)
            p.line(left_margin, height - top_margin - 40, width - right_margin, height - top_margin - 40)

            # Subtítulo
            p.setFont("Helvetica-Bold", 14)
            p.setFillColorRGB(0.2, 0.2, 0.2)
            p.drawString(left_margin, height - top_margin - 70, "Datos de la Institución:")

            # Datos de la visita
            p.setFont("Helvetica", 12)
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
            
            # Guardar registro del itinerario en la base de datos
            itinerario = Itinerario(
                solicitud_id=visita.id,
                observaciones_itinerario="Itinerario generado automáticamente",
                creado_por="Sistema"
            )
            db.session.add(itinerario)
            db.session.commit()
            
            buffer.seek(0)
            return send_file(buffer, as_attachment=True, download_name="itinerario.pdf", mimetype='application/pdf')
            
        except Exception as e:
            print(f"Error al crear itinerario: {e}")
            return "Error al generar itinerario", 500

    # GET: mostrar solo visitas confirmadas
    try:
        visitas = SolicitudVisita.query.filter_by(estado="Confirmada").all()
        return render_template('crear_itinerario.html', visitas=visitas)
    except Exception as e:
        print(f"Error al obtener visitas: {e}")
        return render_template('crear_itinerario.html', visitas=[])



# ------------------------------
# Ejecución de la aplicación
# ------------------------------

if __name__ == '__main__':
    app.run(debug=True)