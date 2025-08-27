#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para explorar y administrar la base de datos SQLite
Sistema de Gestión de Visitas Turísticas
"""

import os
import sys
from datetime import datetime, date, time

def explorar_base_datos():
    """Explora el contenido de la base de datos"""
    print("🗃️  EXPLORADOR DE BASE DE DATOS SQLite")
    print("=" * 50)
    
    try:
        # Importar la aplicación
        from app import app, db, EmpresaTuristica, SolicitudVisita, Usuario
        
        with app.app_context():
            print("📊 ESTADÍSTICAS GENERALES:")
            print("-" * 30)
            
            # Contar registros
            empresas_count = EmpresaTuristica.query.count()
            visitas_count = SolicitudVisita.query.count()
            usuarios_count = Usuario.query.count()
            
            print(f"🏢 Empresas: {empresas_count}")
            print(f"📋 Solicitudes de Visita: {visitas_count}")
            print(f"👥 Usuarios: {usuarios_count}")
            
            # Mostrar empresas
            if empresas_count > 0:
                print("\n🏢 EMPRESAS REGISTRADAS:")
                print("-" * 40)
                empresas = EmpresaTuristica.query.all()
                for i, empresa in enumerate(empresas, 1):
                    print(f"{i}. {empresa.nombre}")
                    print(f"   📧 {empresa.email}")
                    print(f"   📍 {empresa.direccion}")
                    print(f"   📞 {empresa.telefono}")
                    print(f"   🏷️  {empresa.categoria}")
                    print(f"   👥 Capacidad: {empresa.capacidad_maxima}")
                    print()
            
            # Mostrar solicitudes de visita
            if visitas_count > 0:
                print("📋 SOLICITUDES DE VISITA:")
                print("-" * 40)
                visitas = SolicitudVisita.query.all()
                for i, visita in enumerate(visitas, 1):
                    print(f"{i}. {visita.nombre_institucion}")
                    print(f"   👤 Responsable: {visita.responsable}")
                    print(f"   📧 {visita.email}")
                    print(f"   👥 Alumnos: {visita.cantidad_alumnos}")
                    print(f"   📅 Fecha: {visita.fecha_visita}")
                    print(f"   🎯 Estado: {visita.estado}")
                    print()
            
            # Mostrar usuarios
            if usuarios_count > 0:
                print("👥 USUARIOS DEL SISTEMA:")
                print("-" * 40)
                usuarios = Usuario.query.all()
                for i, usuario in enumerate(usuarios, 1):
                    print(f"{i}. {usuario.username}")
                    print(f"   📧 {usuario.email}")
                    print(f"   🏷️  {usuario.rol}")
                    print()
                    
    except Exception as e:
        print(f"❌ Error al explorar BD: {e}")
        return False
    
    return True

def agregar_empresa_ejemplo():
    """Agrega una empresa de ejemplo"""
    print("\n➕ AGREGAR NUEVA EMPRESA")
    print("-" * 30)
    
    try:
        from app import app, db, EmpresaTuristica
        
        with app.app_context():
            nueva_empresa = EmpresaTuristica(
                nombre="Parque Ecológico Esperanza",
                descripcion="Reserva natural con senderos interpretativos",
                direccion="Ruta Provincial 70 Km 5",
                telefono="(03496) 421-888",
                email="info@parqueesperanza.com",
                categoria="Turismo Educativo",
                capacidad_maxima=80,
                duracion_visita="2 horas"
            )
            
            db.session.add(nueva_empresa)
            db.session.commit()
            
            print("✅ Empresa agregada exitosamente!")
            
    except Exception as e:
        print(f"❌ Error al agregar empresa: {e}")

def menu_principal():
    """Menú principal del explorador"""
    while True:
        print("\n🔧 MENÚ PRINCIPAL")
        print("-" * 20)
        print("1. 👀 Explorar base de datos")
        print("2. ➕ Agregar empresa de ejemplo")
        print("3. 🌐 Abrir aplicación web")
        print("4. 🚪 Salir")
        
        opcion = input("\nSelecciona una opción (1-4): ").strip()
        
        if opcion == "1":
            explorar_base_datos()
        elif opcion == "2":
            agregar_empresa_ejemplo()
        elif opcion == "3":
            print("\n🌐 Abre tu navegador en: http://localhost:5000")
            print("📝 Para gestionar datos desde la interfaz web")
        elif opcion == "4":
            print("👋 ¡Hasta luego!")
            break
        else:
            print("❌ Opción inválida. Intenta de nuevo.")

if __name__ == "__main__":
    # Verificar que la base de datos existe
    bd_path = os.path.join('instance', 'turismo_local.db')
    
    if not os.path.exists(bd_path):
        print("❌ Base de datos no encontrada.")
        print("🔧 Ejecuta primero: python ejecutar.py")
        sys.exit(1)
    
    menu_principal()
