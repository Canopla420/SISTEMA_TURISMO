#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script para inicializar la base de datos SQLite
"""

import os
import sys

# Añadir el directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Importar la aplicación y la base de datos
from app import app, db

def inicializar_bd():
    """Inicializar la base de datos"""
    print("🔧 Inicializando base de datos...")
    
    # Crear el contexto de la aplicación
    with app.app_context():
        try:
            # Eliminar todas las tablas existentes
            print("🗑️ Eliminando tablas existentes...")
            db.drop_all()
            
            # Crear todas las tablas
            print("🏗️ Creando nuevas tablas...")
            db.create_all()
            
            print("✅ Base de datos inicializada correctamente")
            
            # Verificar que las tablas se crearon
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tablas = inspector.get_table_names()
            print(f"📋 Tablas creadas: {tablas}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error al inicializar la base de datos: {e}")
            return False

if __name__ == '__main__':
    inicializar_bd()
