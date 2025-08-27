#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para ejecutar la aplicación con SQLite
Sistema de Gestión de Visitas Turísticas - Esperanza
"""

import os
import sys
import subprocess

def ejecutar_aplicacion():
    """Ejecuta la aplicación Flask con SQLite"""
    print("🚀 EJECUTANDO SISTEMA DE TURISMO")
    print("=" * 40)
    
    # Verificar si existe la base de datos
    bd_path = os.path.join('instance', 'turismo_local.db')
    
    if not os.path.exists(bd_path):
        print("⚠️  Base de datos no encontrada. Configurando automáticamente...")
        try:
            # Configuración simple directa
            from app import app, db, EmpresaTuristica, SolicitudVisita, Usuario
            
            with app.app_context():
                # Crear todas las tablas
                db.create_all()
                print("✅ Tablas creadas exitosamente")
                
                # Verificar si ya hay datos
                if EmpresaTuristica.query.count() > 0:
                    print("ℹ️  Ya existen datos en la base de datos")
                else:
                    print("📋 Agregando datos básicos...")
                    # Agregar empresas básicas con los campos correctos
                    empresas_ejemplo = [
                        EmpresaTuristica(
                            nombre="Museo Histórico Esperanza",
                            descripcion="Museo principal de la ciudad",
                            direccion="Av. San Martín 402",
                            telefono="(03496) 420-789",
                            email="museo@esperanza.gov.ar",
                            categoria="Turismo de Identidad",
                            capacidad_maxima=40,
                            duracion_visita="90 minutos"
                        ),
                        EmpresaTuristica(
                            nombre="Centro Cultural Casa Diefenbach",
                            descripcion="Centro cultural histórico",
                            direccion="Calle 25 de Mayo 356",
                            telefono="(03496) 420-123",
                            email="cultura@esperanza.gov.ar",
                            categoria="Turismo de Identidad",
                            capacidad_maxima=60,
                            duracion_visita="75 minutos"
                        )
                    ]
                    
                    for empresa in empresas_ejemplo:
                        db.session.add(empresa)
                    
                    db.session.commit()
                    print(f"✅ {len(empresas_ejemplo)} empresas creadas")
                    
        except Exception as e:
            print(f"❌ Error al configurar: {e}")
            return False
    else:
        print("✅ Base de datos encontrada")
    
    # Ejecutar la aplicación
    print("\n🌐 Iniciando servidor Flask...")
    print("📱 La aplicación estará disponible en: http://localhost:5000")
    print("🛑 Para detener el servidor, presiona Ctrl+C")
    print("-" * 40)
    
    try:
        # Importar y ejecutar la aplicación
        from app import app
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n\n🛑 Servidor detenido por el usuario")
    except Exception as e:
        print(f"\n❌ Error al ejecutar la aplicación: {e}")
        return False
    
    return True

if __name__ == "__main__":
    ejecutar_aplicacion()
