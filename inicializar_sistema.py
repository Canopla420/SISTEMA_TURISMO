#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script simple para inicializar y poblar la base de datos del sistema de turismo
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db, EmpresaTuristica, SolicitudVisita, ConsultaEmpresa, Usuario
from datetime import datetime, date, time

def crear_base_datos():
    """Crea las tablas de la base de datos"""
    print("🏗️ Creando tablas de la base de datos...")
    
    with app.app_context():
        try:
            # Eliminar todas las tablas existentes
            db.drop_all()
            print("   ✅ Tablas anteriores eliminadas")
            
            # Crear todas las tablas
            db.create_all()
            print("   ✅ Nuevas tablas creadas")
            
            return True
        except Exception as e:
            print(f"   ❌ Error al crear tablas: {e}")
            return False

def agregar_datos_prueba():
    """Agrega algunos datos de prueba"""
    print("📝 Agregando datos de prueba...")
    
    with app.app_context():
        try:
            # Empresas de prueba
            empresas_datos = [
                {
                    'nombre': 'Aventuras del Norte',
                    'email': 'info@aventurasdelnorte.com',
                    'telefono': '3794-123456',
                    'categoria': 'Turismo Aventura'
                },
                {
                    'nombre': 'Hoteles Esperanza',
                    'email': 'reservas@hotelesperanza.com',
                    'telefono': '3794-789012',
                    'categoria': 'Hotelería'
                },
                {
                    'nombre': 'Tours Culturales Corrientes',
                    'email': 'contacto@tourscorrientes.com',
                    'telefono': '3794-345678',
                    'categoria': 'Turismo Cultural'
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
            
            db.session.flush()  # Para obtener los IDs
            print(f"   ✅ {len(empresas_creadas)} empresas creadas")
            
            # Solicitudes de visita de prueba
            visitas_datos = [
                {
                    'nombre_institucion': 'Escuela N°1',
                    'responsable': 'Juan Pérez',
                    'telefono': '3794-111222',
                    'email': 'juan.perez@email.com',
                    'cantidad_alumnos': 30,
                    'edad_alumnos': '12-13',
                    'discapacidad': 'No',
                    'empresas_seleccionadas': str(empresas_creadas[0].id),
                    'fecha_visita': date(2024, 2, 15),
                    'hora_grupo1': time(10, 30),
                    'hora_grupo2': None,
                    'observaciones': 'Interesado en tour de aventura',
                    'estado': 'Pendiente'
                },
                {
                    'nombre_institucion': 'Colegio San Martín',
                    'responsable': 'María García',
                    'telefono': '3794-333444',
                    'email': 'maria.garcia@email.com',
                    'cantidad_alumnos': 25,
                    'edad_alumnos': '14-15',
                    'discapacidad': 'No',
                    'empresas_seleccionadas': str(empresas_creadas[1].id),
                    'fecha_visita': date(2024, 2, 20),
                    'hora_grupo1': time(14, 0),
                    'hora_grupo2': None,
                    'observaciones': 'Consulta por reserva de habitación',
                    'estado': 'Confirmada'
                },
                {
                    'nombre_institucion': 'Instituto Técnico',
                    'responsable': 'Carlos López',
                    'telefono': '3794-555666',
                    'email': 'carlos.lopez@email.com',
                    'cantidad_alumnos': 40,
                    'edad_alumnos': '16-17',
                    'discapacidad': 'Sí',
                    'empresas_seleccionadas': str(empresas_creadas[2].id),
                    'fecha_visita': date(2024, 2, 25),
                    'hora_grupo1': time(16, 15),
                    'hora_grupo2': None,
                    'observaciones': 'Tour para grupo familiar',
                    'estado': 'Pendiente'
                }
            ]

            for datos in visitas_datos:
                visita = SolicitudVisita(
                    nombre_institucion=datos['nombre_institucion'],
                    responsable=datos['responsable'],
                    telefono=datos['telefono'],
                    email=datos['email'],
                    cantidad_alumnos=datos['cantidad_alumnos'],
                    edad_alumnos=datos['edad_alumnos'],
                    discapacidad=datos['discapacidad'],
                    empresas_seleccionadas=datos['empresas_seleccionadas'],
                    fecha_visita=datos['fecha_visita'],
                    hora_grupo1=datos['hora_grupo1'],
                    hora_grupo2=datos['hora_grupo2'],
                    observaciones=datos['observaciones'],
                    estado=datos['estado']
                )
                db.session.add(visita)
            
            print(f"   ✅ {len(visitas_datos)} solicitudes de visita creadas")
            
            # Consultas a empresas de prueba
            consultas_datos = [
                {
                    'empresa_id': empresas_creadas[0].id,
                    'fecha_consulta': date(2024, 2, 10),
                    'hora_consulta': time(9, 0),
                    'comentarios': 'Consulta sobre disponibilidad para grupo de 20 personas',
                    'estado': 'Pendiente'
                },
                {
                    'empresa_id': empresas_creadas[1].id,
                    'fecha_consulta': date(2024, 2, 12),
                    'hora_consulta': time(11, 30),
                    'comentarios': 'Información sobre tarifas de temporada alta',
                    'estado': 'Pendiente'
                }
            ]
            
            for datos in consultas_datos:
                consulta = ConsultaEmpresa(
                    empresa_id=datos['empresa_id'],
                    fecha_consulta=datos['fecha_consulta'],
                    hora_consulta=datos['hora_consulta'],
                    comentarios=datos['comentarios'],
                    estado=datos['estado']
                )
                db.session.add(consulta)
            
            print(f"   ✅ {len(consultas_datos)} consultas a empresas creadas")
            
            # Usuario administrador
            admin = Usuario(
                username='admin',
                email='admin@sistema-turismo.com'
            )
            db.session.add(admin)
            print("   ✅ Usuario administrador creado")
            
            # Confirmar cambios
            db.session.commit()
            print("   ✅ Todos los datos guardados en la base de datos")
            
            return True
            
        except Exception as e:
            print(f"   ❌ Error al agregar datos: {e}")
            db.session.rollback()
            return False

def mostrar_resumen():
    """Muestra un resumen de los datos en la base de datos"""
    print("\n📊 RESUMEN DE LA BASE DE DATOS:")
    print("=" * 50)
    
    with app.app_context():
        try:
            empresas_count = EmpresaTuristica.query.count()
            visitas_count = SolicitudVisita.query.count()
            consultas_count = ConsultaEmpresa.query.count()
            usuarios_count = Usuario.query.count()
            
            print(f"🏢 Empresas Turísticas: {empresas_count}")
            print(f"🎯 Solicitudes de Visita: {visitas_count}")
            print(f"📧 Consultas a Empresas: {consultas_count}")
            print(f"👥 Usuarios: {usuarios_count}")
            
            if empresas_count > 0:
                print(f"\n🏢 Lista de Empresas:")
                empresas = EmpresaTuristica.query.all()
                for empresa in empresas:
                    print(f"   - {empresa.nombre} ({empresa.categoria}) - {empresa.email}")
            
            if visitas_count > 0:
                print(f"\n🎯 Últimas Solicitudes de Visita:")
                visitas = SolicitudVisita.query.order_by(SolicitudVisita.fecha_solicitud.desc()).limit(3).all()
                for visita in visitas:
                    print(f"   - {visita.nombre_institucion} ({visita.responsable}) - Estado: {visita.estado}")
            
        except Exception as e:
            print(f"❌ Error al mostrar resumen: {e}")

def main():
    """Función principal"""
    print("🏛️ SISTEMA DE TURISMO - INICIALIZADOR DE BASE DE DATOS")
    print("=" * 60)
    
    # Crear base de datos
    if not crear_base_datos():
        print("❌ Error al crear la base de datos. Abortando.")
        return
    
    # Agregar datos de prueba
    if not agregar_datos_prueba():
        print("❌ Error al agregar datos de prueba. Abortando.")
        return
    
    # Mostrar resumen
    mostrar_resumen()
    
    print("\n✅ ¡Inicialización completada exitosamente!")
    print("💡 Ahora puedes:")
    print("   1. Ejecutar el servidor: python app.py")
    print("   2. Ver los datos en: http://localhost:5000/ver_datos")
    print("   3. Usar el sistema en: http://localhost:5000")

if __name__ == "__main__":
    main()
