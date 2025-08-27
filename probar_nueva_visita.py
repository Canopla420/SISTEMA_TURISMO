#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script para probar específicamente la funcionalidad de nueva_visita
"""

import sys
import os
if sys.platform.startswith('win'):
    os.environ['PYTHONIOENCODING'] = 'utf-8'

# Añadir el directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db

def test_nueva_visita():
    """Probar la ruta de nueva_visita"""
    with app.test_client() as client:
        print("🧪 Probando acceso a /nueva_visita...")
        
        try:
            response = client.get('/nueva_visita')
            print(f"✅ Status: {response.status_code}")
            
            if response.status_code == 200:
                print("✅ La página nueva_visita se carga correctamente")
                return True
            else:
                print(f"❌ Error al cargar nueva_visita: {response.status_code}")
                print(f"❌ Respuesta: {response.data.decode()}")
                return False
                
        except Exception as e:
            print(f"❌ Excepción al probar nueva_visita: {e}")
            return False

def test_crear_visita():
    """Probar envío de formulario de nueva visita"""
    with app.test_client() as client:
        print("\n🧪 Probando envío de formulario...")
        
        # Datos de prueba que coinciden con los campos del formulario
        datos_prueba = {
            'nombre_institucion': 'Escuela de Prueba',
            'localidad': 'Esperanza',
            'contacto_principal': 'Juan Pérez',
            'telefono_contacto_principal': '123456789',
            'correo_institucional': 'juan@escuela.com',
            'cantidad_alumnos': '25',
            'edad_alumnos': '12-13 años',
            'discapacidad': 'No',
            'fecha_visita': '2025-09-15',
            'observaciones': 'Visita de prueba'
        }
        
        try:
            response = client.post('/institucion/solicitar_visita', data=datos_prueba)
            print(f"✅ Status: {response.status_code}")
            
            if response.status_code == 302:  # Redirect
                print("✅ Formulario enviado correctamente (redirect)")
                return True
            elif response.status_code == 200:
                print("✅ Formulario procesado")
                return True
            else:
                print(f"❌ Error al enviar formulario: {response.status_code}")
                print(f"❌ Respuesta: {response.data.decode()}")
                return False
                
        except Exception as e:
            print(f"❌ Excepción al enviar formulario: {e}")
            return False

if __name__ == '__main__':
    print("🔍 PROBANDO FUNCIONALIDAD NUEVA_VISITA")
    print("=" * 50)
    
    with app.app_context():
        # Asegurar que las tablas existan
        db.create_all()
        
        # Probar acceso a la página
        test1 = test_nueva_visita()
        
        # Probar envío de formulario
        test2 = test_crear_visita()
        
        print("\n" + "=" * 50)
        if test1 and test2:
            print("✅ TODAS LAS PRUEBAS PASARON")
        else:
            print("❌ ALGUNAS PRUEBAS FALLARON")
