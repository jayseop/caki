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
  `image_path` TEXT NULL DEFAULT NULL,
  PRIMARY KEY (`idMember`),
  UNIQUE INDEX `email_UNIQUE` (`email` ASC) VISIBLE,
  UNIQUE INDEX `nickname_UNIQUE` (`nickname` ASC) VISIBLE)
ENGINE = InnoDB
AUTO_INCREMENT = 50
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `bartender`.`post`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `bartender`.`post` (
  `idPost` BIGINT NOT NULL AUTO_INCREMENT,
  `Member_idMember` BIGINT NOT NULL,
  `title` VARCHAR(300) NOT NULL,
  `text` VARCHAR(8000) NOT NULL,
  `date` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`idPost`),
  INDEX `fk_Post_Member` (`Member_idMember` ASC) VISIBLE,
  CONSTRAINT `fk_Post_Member`
    FOREIGN KEY (`Member_idMember`)
    REFERENCES `bartender`.`member` (`idMember`))
ENGINE = InnoDB
AUTO_INCREMENT = 184
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
  `image_path` TEXT NOT NULL,
  `Post_idPost` BIGINT NOT NULL,
  PRIMARY KEY (`idImage`),
  INDEX `fk_Image_Post` (`Post_idPost` ASC) VISIBLE,
  CONSTRAINT `fk_Image_Post`
    FOREIGN KEY (`Post_idPost`)
    REFERENCES `bartender`.`post` (`idPost`))
ENGINE = InnoDB
AUTO_INCREMENT = 32
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
AUTO_INCREMENT = 11
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
AUTO_INCREMENT = 17
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `bartender`.`postviews`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `bartender`.`postviews` (
  `idPostviews` BIGINT NOT NULL AUTO_INCREMENT,
  `Post_idPost` BIGINT NOT NULL,
  `Member_idMember` BIGINT NOT NULL,
  `date` TIMESTAMP NOT NULL,
  PRIMARY KEY (`idPostviews`),
  INDEX `fk_member_postviews_idx` (`Member_idMember` ASC) VISIBLE,
  INDEX `fk_post_postviews` (`Post_idPost` ASC) VISIBLE,
  CONSTRAINT `fk_member_postviews`
    FOREIGN KEY (`Member_idMember`)
    REFERENCES `bartender`.`member` (`idMember`),
  CONSTRAINT `fk_post_postviews`
    FOREIGN KEY (`Post_idPost`)
    REFERENCES `bartender`.`post` (`idPost`))
ENGINE = InnoDB
AUTO_INCREMENT = 22
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `bartender`.`review`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `bartender`.`review` (
  `idReview` BIGINT NOT NULL AUTO_INCREMENT,
  `Post_idPost` BIGINT NOT NULL,
  `Member_idMember` BIGINT NOT NULL,
  `review` TEXT NOT NULL,
  PRIMARY KEY (`idReview`),
  INDEX `Post_idPost_idx` (`Post_idPost` ASC) VISIBLE,
  INDEX `fk_Review_Member_idx` (`Member_idMember` ASC) VISIBLE,
  CONSTRAINT `fk_Review_Member`
    FOREIGN KEY (`Member_idMember`)
    REFERENCES `bartender`.`member` (`idMember`),
  CONSTRAINT `fk_Review_Post`
    FOREIGN KEY (`Post_idPost`)
    REFERENCES `bartender`.`post` (`idPost`))
ENGINE = InnoDB
AUTO_INCREMENT = 3
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `bartender`.`tag`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `bartender`.`tag` (
  `idTag` BIGINT NOT NULL AUTO_INCREMENT,
  `Post_idPost` BIGINT NOT NULL,
  `tag` TEXT NOT NULL,
  PRIMARY KEY (`idTag`),
  INDEX `fk_Tag_Post_idx` (`Post_idPost` ASC) VISIBLE,
  CONSTRAINT `fk_Tag_Post`
    FOREIGN KEY (`Post_idPost`)
    REFERENCES `bartender`.`post` (`idPost`))
ENGINE = InnoDB
AUTO_INCREMENT = 1076
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


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
