"""
Test simple para verificar el filtrado de empresas
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db, EmpresaTuristica

def test_filtrado_basico():
    """Test básico del sistema de filtrado"""
    print("🧪 INICIANDO TESTS BÁSICOS")
    
    with app.app_context():
        # Crear base de datos si no existe
        db.create_all()
        
        # Verificar si hay empresas
        count = EmpresaTuristica.query.count()
        print(f"📊 Empresas en BD: {count}")
        
        if count == 0:
            print("➕ Creando empresas de prueba...")
            # Crear empresa de identidad
            empresa1 = EmpresaTuristica(
                nombre="Museo Test",
                correo="test@museo.com",
                categoria_turismo="identidad",
                nivel_educativo_objetivo="Primario",
                activa=True
            )
            
            # Crear empresa educativa
            empresa2 = EmpresaTuristica(
                nombre="Granja Test",
                correo="test@granja.com",
                categoria_turismo="educativo",
                nivel_educativo_objetivo="Secundario",
                activa=True
            )
            
            db.session.add(empresa1)
            db.session.add(empresa2)
            db.session.commit()
            print("✅ Empresas de prueba creadas")
        
        # Test de filtrado
        with app.test_client() as client:
            print("🔍 Probando filtros...")
            
            # Test 1: Instituciones locales + Primario
            response = client.get('/empresas_filtradas?es_de_esperanza=true&nivel_educativo=Primario')
            if response.status_code == 200:
                data = response.get_json()
                print(f"✅ Local/Primario: {len(data)} empresas")
                for emp in data:
                    print(f"   - {emp['nombre']} ({emp['categoria_turismo']})")
            else:
                print(f"❌ Error Local/Primario: {response.status_code}")
            
            # Test 2: Instituciones externas + Secundario
            response = client.get('/empresas_filtradas?es_de_esperanza=false&nivel_educativo=Secundario')
            if response.status_code == 200:
                data = response.get_json()
                print(f"✅ Externa/Secundario: {len(data)} empresas")
                for emp in data:
                    print(f"   - {emp['nombre']} ({emp['categoria_turismo']})")
            else:
                print(f"❌ Error Externa/Secundario: {response.status_code}")
        
        print("\n🎯 INSTRUCCIONES PARA PRUEBA MANUAL:")
        print("1. Ejecuta: python app.py")
        print("2. Ve a: http://localhost:5000/institucion/solicitar_visita")
        print("3. Abre herramientas de desarrollador (F12) → Console")
        print("4. Completa los campos:")
        print("   - Tipo de institución: Local o Externa")
        print("   - Nivel educativo: Primario o Secundario")
        print("5. Observa los logs en la consola del navegador")
        print("6. Las empresas deberían aparecer automáticamente")

if __name__ == "__main__":
    test_filtrado_basico()
