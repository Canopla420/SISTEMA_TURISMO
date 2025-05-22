from flask import Flask, request, jsonify, render_template, redirect, url_for, send_file
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
import io
import os

app = Flask(__name__)


# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///visitas.db'  # Base de datos SQLite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

migrate = Migrate(app, db)
# ------------------------------
# Definición del modelo
# ------------------------------
class SolicitudVisita(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre_institucion = db.Column(db.String(100), nullable=False)
    localidad = db.Column(db.String(100), nullable=False)
    director = db.Column(db.String(100), nullable=False)
    correo_institucional = db.Column(db.String(100), nullable=False)
    telefono_institucion = db.Column(db.String(20), nullable=False)
    contacto_principal = db.Column(db.String(100), nullable=False)
    telefono_contacto_principal = db.Column(db.String(20), nullable=False)
    relacion_contacto = db.Column(db.String(50), nullable=False)
    contacto_suplente = db.Column(db.String(100), nullable=True)
    telefono_contacto_suplente = db.Column(db.String(20), nullable=True)
    nivel_educativo = db.Column(db.String(50), nullable=False)
    cantidad_alumnos = db.Column(db.Integer, nullable=False)
    edad_alumnos = db.Column(db.String(50), nullable=False)
    discapacidad = db.Column(db.String(10), nullable=False)
    tipo_discapacidad = db.Column(db.String(100), nullable=True)
    adaptacion = db.Column(db.String(10), nullable=True)
    lugares = db.Column(db.Text, nullable=False)
    fecha_visita = db.Column(db.String(10), nullable=False)
    hora_grupo1 = db.Column(db.String(5), nullable=True)
    hora_grupo2 = db.Column(db.String(5), nullable=True)
    observaciones = db.Column(db.Text, nullable=True)
    estado = db.Column(db.String(20), default="Pendiente")  # Estado de la visita
    
# ------------------------------
# Crear las tablas en la base de datos
# ------------------------------
with app.app_context():
    db.create_all()



# Configuración de Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'tu_correo@gmail.com'  # Cambia esto por tu correo
app.config['MAIL_PASSWORD'] = 'tu_contraseña'        # Cambia esto por tu contraseña
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
        # Capturar los datos del formulario
        solicitud = SolicitudVisita(
            nombre_institucion=request.form.get('nombre_institucion'),
            localidad=request.form.get('localidad'),
            director=request.form.get('director'),
            correo_institucional=request.form.get('correo_institucional'),
            telefono_institucion=request.form.get('telefono_institucion'),
            contacto_principal=request.form.get('contacto_principal'),
            telefono_contacto_principal=request.form.get('telefono_contacto_principal'),
            relacion_contacto=request.form.get('relacion_contacto'),
            contacto_suplente=request.form.get('contacto_suplente'),
            telefono_contacto_suplente=request.form.get('telefono_contacto_suplente'),
            nivel_educativo=request.form.get('nivel_educativo'),
            cantidad_alumnos=request.form.get('cantidad_alumnos'),
            edad_alumnos=request.form.get('edad_alumnos'),
            discapacidad=request.form.get('discapacidad'),
            tipo_discapacidad=request.form.get('tipo_discapacidad'),
            adaptacion=request.form.get('adaptacion'),
            lugares=",".join(request.form.getlist('lugares[]')),  # Convierte la lista en una cadena
            fecha_visita=request.form.get('fecha_visita'),
            hora_grupo1=request.form.get('hora_grupo1'),
            hora_grupo2=request.form.get('hora_grupo2'),
            observaciones=request.form.get('observaciones')
        )

        # Guardar en la base de datos
        db.session.add(solicitud)
        db.session.commit()

        # Redirigir a la página de confirmación
        return redirect(url_for('confirmacion_visita'))

    # Renderizar el formulario si es una solicitud GET
    return render_template('nueva_visita.html')

@app.route('/modificar_visita/<int:id>', methods=['GET', 'POST'])
def modificar_visita(id):
    """Modificar una visita existente"""
    visita = SolicitudVisita.query.get_or_404(id)  # Buscar la visita por ID

    if request.method == 'POST':
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
        visita.cantidad_alumnos = request.form.get('cantidad_alumnos')
        visita.edad_alumnos = request.form.get('edad_alumnos')
        visita.discapacidad = request.form.get('discapacidad')
        visita.tipo_discapacidad = request.form.get('tipo_discapacidad')
        visita.adaptacion = request.form.get('adaptacion')
        visita.lugares = ",".join(request.form.getlist('lugares[]'))  # Convierte la lista en una cadena
        visita.fecha_visita = request.form.get('fecha_visita')
        visita.hora_grupo1 = request.form.get('hora_grupo1')
        visita.hora_grupo2 = request.form.get('hora_grupo2')
        visita.observaciones = request.form.get('observaciones')

        # Guardar los cambios en la base de datos
        db.session.commit()
        return redirect(url_for('consultar_visitas'))  # Redirigir a la página de consultar visitas

    # Renderizar el formulario con los datos actuales de la visita
    return render_template('modificar_visita.html', visita=visita)


@app.route('/confirmacion_visita', methods=['GET'])
def confirmacion_visita():
    """Página de confirmación después de enviar una solicitud"""
    return render_template('confirmacion_carga_visita.html')

@app.route('/eliminar_visita/<int:id>', methods=['POST'])
def eliminar_visita(id):
    """Eliminar una visita por su ID"""
    # Buscar la visita por ID
    visita = SolicitudVisita.query.get_or_404(id)
    
    # Eliminar la visita
    db.session.delete(visita)
    db.session.commit()  # Confirmar los cambios en la base de datos
    
    # Redirigir a la página de consultar visitas
    return redirect(url_for('consultar_visitas'))

@app.route('/nueva_visita')
def nueva_visita():
    """Formulario para registrar una nueva visita"""
    return render_template('nueva_visita.html')

@app.route('/confirmar_visita/<int:id>', methods=['POST'])
def confirmar_visita(id):
    """Confirmar una visita por su ID"""
    visita = SolicitudVisita.query.get_or_404(id)
    if visita.estado == "Pendiente":
        visita.estado = "Confirmada"
        db.session.commit()
    return redirect(url_for('consultar_visitas'))

@app.route('/rechazar_visita/<int:id>', methods=['POST'])
def rechazar_visita(id):
    """Rechazar una visita por su ID"""
    visita = SolicitudVisita.query.get_or_404(id)
    if visita.estado == "Confirmada":
        visita.estado = "Pendiente"
        db.session.commit()
    return redirect(url_for('consultar_visitas'))

@app.route('/consultar_visitas', methods=['GET'])
def consultar_visitas():
    """Pantalla para consultar visitas"""
    # Obtener todas las visitas desde la base de datos
    visitas = SolicitudVisita.query.all()
    return render_template('consultar_visitas.html', visitas=visitas)

@app.route('/crear_itinerario')
def crear_itinerario():
    """Pantalla para crear un itinerario"""
    return render_template('crear_itinerario.html')

# ------------------------------
# Rutas relacionadas con empresas
# ------------------------------

@app.route('/consultar_empresas', methods=['GET'])
def consultar_empresas():
    """Pantalla para consultar empresas"""
    return render_template('consultar_empresas.html')

@app.route('/todas_empresas', methods=['GET'])
def todas_empresas():
    """Devuelve la lista de empresas en formato JSON"""
    # Supongamos que las empresas están en una lista de diccionarios
    empresas = [
        {"nombre": "EcoTurismo SRL", "correo": "contacto@ecoturismo.com"},
        {"nombre": "Aventura Norte", "correo": "info@aventuranorte.com"},
        {"nombre": "Viajes Andes", "correo": "contacto@viajesandes.com"}
    ]
    return jsonify(empresas)

@app.route('/buscar_empresa')
def buscar_empresa():
    """Busca empresas por nombre (búsqueda dinámica)"""
    query = request.args.get("q", "").lower()
    empresas = [
        {"nombre": "EcoTurismo SRL", "correo": "contacto@ecoturismo.com"},
        {"nombre": "Aventura Norte", "correo": "info@aventuranorte.com"},
        {"nombre": "Viajes Andes", "correo": "contacto@viajesandes.com"}
    ]
    coincidencias = [e for e in empresas if query in e["nombre"].lower()]
    return jsonify(coincidencias)

@app.route('/enviar_consulta', methods=['POST'])
def enviar_consulta():
    """Procesa el formulario y envía un correo a la empresa seleccionada"""
    empresa = request.form.get('empresa')
    correo = request.form.get('correo')
    fecha = request.form.get('fecha')
    hora = request.form.get('hora')
    comentarios = request.form.get('comentarios')

    if not (empresa and correo and fecha and hora):
        return jsonify({"error": "Faltan datos obligatorios"}), 400

    try:
        # Crear y enviar el correo
        msg = Message('Consulta de disponibilidad',
                      sender=app.config['MAIL_USERNAME'],
                      recipients=[correo])
        msg.body = f"""
        Hola {empresa},

        Queremos saber si están disponibles en la fecha {fecha} a las {hora}.

        Comentarios adicionales:
        {comentarios}

        Saludos,
        """
        mail.send(msg)
        return jsonify({"mensaje": "Consulta enviada correctamente"}), 200
    except Exception as e:
        print(f"Error al enviar el correo: {e}")
        return jsonify({"error": "No se pudo enviar el correo"}), 500

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
        visita_id = request.form['visita_id']
        visita = SolicitudVisita.query.get(visita_id)
        if not visita:
            return "Visita no encontrada", 404

        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter

        # Márgenes tipo APA
        left_margin = right_margin = top_margin = bottom_margin = inch

        # # Logo
        # logo_path = os.path.join('static', 'img', 'logo.png')
        # if os.path.exists(logo_path):
        #     p.drawImage(logo_path, left_margin, height - top_margin - 60, width=100, height=60, mask='auto')

        # Título
        p.setFont("Times-Bold", 16)
        p.drawCentredString(width / 2, height - top_margin - 80, "Itinerario de Visita")

        # Datos de la visita (formato APA)
        p.setFont("Times-Roman", 12)
        y = height - top_margin - 120
        line_space = 24

        p.drawString(left_margin, y, f"Institución: {visita.nombre_institucion}")
        y -= line_space
        p.drawString(left_margin, y, f"Fecha de visita: {visita.fecha_visita}")
        y -= line_space
        p.drawString(left_margin, y, f"Localidad: {visita.localidad}")
        y -= line_space
        p.drawString(left_margin, y, f"Director/a: {visita.director}")
        y -= line_space
        p.drawString(left_margin, y, f"Correo: {visita.correo_institucional}")
        y -= line_space
        p.drawString(left_margin, y, f"Teléfono: {visita.telefono_institucion}")
        y -= line_space
        p.drawString(left_margin, y, f"Nivel educativo: {visita.nivel_educativo}")
        y -= line_space
        p.drawString(left_margin, y, f"Cantidad de alumnos: {visita.cantidad_alumnos}")
        y -= line_space
        p.drawString(left_margin, y, f"Lugares a visitar: {visita.lugares}")
        y -= line_space
        p.drawString(left_margin, y, f"Observaciones: {visita.observaciones or 'Ninguna'}")

        p.save()
        buffer.seek(0)
        return send_file(buffer, as_attachment=True, download_name="itinerario.pdf", mimetype='application/pdf')

    # GET: mostrar selector de visitas
    visitas = SolicitudVisita.query.all()
    return render_template('crear_itinerario.html', visitas=visitas)



# ------------------------------
# Ejecución de la aplicación
# ------------------------------

if __name__ == '__main__':
    app.run(debug=True)