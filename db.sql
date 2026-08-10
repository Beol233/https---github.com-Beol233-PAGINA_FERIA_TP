-- db.sql
--
-- Este archivo estaba vacío. Se agrega SOLO la tabla que app.py
-- necesita hoy para que /registro y /login funcionen: "users".
--
-- No se agregan tablas de libros/préstamos todavía porque app.py
-- todavía no tiene rutas que las usen (buscar_libro() sí consulta una
-- tabla "libros", pero eso es parte del escáner, no del login/registro).
-- Esa tabla y las de préstamos quedan para la ruta pedagógica (Parte 2).

CREATE DATABASE IF NOT EXISTS biblioteca CHARACTER SET utf8mb4;
USE biblioteca;

CREATE TABLE IF NOT EXISTS users (
    id            INT AUTO_INCREMENT PRIMARY KEY,
    nombre        VARCHAR(100) NOT NULL,
    apellido      VARCHAR(100) NOT NULL,
    correo        VARCHAR(150) NOT NULL UNIQUE,
    tipo_usuario  ENUM('alumno', 'profesor', 'admin') NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
