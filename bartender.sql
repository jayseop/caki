-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema bartender
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema bartender
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `bartender` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci ;
USE `bartender` ;

-- -----------------------------------------------------
-- Table `bartender`.`member`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `bartender`.`member` (
  `idMember` BIGINT NOT NULL AUTO_INCREMENT,
  `email` VARCHAR(30) NOT NULL,
  `password` VARCHAR(130) NOT NULL,
  `nickname` VARCHAR(45) NOT NULL,
  `date` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `qual` VARCHAR(4) NULL DEFAULT NULL,
  `introduce` VARCHAR(255) NULL DEFAULT NULL,
  PRIMARY KEY (`idMember`),
  UNIQUE INDEX `email_UNIQUE` (`email` ASC) VISIBLE,
  UNIQUE INDEX `nickname_UNIQUE` (`nickname` ASC) VISIBLE)
ENGINE = InnoDB
AUTO_INCREMENT = 15
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `bartender`.`post`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `bartender`.`post` (
  `idPost` BIGINT NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(300) NOT NULL,
  `date` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `view` VARCHAR(45) NOT NULL DEFAULT '0',
  `text` VARCHAR(8000) NOT NULL,
  `Member_idMember` BIGINT NOT NULL,
  PRIMARY KEY (`idPost`),
  INDEX `fk_Post_Member` (`Member_idMember` ASC) VISIBLE,
  CONSTRAINT `fk_Post_Member`
    FOREIGN KEY (`Member_idMember`)
    REFERENCES `bartender`.`member` (`idMember`))
