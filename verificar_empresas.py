"""
Script para verificar y corregir niveles educativos de las empresas
"""

from dotenv import load_dotenv
load_dotenv()

from app import app, db, EmpresaTuristica

def verificar_empresas():
    """Verifica las empresas y sus niveles educativos"""
    with app.app_context():
        print("🔍 VERIFICANDO EMPRESAS EN LA BASE DE DATOS")
        print("=" * 50)
        
        empresas = EmpresaTuristica.query.all()
        print(f"📊 Total de empresas: {len(empresas)}")
        
        if not empresas:
            print("⚠️ No hay empresas en la base de datos")
            return
        
        print("\n📋 LISTADO DE EMPRESAS:")
        niveles_correctos = ['Primario', 'Secundario', 'Ambos']
        empresas_incorrectas = []
        
        for empresa in empresas:
            print(f"🏢 {empresa.nombre}")
            print(f"   📂 Categoría: {empresa.categoria_turismo}")
            print(f"   🎓 Nivel: {empresa.nivel_educativo_objetivo}")
            
            if empresa.nivel_educativo_objetivo not in niveles_correctos:
                empresas_incorrectas.append(empresa)
                print(f"   ❌ NIVEL INCORRECTO: {empresa.nivel_educativo_objetivo}")
            else:
                print(f"   ✅ Nivel correcto")
            print()
        
        if empresas_incorrectas:
            print(f"⚠️ Se encontraron {len(empresas_incorrectas)} empresas con niveles educativos incorrectos")
            print("🔧 Corrigiendo automáticamente...")
            
            for empresa in empresas_incorrectas:
                # Mapear niveles incorrectos a correctos
                if empresa.nivel_educativo_objetivo in ['Inicial', 'nivel inicial', 'inicial']:
                    empresa.nivel_educativo_objetivo = 'Primario'
                    print(f"   📝 {empresa.nombre}: Inicial → Primario")
                elif empresa.nivel_educativo_objetivo in ['Adultos Mayores', 'adultos mayores', 'adultos']:
                    empresa.nivel_educativo_objetivo = 'Ambos'
                    print(f"   📝 {empresa.nombre}: Adultos Mayores → Ambos")
                else:
                    empresa.nivel_educativo_objetivo = 'Ambos'
                    print(f"   📝 {empresa.nombre}: {empresa.nivel_educativo_objetivo} → Ambos")
            
            db.session.commit()
            print("✅ Correcciones aplicadas")
        else:
            print("✅ Todas las empresas tienen niveles educativos correctos")
        
        # Mostrar resumen final
        print("\n📊 RESUMEN FINAL:")
        identidad_primario = EmpresaTuristica.query.filter_by(categoria_turismo='identidad', nivel_educativo_objetivo='Primario').count()
        identidad_secundario = EmpresaTuristica.query.filter_by(categoria_turismo='identidad', nivel_educativo_objetivo='Secundario').count()
        identidad_ambos = EmpresaTuristica.query.filter_by(categoria_turismo='identidad', nivel_educativo_objetivo='Ambos').count()
        
        educativo_primario = EmpresaTuristica.query.filter_by(categoria_turismo='educativo', nivel_educativo_objetivo='Primario').count()
        educativo_secundario = EmpresaTuristica.query.filter_by(categoria_turismo='educativo', nivel_educativo_objetivo='Secundario').count()
        educativo_ambos = EmpresaTuristica.query.filter_by(categoria_turismo='educativo', nivel_educativo_objetivo='Ambos').count()
        
        print("🏛️ TURISMO DE IDENTIDAD:")
        print(f"   📚 Primario: {identidad_primario}")
        print(f"   🎓 Secundario: {identidad_secundario}")
        print(f"   🔄 Ambos: {identidad_ambos}")
        
        print("🎓 TURISMO EDUCATIVO:")
        print(f"   📚 Primario: {educativo_primario}")
        print(f"   🎓 Secundario: {educativo_secundario}")
        print(f"   🔄 Ambos: {educativo_ambos}")
        
        print("\n✅ VERIFICACIÓN COMPLETADA")
        print("🎯 El sistema ahora solo maneja Primario y Secundario como especificado")

if __name__ == "__main__":
    verificar_empresas()
