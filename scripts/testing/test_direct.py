#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import psycopg2
import os
import sys

# Configurar variables de entorno para UTF-8
os.environ['PYTHONIOENCODING'] = 'utf-8'
os.environ['LC_ALL'] = 'en_US.UTF-8'

def test_direct_connection():
    try:
        print("🔍 PROBANDO CONEXIÓN DIRECTA A POSTGRESQL...")
        
        # Conexión directa con psycopg2
        conn = psycopg2.connect(
            host='localhost',
            port=5432,
            database='turismo_db',
            user='turismo_user',
            password='turismo_pass',
            options="-c client_encoding=utf8"  # Forzar UTF-8
        )
        
        cursor = conn.cursor()
        print("✅ Conexión directa exitosa")
        
        # Verificar tablas
        cursor.execute("""
            SELECT tablename FROM pg_tables 
            WHERE schemaname = 'public'
        """)
        tables = [row[0] for row in cursor.fetchall()]
        print(f"📋 Tablas encontradas: {tables}")
        
        # Contar empresas
        cursor.execute("SELECT COUNT(*) FROM empresa_turistica")
        empresas_count = cursor.fetchone()[0]
        print(f"🏢 Total de empresas: {empresas_count}")
        
        if empresas_count > 0:
            # Mostrar empresas
            cursor.execute("SELECT id, nombre, categoria FROM empresa_turistica LIMIT 5")
            empresas = cursor.fetchall()
            print("📝 Empresas encontradas:")
            for empresa in empresas:
                print(f"  - ID: {empresa[0]}, Nombre: {empresa[1]}, Categoría: {empresa[2]}")
        else:
            print("❌ No hay empresas en la base de datos")
            
        # Contar solicitudes
        cursor.execute("SELECT COUNT(*) FROM solicitud_visita")
        solicitudes_count = cursor.fetchone()[0]
        print(f"📝 Total de solicitudes: {solicitudes_count}")
        
        if solicitudes_count > 0:
            cursor.execute("SELECT id, nombre_institucion, estado FROM solicitud_visita LIMIT 3")
            solicitudes = cursor.fetchall()
            print("📝 Solicitudes encontradas:")
            for solicitud in solicitudes:
                print(f"  - ID: {solicitud[0]}, Institución: {solicitud[1]}, Estado: {solicitud[2]}")
        
        conn.close()
        print("\n✅ ¡DATOS VERIFICADOS CORRECTAMENTE!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_direct_connection()
