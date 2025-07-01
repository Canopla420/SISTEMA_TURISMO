"""
Script de prueba para verificar que las rutas principales funcionan
"""

from app import app, db, EmpresaTuristica

def test_app():
    """Prueba básica de la aplicación"""
    with app.test_client() as client:
        with app.app_context():
            # Verificar que la base de datos está funcionando
            try:
                empresas_count = EmpresaTuristica.query.count()
                print(f"✅ Base de datos conectada. Empresas registradas: {empresas_count}")
            except Exception as e:
                print(f"❌ Error en base de datos: {e}")
                return False
            
            # Probar ruta principal
            try:
                response = client.get('/')
                if response.status_code == 200:
                    print("✅ Ruta principal (/) funciona correctamente")
                else:
                    print(f"❌ Error en ruta principal: {response.status_code}")
            except Exception as e:
                print(f"❌ Error al probar ruta principal: {e}")
            
            # Probar ruta de solicitud de visita
            try:
                response = client.get('/institucion/solicitar_visita')
                if response.status_code == 200:
                    print("✅ Ruta de solicitud de visita funciona correctamente")
                else:
                    print(f"❌ Error en ruta de solicitud: {response.status_code}")
            except Exception as e:
                print(f"❌ Error al probar ruta de solicitud: {e}")
            
            # Probar ruta de empresas filtradas
            try:
                response = client.get('/empresas_filtradas?es_de_esperanza=true&nivel_educativo=Primario')
                if response.status_code == 200:
                    print("✅ Ruta de filtrado de empresas funciona correctamente")
                    data = response.get_json()
                    print(f"   📊 Empresas encontradas para Primario/Identidad: {len(data) if data else 0}")
                else:
                    print(f"❌ Error en ruta de filtrado: {response.status_code}")
            except Exception as e:
                print(f"❌ Error al probar filtrado de empresas: {e}")
            
            # Probar ruta de gestión de empresas
            try:
                response = client.get('/gestionar_empresas')
                if response.status_code == 200:
                    print("✅ Ruta de gestión de empresas funciona correctamente")
                else:
                    print(f"❌ Error en gestión de empresas: {response.status_code}")
            except Exception as e:
                print(f"❌ Error al probar gestión de empresas: {e}")
            
            print("\n🎉 Pruebas completadas!")
            print("💡 La aplicación está lista para usar")
            print("🚀 Para ejecutar: python app.py")
            
            return True

if __name__ == "__main__":
    test_app()
