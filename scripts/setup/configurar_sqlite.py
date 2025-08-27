#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para configurar base de datos SQLite local
Sistema de Gestión de Visitas Turísticas - Esperanza
"""

import os
import sys
from datetime import datetime, date, time

def configurar_sqlite():
    """Configura la base de datos SQLite y ejecuta la aplicación"""
    print("🚀 CONFIGURANDO BASE DE DATOS SQLite LOCAL")
    print("=" * 50)
    
    # 1. Crear directorio instance si no existe
    print("📁 Creando directorio instance...")
    instance_dir = 'instance'
    if not os.path.exists(instance_dir):
        os.makedirs(instance_dir)
        print("   ✅ Directorio instance creado")
    else:
        print("   ℹ️  Directorio instance ya existe")
    
    # 2. Importar la aplicación
    print("\n💾 Configurando base de datos...")
    try:
        from app import app, db, EmpresaTuristica, SolicitudVisita, Usuario
        
        with app.app_context():
            # Crear todas las tablas
            db.create_all()
            print("   ✅ Tablas creadas exitosamente")
            
            # Verificar si ya hay datos
            if EmpresaTuristica.query.count() > 0:
                print("   ℹ️  Ya existen datos en la base de datos")
            else:
                print("   📋 Poblando con datos de ejemplo...")
                poblar_datos_ejemplo()
                
    except Exception as e:
        print(f"   ❌ Error al configurar BD: {e}")
        return False
    
    print("\n✅ CONFIGURACIÓN COMPLETADA")
    print("🌐 Para ejecutar la aplicación:")
    print("   python app.py")
    print("   Luego ve a: http://localhost:5000")
    
    return True

def poblar_datos_ejemplo():
    """Pobla la base de datos con datos de ejemplo"""
    from app import app, db, EmpresaTuristica, SolicitudVisita, Usuario
    
    with app.app_context():
        # EMPRESAS DE TURISMO DE IDENTIDAD (locales)
        empresas_identidad = [
            EmpresaTuristica(
                nombre='Museo Histórico de la Colonización Esperanza',
                correo='museo@esperanza.gov.ar',
                telefono='+54 3496 421100',
                direccion='Plaza San Martín 150, Esperanza, Santa Fe',
                servicios_ofrecidos='Visitas guiadas especializadas, talleres de historia local, exhibiciones interactivas',
                descripcion='Principal museo de la ciudad dedicado a preservar la historia de la colonización suiza',
                categoria_turismo='identidad',
                nivel_educativo_objetivo='Ambos',
                capacidad_maxima=60,
                horarios_atencion='Martes a Domingo 9:00-17:00',
                costo_por_persona=350.00,
                requiere_reserva=True,
                activa=True
            ),
            EmpresaTuristica(
                nombre='Centro Cultural Municipal Casa Diefenbach',
                correo='cultura@esperanza.gov.ar',
                telefono='+54 3496 421200',
                direccion='Av. San Martín 456, Esperanza, Santa Fe',
                servicios_ofrecidos='Talleres artísticos, exposiciones temporales, actividades culturales',
                descripcion='Centro neurálgico de la actividad cultural esperancense',
                categoria_turismo='identidad',
                nivel_educativo_objetivo='Primario',
                capacidad_maxima=45,
                horarios_atencion='Lunes a Viernes 8:00-18:00',
                costo_por_persona=200.00,
                requiere_reserva=True,
                activa=True
            )
        ]
        
        # EMPRESAS DE TURISMO EDUCATIVO (externas)
        empresas_educativo = [
            EmpresaTuristica(
                nombre='Granja Educativa "El Campo"',
                correo='visitas@granjaelcampo.com.ar',
                telefono='+54 3496 445566',
                direccion='Ruta Provincial 6 Km 8, Esperanza',
                servicios_ofrecidos='Actividades rurales, contacto con animales, talleres de agricultura',
                descripcion='Experiencia educativa en ambiente rural con actividades prácticas',
                categoria_turismo='educativo',
                nivel_educativo_objetivo='Primario',
                capacidad_maxima=50,
                horarios_atencion='Martes a Sábado 9:00-16:00',
                costo_por_persona=400.00,
                requiere_reserva=True,
                activa=True
            ),
            EmpresaTuristica(
                nombre='Centro de Innovación Tecnológica',
                correo='educacion@centrotech.edu.ar',
                telefono='+54 3496 333444',
                direccion='Parque Tecnológico, Esperanza',
                servicios_ofrecidos='Talleres de robótica, programación, ciencias aplicadas',
                descripcion='Centro de vanguardia en tecnología educativa',
                categoria_turismo='educativo',
                nivel_educativo_objetivo='Secundario',
                capacidad_maxima=30,
                horarios_atencion='Lunes a Viernes 8:00-17:00',
                costo_por_persona=500.00,
                requiere_reserva=True,
                activa=True
            )
        ]
        
        # Agregar todas las empresas
        for empresa in empresas_identidad + empresas_educativo:
            db.session.add(empresa)
        
        # Crear una solicitud de ejemplo
        solicitud_ejemplo = SolicitudVisita(
            nombre_institucion='Escuela Primaria N° 123',
            localidad='Esperanza, Santa Fe',
            tipo_institucion='local',
            es_de_esperanza=True,
            director='María González',
            correo_institucional='direccion@escuela123.edu.ar',
            telefono_institucion='+54 3496 111222',
            contacto_principal='Ana López',
            telefono_contacto_principal='+54 3496 111223',
            relacion_contacto='Maestra de 5° grado',
            nivel_educativo='Primario',
            cantidad_alumnos=25,
            edad_alumnos='10 a 11 años',
            discapacidad='No',
            empresas_seleccionadas='Museo Histórico de la Colonización Esperanza',
            fecha_visita=date(2025, 9, 15),
            hora_grupo1=time(9, 0),
            observaciones='Primera visita del año escolar',
            estado='Pendiente'
        )
        
        db.session.add(solicitud_ejemplo)
        db.session.commit()
        
        print(f"   ✅ {len(empresas_identidad + empresas_educativo)} empresas creadas")
        print("   ✅ 1 solicitud de ejemplo creada")

if __name__ == "__main__":
    configurar_sqlite()
