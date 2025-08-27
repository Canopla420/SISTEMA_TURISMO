# 🏛️ Sistema de Gestión de Visitas Turísticas - Esperanza

Sistema web desarrollado en Flask para gestionar visitas de instituciones educativas a empresas turísticas en la ciudad de Esperanza, Santa Fe.

## 🎯 Funcionalidades Principales

### 🏢 **Gestión de Empresas Turísticas (CRUD)**

- Crear, editar, consultar y desactivar empresas
- Categorización automática por tipo de turismo
- Sistema de filtrado dinámico

### 📋 **Gestión de Solicitudes de Visitas**

- Formulario de solicitud para instituciones
- Filtrado automático de empresas según origen y nivel educativo
- Estados: Pendiente, Confirmada, Realizada, Cancelada

### 🔍 **Sistema de Filtrado Inteligente**

- **Turismo de Identidad**: Para instituciones DE Esperanza
- **Turismo Educativo**: Para instituciones EXTERNAS
- Filtrado por nivel educativo (Primario, Secundario, Ambos)

### 📧 **Consultas a Empresas**

- Envío de consultas por email a empresas
- Gestión de disponibilidad y capacidad

### 📄 **Generación de Itinerarios PDF**

- Creación automática de itinerarios
- Información completa de visitas
- Compartible con instituciones y empresas

## 📁 Organización del Proyecto

El proyecto ha sido **reorganizado** siguiendo las mejores prácticas de desarrollo:

### 🎯 **Estructura Limpia**
- **Archivos principales** en la raíz (app.py, config.py, requirements.txt)
- **Scripts organizados** por funcionalidad en `/scripts/`
- **Documentación centralizada** en `/docs/`
- **Scripts SQL separados** en `/sql/`

### 🔧 **Scripts por Categoría**
- **Setup**: Configuración e instalación (`/scripts/setup/`)
- **Database**: Manejo de base de datos (`/scripts/database/`)  
- **Testing**: Pruebas y diagnósticos (`/scripts/testing/`)

### 💡 **Beneficios**
- ✅ Fácil navegación y mantenimiento
- ✅ Separación clara de responsabilidades
- ✅ Escalabilidad para futuras funcionalidades
- ✅ Mejor experiencia de desarrollo

## 💻 Tecnologías Utilizadas

- **Backend**: Flask (Python)
- **Base de datos**: SQLite (local, sin Docker)
- **Frontend**: HTML5, CSS3, JavaScript
- **PDF**: ReportLab
- **Email**: Flask-Mail

## 🚀 Instalación y Configuración

### 1. Requisitos Previos

- Python 3.8+
- Git

### 2. Clonar el Repositorio

```bash
git clone https://github.com/Canopla420/SISTEMA_TURISMO.git
cd SISTEMA_TURISMO
```

### 3. Crear Entorno Virtual

```bash
python -m venv venv_nuevo
# En Windows:
venv_nuevo\Scripts\activate
# En Linux/Mac:
source venv_nuevo/bin/activate
```

### 4. Configuración Automática

**🎯 Método Recomendado** (un solo comando):
```bash
python scripts/setup/configurar_sistema.py
```

**📁 Métodos alternativos**:
```bash
# Configuración específica SQLite
python scripts/setup/configurar_sqlite.py

# Solo creación de BD robusta  
python scripts/database/crear_bd_solida.py

# Pruebas y diagnóstico
python scripts/testing/test_db.py
```

La configuración automática:

- ✅ Verifica Python 3.8+
- ✅ Instala dependencias Python
- ✅ Crea base de datos SQLite local
- ✅ Crea estructura de tablas
- ✅ Puebla con datos de ejemplo

### 5. Ejecutar la Aplicación

```bash
python app.py
# o también:
python ejecutar.py
```

## 🔗 Accesos del Sistema

- **🖥️ Aplicación Web**: http://localhost:5000
- **📊 pgAdmin** (opcional): http://localhost:5050

### Credenciales de Base de Datos:

- **Host**: localhost:5432
- **Database**: turismo_esperanza
- **User**: admin_turismo
- **Password**: TurismoEsperanza2024!

## 📁 Estructura del Proyecto

```
SISTEMA_TURISMO/
├── app.py                    # 🚀 Aplicación principal Flask
├── config.py                 # ⚙️ Configuración de la aplicación  
├── requirements.txt          # 📦 Dependencias Python
├── docker-compose.yml        # 🐳 Configuración Docker
├── README.md                 # 📖 Documentación principal
├── .env                      # 🔐 Variables de entorno
├── 📁 scripts/               # 🔧 Scripts auxiliares organizados
│   ├── setup/               # Scripts de configuración
│   │   ├── configurar_sistema.py
│   │   ├── setup_postgres.py
│   │   └── configurar_postgresql.py
│   ├── database/            # Scripts de base de datos
│   │   ├── crear_bd.py
│   │   ├── crear_bd_solida.py
│   │   ├── crear_tablas.py
│   │   └── cargar_datos_forzado.py
│   └── testing/             # Scripts de pruebas
│       ├── test_*.py
│       ├── probar_*.py
│       ├── diagnostico_*.py
│       └── verificar_*.py
├── 📁 sql/                   # 💾 Scripts SQL
│   ├── crear_tablas.sql
│   └── insertar_datos.sql
├── 📁 docs/                  # 📖 Documentación técnica
│   ├── CORRECCIONES_APLICADAS.md
│   └── PROYECTO_LIMPIO.md
├── 📁 templates/             # 🎨 Plantillas HTML
│   ├── index.html           # Página principal
│   ├── nueva_visita.html    # Formulario de solicitud
│   ├── consultar_visitas.html # Gestión de visitas
│   ├── gestionar_empresas.html # CRUD empresas
│   └── ...
├── 📁 static/                # 🎨 Archivos estáticos
│   ├── css/                 # Estilos CSS
│   └── js/                  # JavaScript
├── 📁 migrations/            # 🔄 Migraciones de BD
└── 📁 instance/              # 💾 Base de datos local
```

