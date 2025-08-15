-- INSERTAR DATOS DE EJEMPLO EN EL SISTEMA DE TURISMO
-- Copiar y pegar cada bloque por separado en Adminer

-- 1. INSERTAR USUARIOS
INSERT INTO usuario (username, email, rol) VALUES
('admin', 'admin@esperanza.gov.ar', 'Administrador'),
('coordinador', 'coordinador@esperanza.gov.ar', 'Coordinador');

-- 2. INSERTAR EMPRESAS DE TURISMO DE IDENTIDAD (locales)
INSERT INTO empresa_turistica (nombre, descripcion, direccion, telefono, email, categoria, capacidad_maxima, duracion_visita) VALUES
('Museo Histórico de la Colonización Esperanza', 'Museo que preserva la historia de la colonización suiza-alemana', 'Av. San Martín 402', '(03496) 420-789', 'museo@esperanza.gov.ar', 'Turismo de Identidad', 40, '90 minutos'),
('Centro Cultural Municipal Casa Diefenbach', 'Centro cultural en edificio histórico de 1920', 'Calle 25 de Mayo 356', '(03496) 420-123', 'cultura@esperanza.gov.ar', 'Turismo de Identidad', 60, '75 minutos'),
('Iglesia San Pedro', 'Primera iglesia de la colonia suiza, construida en 1862', 'Plaza San Martín s/n', '(03496) 420-456', 'sanpedro@esperanza.gov.ar', 'Turismo de Identidad', 80, '60 minutos');

-- 3. INSERTAR EMPRESAS DE TURISMO EDUCATIVO (externas)
INSERT INTO empresa_turistica (nombre, descripcion, direccion, telefono, email, categoria, capacidad_maxima, duracion_visita) VALUES
('Granja Educativa Los Aromos', 'Experiencia educativa en granja con animales de granja', 'Ruta Provincial 70 Km 8', '(03496) 421-555', 'info@granjalosaromos.com', 'Turismo Educativo', 50, '3 horas'),
('Reserva Natural Municipal', 'Reserva natural con senderos interpretativos y fauna nativa', 'Camino Rural al Río Salado', '(03496) 421-777', 'reserva@esperanza.gov.ar', 'Turismo Educativo', 35, '2.5 horas');

-- 4. INSERTAR SOLICITUD DE EJEMPLO
INSERT INTO solicitud_visita (nombre_institucion, responsable, telefono, email, cantidad_alumnos, edad_alumnos, discapacidad, empresas_seleccionadas, fecha_visita, hora_grupo1, hora_grupo2, observaciones, estado) VALUES
('Escuela Primaria Nacional Esperanza', 'María González', '(03496) 420-999', 'direccion@escuelaesperanza.edu.ar', 25, '8 a 10 años', 'No', 'Museo Histórico de la Colonización Esperanza,Centro Cultural Municipal Casa Diefenbach', '2025-09-15', '09:00:00', '14:00:00', 'Grupo interesado en historia local.', 'Confirmada');
