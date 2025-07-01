"""
Script de diagnóstico para verificar el sistema de filtrado de empresas
"""

from app import app, db, EmpresaTuristica

def diagnosticar_sistema():
    """Diagnostica el estado del sistema"""
    with app.app_context():
        print("🔍 DIAGNÓSTICO DEL SISTEMA DE FILTRADO")
        print("=" * 50)
        
        # 1. Verificar base de datos
        print("\n1️⃣ VERIFICANDO BASE DE DATOS:")
        try:
            total_empresas = EmpresaTuristica.query.count()
            print(f"   📊 Total de empresas: {total_empresas}")
            
            if total_empresas == 0:
                print("   ⚠️ No hay empresas en la base de datos")
                print("   💡 Creando empresas de ejemplo...")
                crear_empresas_ejemplo()
                total_empresas = EmpresaTuristica.query.count()
                print(f"   ✅ Empresas creadas: {total_empresas}")
            
            # Mostrar empresas por categoría
            identidad = EmpresaTuristica.query.filter_by(categoria_turismo='identidad').count()
            educativo = EmpresaTuristica.query.filter_by(categoria_turismo='educativo').count()
            
            print(f"   🏛️ Turismo de Identidad: {identidad}")
            print(f"   🎓 Turismo Educativo: {educativo}")
            
        except Exception as e:
            print(f"   ❌ Error en base de datos: {e}")
            return False
        
        # 2. Verificar ruta de filtrado
        print("\n2️⃣ VERIFICANDO RUTA DE FILTRADO:")
        with app.test_client() as client:
            # Probar filtro para institución local
            response = client.get('/empresas_filtradas?es_de_esperanza=true&nivel_educativo=Primario')
            if response.status_code == 200:
                data = response.get_json()
                print(f"   ✅ Filtro Local/Primario: {len(data)} empresas")
                if data:
                    print(f"      📋 Ejemplo: {data[0]['nombre']}")
            else:
                print(f"   ❌ Error en filtro local: {response.status_code}")
            
            # Probar filtro para institución externa
            response = client.get('/empresas_filtradas?es_de_esperanza=false&nivel_educativo=Secundario')
            if response.status_code == 200:
                data = response.get_json()
                print(f"   ✅ Filtro Externa/Secundario: {len(data)} empresas")
                if data:
                    print(f"      📋 Ejemplo: {data[0]['nombre']}")
            else:
                print(f"   ❌ Error en filtro externo: {response.status_code}")
        
        # 3. Verificar formulario
        print("\n3️⃣ VERIFICANDO FORMULARIO:")
        with app.test_client() as client:
            response = client.get('/institucion/solicitar_visita')
            if response.status_code == 200:
                html = response.get_data(as_text=True)
                checks = {
                    'tipo_institucion': 'id="tipo_institucion"' in html,
                    'nivel_educativo': 'id="nivel_educativo"' in html,
                    'empresas_container': 'id="empresas-container"' in html,
                    'filtro_js': 'filtro_empresas.js' in html
                }
                
                for check, result in checks.items():
                    status = "✅" if result else "❌"
                    print(f"   {status} {check}: {'OK' if result else 'FALTA'}")
            else:
                print(f"   ❌ Error en formulario: {response.status_code}")
        
        print("\n🎯 CONCLUSIÓN:")
        print("   Si todos los checks están en ✅, el sistema debería funcionar.")
        print("   Si hay ❌, revisa los archivos correspondientes.")
        print("\n💡 PRUEBA MANUAL:")
        print("   1. Ejecuta: python app.py")
        print("   2. Ve a: http://localhost:5000")
        print("   3. Abre 'Cargar nueva visita'")
        print("   4. Abre las herramientas de desarrollador (F12)")
        print("   5. Ve a la pestaña 'Console' para ver los logs")
        print("   6. Selecciona tipo de institución y nivel educativo")
        
        return True

def crear_empresas_ejemplo():
    """Crea empresas de ejemplo si no existen"""
    try:
        # Empresas para Turismo de Identidad (instituciones locales)
        empresas_identidad = [
            {
                'nombre': 'Museo de la Colonización',
                'correo': 'museo@esperanza.gov.ar',
                'telefono': '03496-123456',
                'direccion': 'Av. San Martín 123, Esperanza',
                'servicios_ofrecidos': 'Visitas guiadas, exhibiciones interactivas, talleres educativos',
                'descripcion': 'Museo histórico sobre la colonización de Esperanza',
                'categoria_turismo': 'identidad',
                'nivel_educativo_objetivo': 'Ambos',
                'capacidad_maxima': 50,
                'costo_por_persona': 100.0,
                'requiere_reserva': True
            },
            {
                'nombre': 'Casa de la Cultura',
                'correo': 'cultura@esperanza.gov.ar',
                'telefono': '03496-123457',
                'direccion': 'Calle Mitre 456, Esperanza',
                'servicios_ofrecidos': 'Talleres artísticos, exposiciones, actividades culturales',
                'descripcion': 'Centro cultural de la ciudad',
                'categoria_turismo': 'identidad',
                'nivel_educativo_objetivo': 'Primario',
                'capacidad_maxima': 30,
                'costo_por_persona': 50.0,
                'requiere_reserva': True
            }
        ]
        
        # Empresas para Turismo Educativo (instituciones externas)
        empresas_educativo = [
            {
                'nombre': 'Granja Educativa Los Ñandúes',
                'correo': 'info@granjalosnanques.com',
                'telefono': '03496-789012',
                'direccion': 'Ruta 70 Km 15, Esperanza',
                'servicios_ofrecidos': 'Actividades rurales, contacto con animales, talleres de granja',
                'descripcion': 'Granja educativa para conocer la vida rural',
                'categoria_turismo': 'educativo',
                'nivel_educativo_objetivo': 'Primario',
                'capacidad_maxima': 40,
                'costo_por_persona': 200.0,
                'requiere_reserva': True
            },
            {
                'nombre': 'Industrias Santa Fe Tours',
                'correo': 'tours@industriassf.com',
                'telefono': '03496-345678',
                'direccion': 'Parque Industrial, Esperanza',
                'servicios_ofrecidos': 'Visitas a plantas industriales, charlas técnicas',
                'descripcion': 'Recorridos educativos por industrias locales',
                'categoria_turismo': 'educativo',
                'nivel_educativo_objetivo': 'Secundario',
                'capacidad_maxima': 25,
                'costo_por_persona': 150.0,
                'requiere_reserva': True
            }
        ]
        
        # Crear las empresas
        for empresa_data in empresas_identidad + empresas_educativo:
            # Verificar si ya existe
            existe = EmpresaTuristica.query.filter_by(nombre=empresa_data['nombre']).first()
            if not existe:
                empresa = EmpresaTuristica(**empresa_data)
                db.session.add(empresa)
        
        db.session.commit()
        print("   ✅ Empresas de ejemplo creadas")
        
    except Exception as e:
        print(f"   ❌ Error al crear empresas: {e}")
        db.session.rollback()

if __name__ == "__main__":
    diagnosticar_sistema()
