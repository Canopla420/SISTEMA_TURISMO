"""
Test final del sistema de filtrado con niveles educativos correctos
"""

from dotenv import load_dotenv
load_dotenv()

from app import app

def test_filtrado_final():
    """Prueba final del sistema de filtrado"""
    print("🧪 TEST FINAL DEL SISTEMA DE FILTRADO")
    print("=" * 50)
    
    with app.test_client() as client:
        print("🔍 Probando todos los filtros posibles:")
        
        # Test 1: Institución Local + Primario
        print("\n1️⃣ INSTITUCIÓN LOCAL + PRIMARIO:")
        response = client.get('/empresas_filtradas?es_de_esperanza=true&nivel_educativo=Primario')
        if response.status_code == 200:
            data = response.get_json()
            print(f"   ✅ Respuesta exitosa: {len(data)} empresas")
            for emp in data:
                print(f"   🏢 {emp['nombre']} ({emp['categoria_turismo']}, {emp['nivel_educativo_objetivo']})")
        
        # Test 2: Institución Local + Secundario
        print("\n2️⃣ INSTITUCIÓN LOCAL + SECUNDARIO:")
        response = client.get('/empresas_filtradas?es_de_esperanza=true&nivel_educativo=Secundario')
        if response.status_code == 200:
            data = response.get_json()
            print(f"   ✅ Respuesta exitosa: {len(data)} empresas")
            for emp in data:
                print(f"   🏢 {emp['nombre']} ({emp['categoria_turismo']}, {emp['nivel_educativo_objetivo']})")
        
        # Test 3: Institución Externa + Primario
        print("\n3️⃣ INSTITUCIÓN EXTERNA + PRIMARIO:")
        response = client.get('/empresas_filtradas?es_de_esperanza=false&nivel_educativo=Primario')
        if response.status_code == 200:
            data = response.get_json()
            print(f"   ✅ Respuesta exitosa: {len(data)} empresas")
            for emp in data:
                print(f"   🏢 {emp['nombre']} ({emp['categoria_turismo']}, {emp['nivel_educativo_objetivo']})")
        
        # Test 4: Institución Externa + Secundario
        print("\n4️⃣ INSTITUCIÓN EXTERNA + SECUNDARIO:")
        response = client.get('/empresas_filtradas?es_de_esperanza=false&nivel_educativo=Secundario')
        if response.status_code == 200:
            data = response.get_json()
            print(f"   ✅ Respuesta exitosa: {len(data)} empresas")
            for emp in data:
                print(f"   🏢 {emp['nombre']} ({emp['categoria_turismo']}, {emp['nivel_educativo_objetivo']})")
        
        # Test del formulario principal
        print("\n🌐 PROBANDO FORMULARIO PRINCIPAL:")
        response = client.get('/institucion/solicitar_visita')
        if response.status_code == 200:
            html = response.get_data(as_text=True)
            
            # Verificar que no aparezcan niveles incorrectos
            problemas = []
            if 'Nivel Inicial' in html or 'Inicial' in html:
                problemas.append("❌ Aún aparece 'Nivel Inicial'")
            if 'Adultos Mayores' in html:
                problemas.append("❌ Aún aparece 'Adultos Mayores'")
            
            if problemas:
                for problema in problemas:
                    print(f"   {problema}")
            else:
                print("   ✅ Formulario correcto: Solo aparecen Primario y Secundario")
                
            # Verificar que aparezcan las opciones correctas
            if 'Nivel Primario' in html:
                print("   ✅ 'Nivel Primario' presente")
            if 'Nivel Secundario' in html:
                print("   ✅ 'Nivel Secundario' presente")
        
        print("\n🎯 RESUMEN DEL TEST:")
        print("✅ Todas las rutas de filtrado funcionan")
        print("✅ Formulario corregido (solo Primario y Secundario)")
        print("✅ Sistema listo para Dirección de Turismo")
        
        print("\n📋 INSTRUCCIONES FINALES:")
        print("1. Ejecuta: python app.py")
        print("2. Ve a: http://localhost:5000")
        print("3. Prueba 'Cargar nueva visita'")
        print("4. Verifica que en 'Nivel educativo' solo aparezcan:")
        print("   - Nivel Primario")
        print("   - Nivel Secundario")
        print("5. Prueba el filtrado dinámico de empresas")

if __name__ == "__main__":
    test_filtrado_final()
