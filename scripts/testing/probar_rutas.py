"""
Script de prueba para verificar las rutas problemáticas
"""
import requests
import time

# URL base de la aplicación
BASE_URL = "http://127.0.0.1:5000"

def probar_ruta(ruta, nombre):
    """Probar una ruta específica"""
    try:
        print(f"\n🔍 Probando {nombre}...")
        response = requests.get(f"{BASE_URL}{ruta}", timeout=5)
        
        if response.status_code == 200:
            print(f"✅ {nombre}: OK")
            return True
        else:
            print(f"❌ {nombre}: Error {response.status_code}")
            print(f"   Contenido: {response.text[:200]}...")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ {nombre}: Error de conexión - {e}")
        return False

def main():
    print("🚀 Iniciando pruebas de rutas...")
    print("=" * 50)
    
    # Esperar un momento para que el servidor esté listo
    time.sleep(5)
    
    rutas_prueba = [
        ("/", "Página principal"),
        ("/gestionar_empresas", "Gestionar empresas"),
        ("/consultar_visitas", "Consultar visitas"),
        ("/nueva_visita", "Nueva visita"),
        ("/consultar_empresas", "Consultar empresas"),
        ("/todas_empresas", "API todas las empresas"),
        ("/agregar_empresa", "Agregar empresa")
    ]
    
    resultados = []
    for ruta, nombre in rutas_prueba:
        resultado = probar_ruta(ruta, nombre)
        resultados.append((nombre, resultado))
    
    print("\n" + "=" * 50)
    print("📊 RESUMEN DE RESULTADOS:")
    print("=" * 50)
    
    for nombre, resultado in resultados:
        estado = "✅ OK" if resultado else "❌ ERROR"
        print(f"{estado:10} - {nombre}")
    
    exitosas = sum(1 for _, resultado in resultados if resultado)
    total = len(resultados)
    print(f"\n🎯 Rutas exitosas: {exitosas}/{total}")
    
    if exitosas == total:
        print("🎉 ¡Todas las rutas funcionan correctamente!")
    else:
        print("⚠️  Algunas rutas tienen problemas.")

if __name__ == "__main__":
    main()