## 🎪 Rutas Principales

### 📋 **Gestión de Visitas**

- `/` - Página principal
- `/nueva_visita` - Formulario de nueva solicitud
- `/consultar_visitas` - Ver y gestionar visitas
- `/modificar_visita/<id>` - Editar solicitud
- `/confirmar_visita/<id>` - Confirmar visita
- `/crear_itinerario` - Generar PDF de itinerario

### 🏢 **Gestión de Empresas**

- `/gestionar_empresas` - Dashboard CRUD de empresas
- `/agregar_empresa` - Crear nueva empresa
- `/editar_empresa/<id>` - Editar empresa
- `/consultar_empresas` - Búsqueda y consultas

### 🔌 **API Endpoints**

- `/empresas_filtradas` - Filtrado dinámico
- `/todas_empresas` - Lista JSON de empresas
- `/enviar_consulta` - Procesar consultas

## 🎯 Sistema de Categorización

### 🏛️ **TURISMO DE IDENTIDAD** (Instituciones Locales)

Para estudiantes DE Esperanza que quieren conocer su ciudad:

**Nivel Primario:**

- Museo Histórico de la Colonización
- Centro Cultural Municipal
- Espacios patrimoniales locales

**Nivel Secundario:**

- Cooperativa Agrícola Local
- Industrias Lácteas
- Empresas de producción local

### 🎓 **TURISMO EDUCATIVO** (Instituciones Externas)

Para estudiantes de OTRAS ciudades:

**Nivel Primario:**

- Granjas educativas
- Centros de naturaleza
- Actividades rurales

**Nivel Secundario:**

- Centros tecnológicos
- Industrias especializadas
- Innovación y ciencia

## 🛠️ Comandos Útiles

### Docker

```bash
# Iniciar servicios
docker compose up -d

# Parar servicios
docker compose down

# Ver logs
docker compose logs postgres_turismo

# Reiniciar
docker compose restart
```

### Base de Datos

```bash
# Crear migración
flask db migrate -m "Descripción"

# Aplicar migraciones
flask db upgrade

# Conectar a PostgreSQL
docker exec -it postgres_turismo psql -U admin_turismo turismo_esperanza
```

## 🔧 Configuración Avanzada

### Variables de Entorno (.env)

```env
DATABASE_URL=postgresql://admin_turismo:TurismoEsperanza2024!@localhost:5432/turismo_esperanza
SECRET_KEY=clave_secreta_segura
FLASK_ENV=development
FLASK_DEBUG=True
```

### Email (Opcional)

```env
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=tu_email@gmail.com
MAIL_PASSWORD=tu_app_password
```

## 🆘 Solución de Problemas

### Error de Docker

```bash
# Verificar que Docker esté ejecutándose
docker --version
docker compose version

# Reiniciar Docker Desktop si es necesario
```

### Error de Base de Datos

```bash
# Resetear base de datos
docker compose down -v
python configurar_sistema.py
```

### Error de Dependencias

```bash
# Reinstalar dependencias
pip install -r requirements.txt --force-reinstall
```

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más detalles.

## 👨‍💻 Autor

**Canopla420** - [GitHub](https://github.com/Canopla420)

---

_Sistema desarrollado para la Dirección de Turismo de la Ciudad de Esperanza, Santa Fe_ 2. Instalar "SQLTools PostgreSQL/Cockroach Driver" 3. Crear nueva conexión:

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

1.  **Tipos de datos mejorados**:

    - Fechas como `Date` en lugar de strings
    - Horas como `Time` en lugar de strings
    - Precios como `Numeric` para mayor precisión

2.  **Relaciones entre tablas**:

    - Las visitas están relacionadas con empresas
    - Se mantiene historial completo
    - Soft delete para empresas (no se eliminan, se desactivan)

3.  **Manejo de errores**:
    - Try-catch en operaciones críticas
    - Rollback automático en caso de errores
    - Logging de errores para debugging
4.  **Configuración flexible**:

    - Variables de entorno para credenciales
    - Configuraciones separadas para desarrollo/producción
    - Fácil cambio entre entornos

           # 1. Clonar el repositorio

      git clone https://github.com/Canopla420/SISTEMA_TURISMO.git
      cd SISTEMA_TURISMO

# 2. Instalar dependencias

pip install -r requirements.txt

# 3. Configurar base de datos

flask db upgrade

# 4. Ejecutar

python app.py
