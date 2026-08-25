-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema biblioteca_bd
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema biblioteca_bd
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `biblioteca_bd` DEFAULT CHARACTER SET utf8 ;
USE `biblioteca_bd` ;

-- -----------------------------------------------------
-- Table `biblioteca_bd`.`roles`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `biblioteca_bd`.`roles` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(50) NULL,
  `descripcion` TEXT NULL,
  `updated_at` DATETIME NULL,
  `created_at` DATETIME NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `biblioteca_bd`.`usuarios`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `biblioteca_bd`.`usuarios` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(150) NULL,
  `apellido` VARCHAR(45) NULL,
  `correo` VARCHAR(150) NULL,
  `password` VARCHAR(255) NULL,
  `updated_at` DATETIME NULL,
  `created_at` DATETIME NULL,
  `rol_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_usuarios_roles1_idx` (`rol_id` ASC) VISIBLE,
  UNIQUE INDEX `correo_UNIQUE` (`correo` ASC) VISIBLE,
  CONSTRAINT `fk_usuarios_roles1`
    FOREIGN KEY (`rol_id`)
    REFERENCES `biblioteca_bd`.`roles` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `biblioteca_bd`.`categorias`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `biblioteca_bd`.`categorias` (
  `id` INT NOT NULL,
  `nombre` VARCHAR(100) NULL,
  `descripcion` TEXT NULL,
  `update_at` DATETIME NULL,
  `created_at` DATETIME NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;




-- Table `biblioteca_bd`.`libros`
-- ----------------------------------------------------
CREATE TABLE IF NOT EXISTS `biblioteca_bd`.`libros` (
  `id` INT NOT NULL,
  `isbn` VARCHAR(20) NULL,
  `titulo` VARCHAR(300) NULL,
  `autor` VARCHAR(200) NULL,
  `editorial` VARCHAR(150) NULL,
  `anio` YEAR NULL,
  `cantidad_total` INT NULL,
  `cantidad_disponible` INT NULL,
  `categoria_id` INT NOT NULL,
  PRIMARY KEY (`id`, `categoria_id`),
  INDEX `fk_libros_categorias1_idx` (`categoria_id` ASC) VISIBLE,
  CONSTRAINT `fk_libros_categorias1`
    FOREIGN KEY (`categoria_id`)
    REFERENCES `biblioteca_bd`.`categorias` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `biblioteca_bd`.`prestamos`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `biblioteca_bd`.`prestamos` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `usuario_id` INT NOT NULL,
  `libro_id` INT NOT NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  `fecha_dev_esperada` DATETIME NULL,
  PRIMARY KEY (`id`, `usuario_id`, `libro_id`),
  INDEX `fk_usuarios_has_libros_libros1_idx` (`libro_id` ASC) VISIBLE,
  INDEX `fk_usuarios_has_libros_usuarios1_idx` (`usuario_id` ASC) VISIBLE,
  CONSTRAINT `fk_usuarios_has_libros_usuarios1`
    FOREIGN KEY (`usuario_id`)
    REFERENCES `biblioteca_bd`.`usuarios` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_usuarios_has_libros_libros1`
    FOREIGN KEY (`libro_id`)
    REFERENCES `biblioteca_bd`.`libros` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `biblioteca_bd`.`codigo_de_barras`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `biblioteca_bd`.`codigo_de_barras` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `codigo` VARCHAR(50) NULL,
  `tipo_codigo` VARCHAR(20) NULL,
  `updated_at` DATETIME NULL,
  `created_at` DATETIME NULL,
  `libro_id` INT NOT NULL,
  PRIMARY KEY (`id`, `libro_id`),
  UNIQUE INDEX `codigo_UNIQUE` (`codigo` ASC) VISIBLE,
  INDEX `fk_codigo_de_barras_libros1_idx` (`libro_id` ASC) VISIBLE,
  CONSTRAINT `fk_codigo_de_barras_libros1`
    FOREIGN KEY (`libro_id`)
    REFERENCES `biblioteca_bd`.`libros` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
