import sqlite3
import os

def actualizar_campos_visita():
    # Ruta a la base de datos
    db_path = os.path.join('instance', 'turismo.db')
    
    # Conectar a la base de datos
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Lista de columnas a agregar
    nuevas_columnas = [
        ('contacto_principal', 'VARCHAR(100)'),
        ('telefono_contacto_principal', 'VARCHAR(50)'),
        ('relacion_contacto', 'VARCHAR(100)'),
        ('contacto_suplente', 'VARCHAR(100)'),
        ('telefono_contacto_suplente', 'VARCHAR(50)'),
        ('nivel_educativo', 'VARCHAR(20)')
    ]
    
    try:
        # Agregar cada columna nueva si no existe
        for columna, tipo in nuevas_columnas:
            try:
                cursor.execute(f'ALTER TABLE solicitud_visita ADD COLUMN {columna} {tipo}')
                print(f'✅ Columna {columna} agregada correctamente')
            except sqlite3.OperationalError as e:
                if 'duplicate column name' in str(e):
                    print(f'ℹ️ La columna {columna} ya existe')
                else:
                    print(f'❌ Error al agregar columna {columna}: {e}')
        
        # Confirmar los cambios
        conn.commit()
        print('✅ Base de datos actualizada correctamente')
        
    except Exception as e:
        print(f'❌ Error: {e}')
        conn.rollback()
    
    finally:
        # Cerrar la conexión
        conn.close()

if __name__ == '__main__':
    print('🔄 Actualizando campos de visita en la base de datos...')
    actualizar_campos_visita()