# Sistema de Gestión de Visitas Turísticas

Sistema web desarrollado en Flask para gestionar visitas de instituciones educativas a empresas turísticas.

## Tecnologías utilizadas

- **Backend**: Flask (Python)
- **Base de datos**: PostgreSQL
- **Frontend**: HTML, CSS, JavaScript
- **PDF**: ReportLab
- **Email**: Flask-Mail

## Configuración de PostgreSQL

### 1. Instalar PostgreSQL
- Descarga e instala PostgreSQL desde: https://www.postgresql.org/download/
- Durante la instalación, anota el puerto (por defecto 5432) y la contraseña del usuario `postgres`

### 2. Crear la base de datos
```sql
-- Conectarse a PostgreSQL como superusuario
psql -U postgres

-- Crear la base de datos
CREATE DATABASE sistema_turismo;

-- Crear un usuario específico (opcional)
CREATE USER turismo_user WITH PASSWORD 'tu_password';
GRANT ALL PRIVILEGES ON DATABASE sistema_turismo TO turismo_user;

-- Salir de PostgreSQL
\q
```

### 3. Configurar VS Code para PostgreSQL

#### Opción 1: Usar extensión SQLTools
1. Instalar extensión "SQLTools" en VS Code
2. Instalar "SQLTools PostgreSQL/Cockroach Driver"
3. Crear nueva conexión:
   - Host: localhost
   - Port: 5432
   - Database: sistema_turismo
   - Username: postgres (o tu usuario)
   - Password: tu_password

#### Opción 2: Usar extensión PostgreSQL
1. Instalar extensión "PostgreSQL" (ckolkman.vscode-postgres)
2. Configurar conexión con tus credenciales

## Instalación del proyecto

### 1. Instalar dependencias
```bash
# Instalar psycopg2 para PostgreSQL
pip install psycopg2-binary

# Instalar todas las dependencias
pip install -r requirements.txt
```

### 2. Configurar variables de entorno
```bash
# Copiar el archivo de ejemplo
copy .env.example .env

# Editar .env con tus datos reales:
# - DB_PASSWORD: tu contraseña de PostgreSQL
# - DB_USER: tu usuario (postgres por defecto)
# - MAIL_USERNAME y MAIL_PASSWORD: para envío de emails
```

### 3. Inicializar la base de datos
```bash
# Inicializar migraciones (solo la primera vez)
flask db init

# Crear migración inicial
flask db migrate -m "Crear tablas iniciales"

# Aplicar migraciones
flask db upgrade

# Poblar con datos de ejemplo (opcional)
python init_db.py
```

### 4. Ejecutar la aplicación
```bash
python app.py
```

## Estructura de la base de datos

### Tablas principales:
- **solicitudes_visita**: Solicitudes de visitas de instituciones
- **empresas_turisticas**: Empresas que reciben las visitas
- **visitas_realizadas**: Historial de visitas completadas
- **consultas_empresas**: Consultas enviadas a empresas
- **itinerarios**: Itinerarios generados en PDF
- **usuarios**: Sistema de usuarios (futuro)

## Sistema de Categorización de Visitas

El sistema está diseñado para manejar dos tipos principales de turismo educativo:

### 🏛️ **NUESTRA IDENTIDAD (Esperanza)**
**Para instituciones DE Esperanza que quieren conocer su ciudad**

#### Nivel Primario:
- Museo Histórico de Esperanza
- Centro Cultural Municipal
- Espacios patrimoniales locales

#### Nivel Secundario:  
- Cooperativa Agrícola Local
- Industria Láctea Esperanza
- Empresas locales de producción

### 🌟 **TURISMO EDUCATIVO (Externas)**
**Para instituciones de AFUERA que visitan la región**

#### Nivel Primario:
- Granja Educativa Los Arrayanes
- Acuario del Río Paraná
- Experiencias rurales y de naturaleza

#### Nivel Secundario:
- Planetario de Santa Fe
- Centro de Innovación Tecnológica
- Parque Nacional Los Palmares

### ⚙️ **Funcionamiento del Sistema**

1. **Detección automática**: Al ingresar la localidad, el sistema detecta si es de Esperanza o externa
2. **Filtrado inteligente**: Las empresas se muestran según:
   - Tipo de institución (local/externa)
   - Nivel educativo (primario/secundario)
3. **Categorías de empresas**:
   - `categoria_turismo`: 'identidad' o 'educativo'
   - `nivel_educativo_objetivo`: 'Primario', 'Secundario', 'Ambos'

### Para instituciones:
- ✅ Solicitar visitas a empresas turísticas
- ✅ Seleccionar múltiples empresas
- ✅ Especificar fechas y horarios
- ✅ Detallar información del grupo

### Para administradores:
- ✅ Gestionar empresas turísticas (CRUD)
- ✅ Consultar y modificar solicitudes
- ✅ Confirmar/rechazar visitas
- ✅ Generar itinerarios en PDF
- ✅ Registrar visitas realizadas
- ✅ Enviar consultas a empresas

## Comandos útiles

### Migraciones
```bash
# Crear nueva migración después de cambios en modelos
flask db migrate -m "Descripción del cambio"

# Aplicar migraciones pendientes
flask db upgrade

# Ver historial de migraciones
flask db history

# Revertir a migración anterior
flask db downgrade
```

### Base de datos
```bash
# Conectarse directamente a PostgreSQL
psql -U postgres -d sistema_turismo

# Backup de la base de datos
pg_dump -U postgres sistema_turismo > backup.sql

# Restaurar backup
psql -U postgres sistema_turismo < backup.sql
```

## Rutas principales

- `/` - Página principal
- `/nueva_visita` - Formulario de nueva visita
- `/consultar_visitas` - Ver todas las visitas
- `/consultar_empresas` - Consultar empresas
- `/gestionar_empresas` - Administrar empresas (CRUD)
- `/crear_itinerario` - Generar PDFs de itinerarios

## Notas importantes

1. **Tipos de datos mejorados**: 
   - Fechas como `Date` en lugar de strings
   - Horas como `Time` en lugar de strings
   - Precios como `Numeric` para mayor precisión

2. **Relaciones entre tablas**: 
   - Las visitas están relacionadas con empresas
   - Se mantiene historial completo
   - Soft delete para empresas (no se eliminan, se desactivan)

3. **Manejo de errores**: 
   - Try-catch en operaciones críticas
   - Rollback automático en caso de errores
   - Logging de errores para debugging

4. **Configuración flexible**: 
   - Variables de entorno para credenciales
   - Configuraciones separadas para desarrollo/producción
   - Fácil cambio entre entornos
