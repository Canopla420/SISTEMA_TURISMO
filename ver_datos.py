#!/usr/bin/env python3
"""
Script simple para ver datos de la base de datos
"""

from app import app, db, EmpresaTuristica, SolicitudVisita, Usuario

def mostrar_datos():
    with app.app_context():
        print("📊 CONTENIDO DE LA BASE DE DATOS")
        print("=" * 40)
        
        # Empresas
        empresas = EmpresaTuristica.query.all()
        print(f"\n🏢 EMPRESAS ({len(empresas)}):")
        for empresa in empresas:
            print(f"  • {empresa.nombre}")
            print(f"    📧 {empresa.email}")
            print(f"    🏷️  {empresa.categoria}")
        
        # Solicitudes
        visitas = SolicitudVisita.query.all()
        print(f"\n📋 SOLICITUDES ({len(visitas)}):")
        for visita in visitas:
            print(f"  • {visita.nombre_institucion}")
            print(f"    👤 {visita.responsable}")
            print(f"    🎯 {visita.estado}")
        
        # Usuarios
        usuarios = Usuario.query.all()
        print(f"\n👥 USUARIOS ({len(usuarios)}):")
        for usuario in usuarios:
            print(f"  • {usuario.username} ({usuario.rol})")

if __name__ == "__main__":
    mostrar_datos()
