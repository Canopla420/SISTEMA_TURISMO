#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para probar que las empresas se muestren correctamente en nueva visita
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db, EmpresaTuristica, SolicitudVisita

def probar_flujo_empresas():
    """Prueba el flujo completo de empresas"""
    print("🧪 PROBANDO FLUJO DE EMPRESAS EN NUEVA VISITA")
    print("=" * 60)
    
    with app.app_context():
        try:
            # 1. Limpiar datos existentes
            print("🧹 Limpiando datos existentes...")
            SolicitudVisita.query.delete()
            EmpresaTuristica.query.delete()
            db.session.commit()
            
            # 2. Crear empresas de prueba
            print("🏢 Creando empresas de prueba...")
            empresas_datos = [
                {
                    'nombre': 'Turismo Aventura Esperanza',
                    'email': 'aventura@esperanza.com',
                    'telefono': '3794-123456',
                    'categoria': 'Turismo Aventura'
                },
                {
                    'nombre': 'Hotel Plaza Central',
                    'email': 'reservas@plazacentral.com',
                    'telefono': '3794-789012',
                    'categoria': 'Hotelería'
                },
                {
                    'nombre': 'Tours Culturales del Litoral',
                    'email': 'info@tourslitoral.com',
                    'telefono': '3794-345678',
                    'categoria': 'Turismo Cultural'
                },
                {
                    'nombre': 'Restaurante Típico Regional',
                    'email': 'contacto@tipicoreg.com',
                    'telefono': '3794-555666',
                    'categoria': 'Gastronomía'
                }
            ]
            
            empresas_creadas = []
            for datos in empresas_datos:
                empresa = EmpresaTuristica(
                    nombre=datos['nombre'],
                    email=datos['email'],
                    telefono=datos['telefono'],
                    categoria=datos['categoria']
                )
                db.session.add(empresa)
                empresas_creadas.append(empresa)
            
            db.session.commit()
            print(f"   ✅ {len(empresas_creadas)} empresas creadas")
            
            # 3. Mostrar empresas creadas
            print("\n📋 EMPRESAS DISPONIBLES:")
            for i, empresa in enumerate(empresas_creadas, 1):
                print(f"   {i}. {empresa.nombre} (ID: {empresa.id})")
                print(f"      📧 {empresa.email}")
                print(f"      📞 {empresa.telefono}")
                print(f"      📂 {empresa.categoria}")
                print()
            
            # 4. Simular una solicitud de visita con empresas seleccionadas
            print("🎯 Creando solicitud de visita de prueba...")
            from datetime import date, time
            
            # Seleccionar las primeras 2 empresas
            empresas_seleccionadas = empresas_creadas[:2]
            empresas_ids = [str(empresa.id) for empresa in empresas_seleccionadas]
            empresas_ids_str = ','.join(empresas_ids)
            
            visita_prueba = SolicitudVisita(
                nombre_institucion='Escuela Nacional de Esperanza',
                nombre_visitante='Juan Pérez',
                email_visitante='juan.perez@escuela.com',
                telefono_visitante='3794-111222',
                fecha_visita=date(2024, 3, 15),
                hora_visita=time(10, 30),
                observaciones='Visita educativa para 30 alumnos de 5to año',
                empresas_seleccionadas=empresas_ids_str,
                estado='Pendiente'
            )
            
            db.session.add(visita_prueba)
            db.session.commit()
            
            print(f"   ✅ Visita creada con empresas: {empresas_ids_str}")
            
            # 5. Probar la función de conversión de nombres
            from app import obtener_nombres_empresas
            nombres_empresas = obtener_nombres_empresas(empresas_ids_str)
            print(f"   📝 Nombres de empresas: {nombres_empresas}")
            
            # 6. Verificar datos en consultar visitas
            print("\n📊 VERIFICANDO DATOS EN CONSULTA:")
            visitas = SolicitudVisita.query.all()
            for visita in visitas:
                print(f"   🎯 Visita ID: {visita.id}")
                print(f"      Institución: {visita.nombre_institucion}")
                print(f"      Empresas (IDs): {visita.empresas_seleccionadas}")
                nombres = obtener_nombres_empresas(visita.empresas_seleccionadas)
                print(f"      Empresas (nombres): {nombres}")
                print()
            
            print("✅ ¡Prueba completada exitosamente!")
            print("\n💡 Ahora puedes:")
            print("   1. Ir a http://localhost:5000/nueva_visita")
            print("   2. Ver las empresas listadas automáticamente")
            print("   3. Seleccionar empresas y enviar el formulario")
            print("   4. Ver el resultado en http://localhost:5000/consultar_visitas")
            print("   5. Ver todos los datos en http://localhost:5000/ver_datos")
            
        except Exception as e:
            print(f"❌ Error durante la prueba: {e}")
            db.session.rollback()

if __name__ == "__main__":
    probar_flujo_empresas()
