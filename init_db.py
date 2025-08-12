"""
Script para poblar la base de datos con datos de ejemplo
"""
from app import app, db, EmpresaTuristica
from datetime import datetime

def init_empresas_ejemplo():
    """Crea empresas de ejemplo en la base de datos categorizadas por tipo de turismo y nivel educativo"""
    
    empresas_ejemplo = [
        # EMPRESAS PARA IDENTIDAD LOCAL (Esperanza) - PRIMARIO
        {
            'nombre': 'Museo Histórico de Esperanza',
            'correo': 'educacion@museoesperanza.gov.ar',
            'telefono': '+54 3496 421234',
            'direccion': 'Plaza San Martín 123, Esperanza, Santa Fe',
            'servicios_ofrecidos': 'Visitas guiadas, talleres de historia local, exhibiciones interactivas',
            'descripcion': 'Museo dedicado a la historia y cultura de Esperanza',
            'categoria_turismo': 'identidad',
            'nivel_educativo_objetivo': 'Primario',
            'capacidad_maxima': 40,
            'horarios_atencion': 'Martes a Viernes 9:00-17:00',
            'costo_por_persona': 300.00,
            'requiere_reserva': True
        },
        {
            'nombre': 'Centro Cultural Municipal',
            'correo': 'cultura@esperanza.gov.ar',
            'telefono': '+54 3496 425678',
            'direccion': 'Av. San Martín 456, Esperanza, Santa Fe',
            'servicios_ofrecidos': 'Talleres artísticos, exposiciones, actividades culturales',
            'descripcion': 'Centro cultural con actividades para conocer las tradiciones locales',
            'categoria_turismo': 'identidad',
            'nivel_educativo_objetivo': 'Ambos',
            'capacidad_maxima': 60,
            'horarios_atencion': 'Lunes a Viernes 8:00-18:00',
            'costo_por_persona': 250.00,
            'requiere_reserva': True
        },
        
        # EMPRESAS PARA IDENTIDAD LOCAL (Esperanza) - SECUNDARIO
        {
            'nombre': 'Cooperativa Agrícola Local',
            'correo': 'visitas@coopagriesperanza.com.ar',
            'telefono': '+54 3496 427890',
            'direccion': 'Ruta Provincial 6 Km 15, Esperanza',
            'servicios_ofrecidos': 'Recorrido por instalaciones, charlas sobre cooperativismo, degustación de productos',
            'descripcion': 'Conocer el sistema cooperativo y la producción agrícola local',
            'categoria_turismo': 'identidad',
            'nivel_educativo_objetivo': 'Secundario',
            'capacidad_maxima': 35,
            'horarios_atencion': 'Lunes a Viernes 9:00-16:00',
            'costo_por_persona': 800.00,
            'requiere_reserva': True
        },
        {
            'nombre': 'Industria Láctea Esperanza',
            'correo': 'educativo@lacteoesesperanza.com',
            'telefono': '+54 3496 429012',
            'direccion': 'Zona Industrial Norte, Esperanza',
            'servicios_ofrecidos': 'Visita a planta productiva, proceso de elaboración, control de calidad',
            'descripcion': 'Industria local de productos lácteos con programa educativo',
            'categoria_turismo': 'identidad',
            'nivel_educativo_objetivo': 'Secundario',
            'capacidad_maxima': 25,
            'horarios_atencion': 'Martes y Jueves 10:00-15:00',
            'costo_por_persona': 650.00,
            'requiere_reserva': True
        },
        
        # EMPRESAS PARA TURISMO EDUCATIVO (Externas) - PRIMARIO
        {
            'nombre': 'Granja Educativa Los Arrayanes',
            'correo': 'visitas@granjalosarrayanes.com.ar',
            'telefono': '+54 342 4561234',
            'direccion': 'Ruta 11 Km 445, Santa Fe',
            'servicios_ofrecidos': 'Contacto con animales, huerta orgánica, elaboración de pan casero',
            'descripcion': 'Experiencia rural educativa para nivel primario',
            'categoria_turismo': 'educativo',
            'nivel_educativo_objetivo': 'Primario',
            'capacidad_maxima': 80,
            'horarios_atencion': 'Martes a Viernes 9:00-15:00',
            'costo_por_persona': 1500.00,
            'requiere_reserva': True
        },
        {
            'nombre': 'Acuario del Río Paraná',
            'correo': 'educacion@acuarioparana.org.ar',
            'telefono': '+54 342 4567890',
            'direccion': 'Costanera Este 1200, Santa Fe',
            'servicios_ofrecidos': 'Recorrido por acuarios, charlas sobre fauna del río, actividades interactivas',
            'descripcion': 'Centro de interpretación de la fauna acuática regional',
            'categoria_turismo': 'educativo',
            'nivel_educativo_objetivo': 'Ambos',
            'capacidad_maxima': 100,
            'horarios_atencion': 'Martes a Domingo 10:00-18:00',
            'costo_por_persona': 1200.00,
            'requiere_reserva': True
        },
        
        # EMPRESAS PARA TURISMO EDUCATIVO (Externas) - SECUNDARIO
        {
            'nombre': 'Planetario de Santa Fe',
            'correo': 'reservas@planetariosf.gov.ar',
            'telefono': '+54 342 4570123',
            'direccion': 'Parque Federal 2500, Santa Fe',
            'servicios_ofrecidos': 'Funciones de planetario, observatorio astronómico, talleres de ciencias',
            'descripcion': 'Centro de divulgación científica y astronomía',
            'categoria_turismo': 'educativo',
            'nivel_educativo_objetivo': 'Secundario',
            'capacidad_maxima': 120,
            'horarios_atencion': 'Miércoles a Domingo 15:00-21:00',
            'costo_por_persona': 1800.00,
            'requiere_reserva': True
        },
        {
            'nombre': 'Centro de Innovación Tecnológica',
            'correo': 'visitas@citecnologico.edu.ar',
            'telefono': '+54 342 4572345',
            'direccion': 'Parque Tecnológico del Litoral, Santa Fe',
            'servicios_ofrecidos': 'Laboratorios de robótica, impresión 3D, programación, realidad virtual',
            'descripcion': 'Centro educativo de nuevas tecnologías para estudiantes',
            'categoria_turismo': 'educativo',
            'nivel_educativo_objetivo': 'Secundario',
            'capacidad_maxima': 40,
            'horarios_atencion': 'Lunes a Viernes 9:00-17:00',
            'costo_por_persona': 2200.00,
            'requiere_reserva': True
        },
        {
            'nombre': 'Parque Nacional Los Palmares',
            'correo': 'educativo@palmares.gov.ar',
            'telefono': '+54 3447 456789',
            'direccion': 'Ruta Nacional 168 Km 58, Entre Ríos',
            'servicios_ofrecidos': 'Senderismo interpretativo, observación de aves, educación ambiental',
            'descripcion': 'Área protegida con programa de educación ambiental',
            'categoria_turismo': 'educativo',
            'nivel_educativo_objetivo': 'Ambos',
            'capacidad_maxima': 150,
            'horarios_atencion': 'Todos los días 8:00-18:00',
            'costo_por_persona': 950.00,
            'requiere_reserva': True
        }
    ]
    
    with app.app_context():
        # Verificar si ya existen empresas
        if EmpresaTuristica.query.count() > 0:
            print("Ya existen empresas en la base de datos. No se crearán duplicados.")
            return
        
        print("Creando empresas de ejemplo categorizadas...")
        
        for empresa_data in empresas_ejemplo:
            empresa = EmpresaTuristica(**empresa_data)
            db.session.add(empresa)
        
        try:
            db.session.commit()
            print(f"Se crearon {len(empresas_ejemplo)} empresas de ejemplo exitosamente.")
            print("\nCategorías creadas:")
            print("- IDENTIDAD (Esperanza): 4 empresas")
            print("  * Primario: 2 empresas")
            print("  * Secundario: 2 empresas")
            print("- EDUCATIVO (Externas): 5 empresas")
            print("  * Primario: 2 empresas")
            print("  * Secundario: 3 empresas")
            print("  * Ambos niveles: Algunas empresas atienden ambos niveles")
        except Exception as e:
            db.session.rollback()
            print(f"Error al crear empresas: {e}")

if __name__ == '__main__':
    init_empresas_ejemplo()
