#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para mostrar todos los datos almacenados en la base de datos del sistema de turismo
"""

import sqlite3
import os
from datetime import datetime

def conectar_bd():
    """Conecta a la base de datos SQLite"""
    db_paths = ['instance/turismo.db', 'instance/turismo_local.db', 'turismo.db', 'turismo_local.db']
    
    for db_path in db_paths:
        if os.path.exists(db_path):
            print(f"✅ Usando base de datos: {db_path}")
            return sqlite3.connect(db_path)
    
    print(f"❌ Base de datos no encontrada en: {db_paths}")
    return None

def mostrar_tabla(cursor, nombre_tabla):
    """Muestra todos los datos de una tabla específica"""
    print(f"\n{'='*60}")
    print(f"📋 TABLA: {nombre_tabla.upper()}")
    print(f"{'='*60}")
    
    try:
        # Obtener información de columnas
        cursor.execute(f"PRAGMA table_info({nombre_tabla})")
        columnas = cursor.fetchall()
        
        if not columnas:
            print(f"⚠️ La tabla {nombre_tabla} no existe o está vacía")
            return
        
        # Mostrar estructura de la tabla
        print("\n📝 Estructura de la tabla:")
        for col in columnas:
            print(f"  - {col[1]} ({col[2]})")
        
        # Obtener datos
        cursor.execute(f"SELECT * FROM {nombre_tabla}")
        filas = cursor.fetchall()
        
        if not filas:
            print(f"\n📭 La tabla {nombre_tabla} está vacía")
            return
        
        print(f"\n📊 Datos almacenados ({len(filas)} registros):")
        print("-" * 80)
        
        # Nombres de columnas
        nombres_columnas = [col[1] for col in columnas]
        
        # Mostrar encabezados
        encabezado = " | ".join([f"{col:15}" for col in nombres_columnas])
        print(encabezado)
        print("-" * len(encabezado))
        
        # Mostrar datos
        for i, fila in enumerate(filas, 1):
            datos_fila = " | ".join([f"{str(dato)[:15]:15}" for dato in fila])
            print(f"{datos_fila}")
            
            # Mostrar detalles completos cada 5 filas o si hay campos largos
            if i % 5 == 0 or any(len(str(dato)) > 15 for dato in fila):
                print(f"\n🔍 Detalles del registro {i}:")
                for j, col in enumerate(nombres_columnas):
                    print(f"  {col}: {fila[j]}")
                print("-" * 40)
        
    except sqlite3.Error as e:
        print(f"❌ Error al consultar la tabla {nombre_tabla}: {e}")

def main():
    """Función principal"""
    print("🏛️ SISTEMA DE TURISMO - VISUALIZADOR DE BASE DE DATOS")
    print(f"📅 Fecha y hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    # Conectar a la base de datos
    conn = conectar_bd()
    if not conn:
        return
    
    cursor = conn.cursor()
    
    try:
        # Obtener lista de tablas
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tablas = cursor.fetchall()
        
        if not tablas:
            print("❌ No se encontraron tablas en la base de datos")
            return
        
        print(f"📁 Tablas encontradas: {len(tablas)}")
        for tabla in tablas:
            print(f"  - {tabla[0]}")
        
        # Mostrar datos de cada tabla
        tablas_principales = ['empresas', 'visitas', 'itinerarios', 'consultas_empresas']
        
        for tabla_info in tablas:
            nombre_tabla = tabla_info[0]
            if nombre_tabla in tablas_principales:
                mostrar_tabla(cursor, nombre_tabla)
        
        # Mostrar resumen final
        print(f"\n{'='*60}")
        print("📈 RESUMEN DE DATOS")
        print(f"{'='*60}")
        
        for tabla_info in tablas:
            nombre_tabla = tabla_info[0]
            if nombre_tabla in tablas_principales:
                cursor.execute(f"SELECT COUNT(*) FROM {nombre_tabla}")
                cantidad = cursor.fetchone()[0]
                print(f"  📊 {nombre_tabla}: {cantidad} registros")
        
    except sqlite3.Error as e:
        print(f"❌ Error al acceder a la base de datos: {e}")
    
    finally:
        conn.close()
        print(f"\n✅ Consulta completada exitosamente")
        print("💡 Para ver estos datos en tiempo real, visita: http://localhost:5000/ver_datos")

if __name__ == "__main__":
    main()
