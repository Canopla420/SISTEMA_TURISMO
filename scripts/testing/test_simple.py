#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import psycopg2
import os

def test_connection_bypass():
    try:
        print("🔍 PROBANDO CONEXIÓN CON BYPASS UTF-8...")
        
        # Intentar conexión con configuración específica para Windows
        connection_string = "host=localhost port=5432 dbname=turismo_db user=turismo_user password=turismo_pass"
        
        conn = psycopg2.connect(
            connection_string,
            connect_timeout=10
        )
        
        # Configurar la conexión para UTF-8
        conn.set_client_encoding('UTF8')
        
        cursor = conn.cursor()
        print("✅ Conexión exitosa")
        
        # Probar consulta simple
        cursor.execute("SELECT COUNT(*) FROM empresa_turistica")
        count = cursor.fetchone()[0]
        print(f"🏢 Empresas encontradas: {count}")
        
        if count > 0:
            cursor.execute("SELECT nombre FROM empresa_turistica LIMIT 3")
            empresas = cursor.fetchall()
            print("📝 Nombres de empresas:")
            for empresa in empresas:
                print(f"  - {empresa[0]}")
        
        cursor.execute("SELECT COUNT(*) FROM solicitud_visita")
        solicitudes = cursor.fetchone()[0]
        print(f"📝 Solicitudes encontradas: {solicitudes}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error en conexión: {e}")
        
        # Plan B: Verificar desde Adminer directamente
        print("\n🔄 PLAN B: Verificar en Adminer...")
        print("1. Ve a http://localhost:8080")
        print("2. Conecta con:")
        print("   - Servidor: localhost:5432")
        print("   - Usuario: turismo_user")
        print("   - Contraseña: turismo_pass")
        print("   - Base de datos: turismo_db")
        print("3. Ve a la tabla 'empresa_turistica' y verifica los datos")

if __name__ == "__main__":
    test_connection_bypass()
