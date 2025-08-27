#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

# Configurar codificación UTF-8
if sys.platform.startswith('win'):
    os.environ['PYTHONIOENCODING'] = 'utf-8'

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config

# Crear aplicación Flask mínima
app = Flask(__name__)
config_name = os.getenv('FLASK_CONFIG', 'development')
app.config.from_object(config[config_name])

db = SQLAlchemy(app)

# Definir el modelo simplificado
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

class SolicitudVisita(db.Model):
    __tablename__ = 'solicitud_visita'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre_institucion = db.Column(db.String(200), nullable=False)
    responsable = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    cantidad_alumnos = db.Column(db.Integer, nullable=False)
    estado = db.Column(db.String(50), default='Pendiente')

def test_database():
    with app.app_context():
        try:
            print("🔍 PROBANDO CONEXIÓN A LA BASE DE DATOS...")
            
            # Probar conexión básica con SQLAlchemy 2.0
            with db.engine.connect() as conn:
                result = conn.execute(db.text("SELECT 1"))
                print("✅ Conexión a PostgreSQL exitosa")
                
                # Verificar que las tablas existen
                result = conn.execute(db.text("""
                    SELECT tablename FROM pg_tables 
                    WHERE schemaname = 'public'
                """))
                tables = [row[0] for row in result]
                print(f"📋 Tablas encontradas: {tables}")
                
                # Contar empresas
                result = conn.execute(db.text("SELECT COUNT(*) FROM empresa_turistica"))
                empresas_count = result.scalar()
                print(f"🏢 Total de empresas en BD: {empresas_count}")
                
                if empresas_count > 0:
                    # Mostrar empresas
                    result = conn.execute(db.text("SELECT id, nombre, categoria FROM empresa_turistica LIMIT 5"))
                    print("📝 Empresas encontradas:")
                    for row in result:
                        print(f"  - ID: {row[0]}, Nombre: {row[1]}, Categoría: {row[2]}")
                        
                    # Probar con SQLAlchemy ORM
                    print("\n🔄 Probando con SQLAlchemy ORM...")
                    empresas_orm = EmpresaTuristica.query.all()
                    print(f"✅ SQLAlchemy encontró {len(empresas_orm)} empresas")
                    for empresa in empresas_orm[:3]:
                        print(f"  - ORM: {empresa.nombre} ({empresa.categoria})")
                else:
                    print("❌ No hay empresas en la base de datos")
                
                # Contar solicitudes
                result = conn.execute(db.text("SELECT COUNT(*) FROM solicitud_visita"))
                solicitudes_count = result.scalar()
                print(f"📝 Total de solicitudes en BD: {solicitudes_count}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    test_database()
