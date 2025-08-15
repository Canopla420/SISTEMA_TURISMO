-- Script SQL para crear las tablas del Sistema de Turismo
-- Ejecutar en Adminer: http://localhost:8080

-- Crear tabla de usuarios
CREATE TABLE usuario (
    id SERIAL PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    rol VARCHAR(50) NOT NULL DEFAULT 'Usuario',
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Crear tabla de empresas turísticas
CREATE TABLE empresa_turistica (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(200) NOT NULL,
    descripcion TEXT,
    direccion VARCHAR(200),
    telefono VARCHAR(50),
    email VARCHAR(120),
    categoria VARCHAR(50) NOT NULL,
    capacidad_maxima INTEGER,
    duracion_visita VARCHAR(50),
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Crear tabla de solicitudes de visita
CREATE TABLE solicitud_visita (
    id SERIAL PRIMARY KEY,
    nombre_institucion VARCHAR(200) NOT NULL,
    responsable VARCHAR(100) NOT NULL,
    telefono VARCHAR(50) NOT NULL,
    email VARCHAR(120) NOT NULL,
    cantidad_alumnos INTEGER NOT NULL,
    edad_alumnos VARCHAR(50),
    discapacidad VARCHAR(10) DEFAULT 'No',
    empresas_seleccionadas TEXT,
    fecha_visita DATE,
    hora_grupo1 TIME,
    hora_grupo2 TIME,
    observaciones TEXT,
    estado VARCHAR(50) DEFAULT 'Pendiente',
    fecha_solicitud TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insertar datos de ejemplo

-- Usuarios
INSERT INTO usuario (username, email, rol) VALUES
('admin', 'admin@esperanza.gov.ar', 'Administrador'),
('coordinador', 'coordinador@esperanza.gov.ar', 'Coordinador');

-- Empresas de Turismo de Identidad (locales)
INSERT INTO empresa_turistica (nombre, descripcion, direccion, telefono, email, categoria, capacidad_maxima, duracion_visita) VALUES
('Museo Histórico de la Colonización Esperanza', 'Museo que preserva la historia de la colonización suiza-alemana', 'Av. San Martín 402', '(03496) 420-789', 'museo@esperanza.gov.ar', 'Turismo de Identidad', 40, '90 minutos'),
('Centro Cultural Municipal Casa Diefenbach', 'Centro cultural en edificio histórico de 1920', 'Calle 25 de Mayo 356', '(03496) 420-123', 'cultura@esperanza.gov.ar', 'Turismo de Identidad', 60, '75 minutos'),
('Iglesia San Pedro', 'Primera iglesia de la colonia suiza, construida en 1862', 'Plaza San Martín s/n', '(03496) 420-456', 'sanpedro@esperanza.gov.ar', 'Turismo de Identidad', 80, '60 minutos');

-- Empresas de Turismo Educativo (externas)
INSERT INTO empresa_turistica (nombre, descripcion, direccion, telefono, email, categoria, capacidad_maxima, duracion_visita) VALUES
('Granja Educativa Los Aromos', 'Experiencia educativa en granja con animales de granja', 'Ruta Provincial 70 Km 8', '(03496) 421-555', 'info@granjalosaromos.com', 'Turismo Educativo', 50, '3 horas'),
('Reserva Natural Municipal', 'Reserva natural con senderos interpretativos y fauna nativa', 'Camino Rural al Río Salado', '(03496) 421-777', 'reserva@esperanza.gov.ar', 'Turismo Educativo', 35, '2.5 horas');

-- Solicitud de ejemplo
INSERT INTO solicitud_visita (nombre_institucion, responsable, telefono, email, cantidad_alumnos, edad_alumnos, discapacidad, empresas_seleccionadas, fecha_visita, hora_grupo1, hora_grupo2, observaciones, estado) VALUES
('Escuela Primaria Nacional Esperanza', 'María González', '(03496) 420-999', 'direccion@escuelaesperanza.edu.ar', 25, '8 a 10 años', 'No', 'Museo Histórico de la Colonización Esperanza,Centro Cultural Municipal Casa Diefenbach', '2025-09-15', '09:00:00', '14:00:00', 'Grupo interesado en historia local.', 'Confirmada');
