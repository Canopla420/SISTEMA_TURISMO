#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para verificar que las tablas se crearon correctamente en PostgreSQL
"""

import psycopg2

def verificar_tablas():
    try:
        # Conectar a la base de datos
        conn = psycopg2.connect(
            host='localhost',
            port=5432,
            database='turismo_db',
            user='turismo_user',
            password='turismo_pass'
        )
        cursor = conn.cursor()
        
        # Verificar tablas existentes
        cursor.execute("SELECT tablename FROM pg_tables WHERE schemaname = 'public';")
        tables = cursor.fetchall()
        
        print('📋 TABLAS ENCONTRADAS EN LA BASE DE DATOS:')
        print('='*50)
        for table in tables:
            print(f'✅ {table[0]}')
        
        # Contar registros en cada tabla
        cursor.execute('SELECT COUNT(*) FROM usuario;')
        usuarios = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM empresa_turistica;')
        empresas = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM solicitud_visita;')
        solicitudes = cursor.fetchone()[0]
        
        print(f'\n📊 DATOS INSERTADOS:')
        print(f'👥 Usuarios: {usuarios}')
        print(f'🏢 Empresas: {empresas}')
        print(f'📝 Solicitudes: {solicitudes}')
        
        conn.close()
        print('\n✅ ¡BASE DE DATOS CONFIGURADA CORRECTAMENTE!')
        return True
        
    except Exception as e:
        print(f'❌ Error verificando tablas: {e}')
        return False

if __name__ == "__main__":
    verificar_tablas()
