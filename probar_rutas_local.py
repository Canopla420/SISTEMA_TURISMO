#!/usr/bin/env python3
"""
Script para probar las rutas y ver errores específicos
"""

from app import app

def probar_rutas():
    with app.test_client() as client:
        rutas_a_probar = [
            '/',
            '/nueva_visita',
            '/consultar_visitas',
            '/gestionar_empresas',
            '/consultar_empresas'
        ]
        
        print("🔍 PROBANDO RUTAS DEL SERVIDOR...")
        print("=" * 50)
        
        for ruta in rutas_a_probar:
            try:
                response = client.get(ruta)
                print(f"📍 {ruta}")
                print(f"   Status: {response.status_code}")
                
                if response.status_code != 200:
                    print(f"   ❌ Error: {response.status_code}")
                    if response.data:
                        error_text = response.data.decode('utf-8')[:300]
                        print(f"   Detalle: {error_text}...")
                else:
                    print(f"   ✅ OK")
                    
            except Exception as e:
                print(f"   ❌ Excepción: {e}")
            
            print()

if __name__ == "__main__":
    probar_rutas()
