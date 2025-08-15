#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

# Configurar codificación UTF-8
if sys.platform.startswith('win'):
    os.environ['PYTHONIOENCODING'] = 'utf-8'

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Crear aplicación Flask mínima
app = Flask(__name__)

# Configuración directa de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://turismo_user:turismo_pass@localhost:5432/turismo_db?client_encoding=utf8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Definir los modelos exactamente como en la base de datos
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

def cargar_datos_forzado():
    with app.app_context():
        try:
            print("🔍 VERIFICANDO ESTADO ACTUAL...")
            
            # Verificar si hay datos
            empresas_count = EmpresaTuristica.query.count()
            solicitudes_count = SolicitudVisita.query.count()
            
            print(f"📊 Estado actual: {empresas_count} empresas, {solicitudes_count} solicitudes")
            
            if empresas_count > 0:
                print("✅ Ya hay empresas. Listando...")
                empresas = EmpresaTuristica.query.all()
                for empresa in empresas:
                    print(f"  - {empresa.nombre} ({empresa.categoria})")
                return
            
            print("🚀 CARGANDO DATOS...")
            
            # Datos de empresas
            empresas_data = [
                {
                    'nombre': 'Museo Histórico de la Colonización Esperanza',
                    'descripcion': 'Museo que preserva la historia de la colonización suiza-alemana',
                    'direccion': 'Av. San Martín 402',
                    'telefono': '(03496) 420-789',
                    'email': 'museo@esperanza.gov.ar',
                    'categoria': 'Turismo de Identidad',
                    'capacidad_maxima': 40,
                    'duracion_visita': '90 minutos'
                },
                {
                    'nombre': 'Centro Cultural Municipal Casa Diefenbach',
                    'descripcion': 'Centro cultural en edificio histórico de 1920',
                    'direccion': 'Calle 25 de Mayo 356',
                    'telefono': '(03496) 420-123',
                    'email': 'cultura@esperanza.gov.ar',
                    'categoria': 'Turismo de Identidad',
                    'capacidad_maxima': 60,
                    'duracion_visita': '75 minutos'
                },
                {
                    'nombre': 'Iglesia San Pedro',
                    'descripcion': 'Primera iglesia de la colonia suiza, construida en 1862',
                    'direccion': 'Plaza San Martín s/n',
                    'telefono': '(03496) 420-456',
                    'email': 'sanpedro@esperanza.gov.ar',
                    'categoria': 'Turismo de Identidad',
                    'capacidad_maxima': 80,
                    'duracion_visita': '60 minutos'
                },
                {
                    'nombre': 'Granja Educativa Los Aromos',
                    'descripcion': 'Experiencia educativa en granja con animales de granja',
                    'direccion': 'Ruta Provincial 70 Km 8',
                    'telefono': '(03496) 421-555',
                    'email': 'info@granjalosaromos.com',
                    'categoria': 'Turismo Educativo',
                    'capacidad_maxima': 50,
                    'duracion_visita': '3 horas'
                },
                {
                    'nombre': 'Reserva Natural Municipal',
                    'descripcion': 'Reserva natural con senderos interpretativos y fauna nativa',
                    'direccion': 'Camino Rural al Río Salado',
                    'telefono': '(03496) 421-777',
                    'email': 'reserva@esperanza.gov.ar',
                    'categoria': 'Turismo Educativo',
                    'capacidad_maxima': 35,
                    'duracion_visita': '2.5 horas'
                }
            ]
            
            # Insertar empresas
            for i, empresa_data in enumerate(empresas_data, 1):
                print(f"  {i}. Insertando {empresa_data['nombre']}")
                empresa = EmpresaTuristica(**empresa_data)
                db.session.add(empresa)
            
            # Insertar solicitud de ejemplo
            print("  6. Insertando solicitud de ejemplo")
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
            
            # Guardar todo
            db.session.commit()
            
            print("✅ ¡DATOS CARGADOS EXITOSAMENTE!")
            print(f"✅ Total insertado: {len(empresas_data)} empresas y 1 solicitud")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            db.session.rollback()
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    cargar_datos_forzado()
