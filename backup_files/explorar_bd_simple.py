import sqlite3
import os

# Verificar si las bases de datos existen
bases_de_datos = [
    'instance/turismo.db',
    'instance/turismo_local.db',
    'turismo.db',
    'turismo_local.db'
]

print("🔍 BUSCANDO BASES DE DATOS...")
for bd in bases_de_datos:
    if os.path.exists(bd):
        print(f"✅ Encontrada: {bd}")
        print(f"   Tamaño: {os.path.getsize(bd)} bytes")
        
        # Conectar y mostrar tablas
        try:
            conn = sqlite3.connect(bd)
            cursor = conn.cursor()
            
            # Obtener lista de tablas
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tablas = cursor.fetchall()
            
            print(f"   📋 Tablas ({len(tablas)}):")
            for tabla in tablas:
                cursor.execute(f"SELECT COUNT(*) FROM {tabla[0]}")
                count = cursor.fetchone()[0]
                print(f"      - {tabla[0]}: {count} registros")
            
            # Mostrar algunos datos de muestra
            if tablas:
                print(f"\n   📊 DATOS DE MUESTRA DE {bd}:")
                for tabla in tablas:
                    nombre_tabla = tabla[0]
                    print(f"\n   🗂️ Tabla: {nombre_tabla}")
                    
                    # Obtener estructura
                    cursor.execute(f"PRAGMA table_info({nombre_tabla})")
                    columnas = cursor.fetchall()
                    nombres_cols = [col[1] for col in columnas]
                    print(f"      Columnas: {', '.join(nombres_cols)}")
                    
                    # Obtener hasta 3 registros de muestra
                    cursor.execute(f"SELECT * FROM {nombre_tabla} LIMIT 3")
                    registros = cursor.fetchall()
                    
                    if registros:
                        for i, registro in enumerate(registros, 1):
                            print(f"      Registro {i}:")
                            for j, valor in enumerate(registro):
                                print(f"        {nombres_cols[j]}: {valor}")
                    else:
                        print(f"      (Tabla vacía)")
            
            conn.close()
        except Exception as e:
            print(f"   ❌ Error al leer: {e}")
        
        print("-" * 50)
    else:
        print(f"❌ No encontrada: {bd}")

print("\n✅ Búsqueda completada")