ENGINE = InnoDB
AUTO_INCREMENT = 9
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `bartender`.`cocktail`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `bartender`.`cocktail` (
  `idCocktail` BIGINT NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(100) NOT NULL,
  `Post_idPost` BIGINT NOT NULL,
  PRIMARY KEY (`idCocktail`),
  INDEX `fk_Cocktail_Post` (`Post_idPost` ASC) VISIBLE,
  INDEX `idx_Cocktail_idPost` (`idCocktail` ASC, `Post_idPost` ASC) VISIBLE,
  CONSTRAINT `fk_Cocktail_Post`
    FOREIGN KEY (`Post_idPost`)
    REFERENCES `bartender`.`post` (`idPost`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `bartender`.`image`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `bartender`.`image` (
  `idImage` BIGINT NOT NULL AUTO_INCREMENT,
  `image_name` VARCHAR(100) NOT NULL,
  `image_path` VARCHAR(300) NOT NULL,
  `Post_idPost` BIGINT NOT NULL,
  PRIMARY KEY (`idImage`),
  INDEX `fk_Image_Post` (`Post_idPost` ASC) VISIBLE,
  CONSTRAINT `fk_Image_Post`
    FOREIGN KEY (`Post_idPost`)
    REFERENCES `bartender`.`post` (`idPost`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `bartender`.`ingredient`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `bartender`.`ingredient` (
  `idIngredient` BIGINT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(100) NOT NULL,
  `price` BIGINT NULL DEFAULT NULL,
  `alcohol` TINYINT NOT NULL,
  `Cocktail_idCocktail` BIGINT NOT NULL,
  PRIMARY KEY (`idIngredient`),
  INDEX `fk_Ingredient_Cocktail` (`Cocktail_idCocktail` ASC) VISIBLE,
  CONSTRAINT `fk_Ingredient_Cocktail`
    FOREIGN KEY (`Cocktail_idCocktail`)
    REFERENCES `bartender`.`cocktail` (`idCocktail`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `bartender`.`keep`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `bartender`.`keep` (
  `idKeep` BIGINT NOT NULL AUTO_INCREMENT,
  `Member_idMember` BIGINT NOT NULL,
  `Post_idPost` BIGINT NOT NULL,
  `date` TIMESTAMP NULL DEFAULT NULL,
  PRIMARY KEY (`idKeep`),
  INDEX `fk_Keep_Member` (`Member_idMember` ASC) VISIBLE,
  INDEX `fk_Keep_Post` (`Post_idPost` ASC) VISIBLE,
  CONSTRAINT `fk_Keep_Member`
    FOREIGN KEY (`Member_idMember`)
    REFERENCES `bartender`.`member` (`idMember`),
  CONSTRAINT `fk_Keep_Post`
    FOREIGN KEY (`Post_idPost`)
    REFERENCES `bartender`.`post` (`idPost`))
ENGINE = InnoDB
AUTO_INCREMENT = 4
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `bartender`.`like`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `bartender`.`like` (
  `idLike` BIGINT NOT NULL AUTO_INCREMENT,
  `Post_idPost` BIGINT NOT NULL,
  `Member_idMember` BIGINT NULL DEFAULT NULL,
  `date` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  `weather` TEXT NULL DEFAULT NULL,
  PRIMARY KEY (`idLike`),
  INDEX `fk_Like_Post` (`Post_idPost` ASC) VISIBLE,
  INDEX `Member_idMember` (`Member_idMember` ASC) VISIBLE,
  CONSTRAINT `fk_Like_Post`
    FOREIGN KEY (`Post_idPost`)
    REFERENCES `bartender`.`post` (`idPost`),
  CONSTRAINT `Member_idMember`
    FOREIGN KEY (`Member_idMember`)
    REFERENCES `bartender`.`member` (`idMember`))
ENGINE = InnoDB
AUTO_INCREMENT = 9
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `bartender`.`theme`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `bartender`.`theme` (
  `idTheme` BIGINT NOT NULL AUTO_INCREMENT,
  `state` VARCHAR(45) NOT NULL,
  `tag` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`idTheme`))
ENGINE = InnoDB
AUTO_INCREMENT = 14
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `bartender`.`temp`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `bartender`.`temp` (
  `Theme_idTheme` BIGINT NOT NULL,
  `Post_idPost` BIGINT NOT NULL,
  PRIMARY KEY (`Theme_idTheme`, `Post_idPost`),
  INDEX `fk_Temp_Post` (`Post_idPost` ASC) VISIBLE,
  CONSTRAINT `fk_Temp_Post`
    FOREIGN KEY (`Post_idPost`)
    REFERENCES `bartender`.`post` (`idPost`),
  CONSTRAINT `fk_Temp_Theme`
    FOREIGN KEY (`Theme_idTheme`)
    REFERENCES `bartender`.`theme` (`idTheme`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `bartender`.`video`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `bartender`.`video` (
  `idVideo` BIGINT NOT NULL AUTO_INCREMENT,
  `video_name` VARCHAR(100) NOT NULL,
  `video_path` VARCHAR(300) NOT NULL,
  `Post_idPost` BIGINT NOT NULL,
  PRIMARY KEY (`idVideo`),
  INDEX `fk_Video_Post` (`Post_idPost` ASC) VISIBLE,
  CONSTRAINT `fk_Video_Post`
    FOREIGN KEY (`Post_idPost`)
    REFERENCES `bartender`.`post` (`idPost`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;

INSERT INTO theme (state, tag) 
VALUES ('보드카', '술');
INSERT INTO theme (state, tag) 
VALUES ('럼', '술');
INSERT INTO theme (state, tag) 
VALUES ('브랜디', '술');
INSERT INTO theme (state, tag) 
VALUES ('위스키', '술');
INSERT INTO theme (state, tag) 
VALUES ('리큐르', '술');
INSERT INTO theme (state, tag) 
VALUES ('진', '술');
INSERT INTO theme (state, tag) 
VALUES ('데킬라', '술');

INSERT INTO theme (state, tag) 
VALUES ('당도1', '당도');
INSERT INTO theme (state, tag) 
VALUES ('당도2', '당도');
INSERT INTO theme (state, tag) 
VALUES ('당도3', '당도');

INSERT INTO theme (state, tag) 
VALUES ('도수1', '도수');
INSERT INTO theme (state, tag) 
VALUES ('도수2', '도수');
INSERT INTO theme (state, tag) 
VALUES ('도수3', '도수');



SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
