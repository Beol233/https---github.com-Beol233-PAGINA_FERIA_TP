SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

DROP SCHEMA IF EXISTS `biblioteca_bd`;
CREATE SCHEMA IF NOT EXISTS `biblioteca_bd` DEFAULT CHARACTER SET utf8mb4;
USE `biblioteca_bd`;

-- -----------------------------------------------------
-- Table `roles` — alumno / profesor / admin
-- -----------------------------------------------------
CREATE TABLE `roles` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(50) NOT NULL,
  `descripcion` TEXT NULL,
  `created_at` DATETIME DEFAULT NOW(),
  `updated_at` DATETIME DEFAULT NOW() ON UPDATE NOW(),
  PRIMARY KEY (`id`),
  UNIQUE INDEX `nombre_UNIQUE` (`nombre` ASC)
) ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `usuarios`
-- -----------------------------------------------------
CREATE TABLE `usuarios` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(150) NOT NULL,
  `apellido` VARCHAR(45) NULL,
  `correo` VARCHAR(150) NOT NULL,
  `password` VARCHAR(255) NOT NULL,
  `matricula` VARCHAR(50) NULL,
  `rol_id` INT NOT NULL,
  `created_at` DATETIME DEFAULT NOW(),
  `updated_at` DATETIME DEFAULT NOW() ON UPDATE NOW(),
  PRIMARY KEY (`id`),
  UNIQUE INDEX `correo_UNIQUE` (`correo` ASC),
  INDEX `fk_usuarios_roles1_idx` (`rol_id` ASC),
  CONSTRAINT `fk_usuarios_roles1`
    FOREIGN KEY (`rol_id`) REFERENCES `roles` (`id`)
    ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `categorias` — géneros del mockup
-- -----------------------------------------------------
CREATE TABLE `categorias` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(100) NOT NULL,
  `descripcion` TEXT NULL,
  `created_at` DATETIME DEFAULT NOW(),
  `updated_at` DATETIME DEFAULT NOW() ON UPDATE NOW(),
  PRIMARY KEY (`id`),
  UNIQUE INDEX `nombre_UNIQUE` (`nombre` ASC)
) ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `libros`
-- -----------------------------------------------------
CREATE TABLE `libros` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `isbn` VARCHAR(20) NULL,
  `titulo` VARCHAR(300) NOT NULL,
  `autor` VARCHAR(200) NOT NULL,
  `editorial` VARCHAR(150) NULL,
  `anio` SMALLINT NULL,  -- SMALLINT y no YEAR: YEAR solo admite 1901-2155,
                         -- y el catálogo incluye clásicos anteriores (ej: 1605)
  `cantidad_total` INT NOT NULL DEFAULT 1,
  `cantidad_disponible` INT NOT NULL DEFAULT 1,
  `portada_url` VARCHAR(500) NULL,
  `categoria_id` INT NOT NULL,
  `created_at` DATETIME DEFAULT NOW(),
  `updated_at` DATETIME DEFAULT NOW() ON UPDATE NOW(),
  PRIMARY KEY (`id`),
  UNIQUE INDEX `isbn_UNIQUE` (`isbn` ASC),
  INDEX `fk_libros_categorias1_idx` (`categoria_id` ASC),
  CONSTRAINT `fk_libros_categorias1`
    FOREIGN KEY (`categoria_id`) REFERENCES `categorias` (`id`)
    ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `prestamos`
-- -----------------------------------------------------
CREATE TABLE `prestamos` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `usuario_id` INT NOT NULL,
  `libro_id` INT NOT NULL,
  `fecha_prestamo` DATETIME NOT NULL,
  `fecha_dev_esperada` DATETIME NOT NULL,
  `fecha_devolucion` DATETIME NULL,
  `estado` ENUM('activo', 'atrasado', 'devuelto') NOT NULL DEFAULT 'activo',
  `created_at` DATETIME DEFAULT NOW(),
  `updated_at` DATETIME DEFAULT NOW() ON UPDATE NOW(),
  PRIMARY KEY (`id`),
  INDEX `fk_prestamos_libros1_idx` (`libro_id` ASC),
  INDEX `fk_prestamos_usuarios1_idx` (`usuario_id` ASC),
  CONSTRAINT `fk_prestamos_usuarios1`
    FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`)
    ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_prestamos_libros1`
    FOREIGN KEY (`libro_id`) REFERENCES `libros` (`id`)
    ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `codigo_de_barras`
-- Códigos adicionales asociados a un libro (por ejemplo,
-- una etiqueta interna distinta del ISBN oficial). El
-- escáner primero busca por `libros.isbn` y, si no
-- encuentra nada, cae aquí como respaldo.
-- -----------------------------------------------------
CREATE TABLE `codigo_de_barras` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `codigo` VARCHAR(50) NOT NULL,
  `tipo_codigo` VARCHAR(20) NULL DEFAULT 'ISBN',
  `libro_id` INT NOT NULL,
  `created_at` DATETIME DEFAULT NOW(),
  `updated_at` DATETIME DEFAULT NOW() ON UPDATE NOW(),
  PRIMARY KEY (`id`),
  UNIQUE INDEX `codigo_UNIQUE` (`codigo` ASC),
  INDEX `fk_codigo_de_barras_libros1_idx` (`libro_id` ASC),
  CONSTRAINT `fk_codigo_de_barras_libros1`
    FOREIGN KEY (`libro_id`) REFERENCES `libros` (`id`)
    ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB;

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;