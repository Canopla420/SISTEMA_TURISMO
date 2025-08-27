# 📁 Scripts

Esta carpeta contiene todos los scripts auxiliares del proyecto organizados por categoría.

## 🔧 setup/
Scripts para configurar e instalar el sistema:
- `configurar_sistema.py` - Configuración automática completa
- `setup_postgres.py` - Configuración específica de PostgreSQL
- `configurar_postgresql.py` - Configuración adicional de PostgreSQL

## 💾 database/
Scripts para manejo de base de datos:
- `crear_bd.py` - Creación básica de BD
- `crear_bd_solida.py` - Creación avanzada y robusta de BD
- `crear_tablas.py` - Creación específica de tablas
- `cargar_datos_forzado.py` - Carga forzada de datos de ejemplo

## 🧪 testing/
Scripts de pruebas, diagnóstico y verificación:
- `test_*.py` - Scripts de testing
- `probar_*.py` - Scripts de pruebas funcionales
- `diagnostico_*.py` - Scripts de diagnóstico
- `verificar_*.py` - Scripts de verificación

## 🎯 Uso Recomendado

Para configurar el proyecto desde cero:
```bash
python scripts/setup/configurar_sistema.py
```

Para crear la base de datos:
```bash
python scripts/database/crear_bd_solida.py
```

Para probar el sistema:
```bash
python scripts/testing/test_db.py
```
