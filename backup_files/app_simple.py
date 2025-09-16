#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script simple para inicializar y ejecutar la aplicación
"""

import os
import sys
from app import app, db

def main():
    print("🚀 Iniciando aplicación de turismo...")
    
    with app.app_context():
        try:
            # Crear todas las tablas
            print("🏗️ Creando tablas...")
            db.create_all()
            print("✅ Tablas creadas correctamente")
            
            # Verificar que existen
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tablas = inspector.get_table_names()
            print(f"📋 Tablas disponibles: {tablas}")
            
        except Exception as e:
            print(f"⚠️ Advertencia al crear tablas: {e}")
    
    # Ejecutar la aplicación
    print("🌐 Iniciando servidor web en http://localhost:5000")
    print("📝 Para probar: ve a la página y haz click en 'Cargar Nueva Visita'")
    app.run(host='127.0.0.1', port=5000, debug=True)

if __name__ == '__main__':
    main()
