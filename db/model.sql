-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema attini
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema attini
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `attini` DEFAULT CHARACTER SET latin1 ;
USE `attini` ;

-- -----------------------------------------------------
-- Table `attini`.`photo`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `attini`.`photo` (
  `epoch` INT(10) NOT NULL,
  `id` VARCHAR(16) CHARACTER SET 'utf8' NOT NULL,
  `photo_bin` BLOB NOT NULL,
  `ip` VARCHAR(40) CHARACTER SET 'utf8' NOT NULL,
  PRIMARY KEY (`epoch`, `id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_unicode_ci;


-- -----------------------------------------------------
-- Table `attini`.`readings`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `attini`.`readings` (
  `epoch` INT(10) NOT NULL,
  `id` VARCHAR(16) CHARACTER SET 'utf8' NOT NULL,
  `type` VARCHAR(255) CHARACTER SET 'utf8' NOT NULL,
  `read_value` VARCHAR(255) CHARACTER SET 'utf8' NOT NULL,
  `ip` VARCHAR(40) CHARACTER SET 'utf8' NOT NULL,
  PRIMARY KEY (`epoch`, `id`, `type`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_unicode_ci;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

