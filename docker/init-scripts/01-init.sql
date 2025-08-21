-- Script de inicialización para PostgreSQL
-- Sistema de Gestión de Visitas Turísticas - Esperanza

-- Crear extensiones necesarias
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Configurar el esquema por defecto
SET search_path TO public;

-- Crear secuencias personalizadas
CREATE SEQUENCE IF NOT EXISTS seq_solicitud_visita START 1000;
CREATE SEQUENCE IF NOT EXISTS seq_empresa_turistica START 100;
CREATE SEQUENCE IF NOT EXISTS seq_usuario START 10;

-- Configurar locale en español
SET lc_time = 'es_AR.UTF-8';
SET timezone = 'America/Argentina/Buenos_Aires';

-- Crear índices adicionales para optimización
-- (Se crearán después de que Flask-SQLAlchemy cree las tablas)

-- Log de inicialización
INSERT INTO information_schema.sql_features (feature_id, feature_name, sub_feature_id, sub_feature_name, is_supported, comments) 
VALUES ('TURISMO_INIT', 'Base de datos turismo inicializada', '1', 'Configuración completada', 'YES', 'Inicialización exitosa en ' || NOW())
ON CONFLICT DO NOTHING;
