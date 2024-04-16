CREATE DATABASE IF NOT EXISTS bartender;
USE bartender;

-- Drop existing tables if they exist
DROP TABLE IF EXISTS `Member`;
DROP TABLE IF EXISTS `Post`;
DROP TABLE IF EXISTS `Keep`;
DROP TABLE IF EXISTS `Image`;
DROP TABLE IF EXISTS `Video`;
DROP TABLE IF EXISTS `Like`;
DROP TABLE IF EXISTS `Cocktail`;
DROP TABLE IF EXISTS `Ingredient`;
DROP TABLE IF EXISTS `Theme`;
DROP TABLE IF EXISTS `Temp`;

-- Create Member table
CREATE TABLE `Member` (
  `idMember` BIGINT NOT NULL AUTO_INCREMENT,
  `email` VARCHAR(30) NOT NULL,
  `password` VARCHAR(130) NOT NULL,
  `nickname` VARCHAR(45) NOT NULL,
  `date` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,  -- 가입 날짜를 현재 날짜로 기본값 설정
  `qual` VARCHAR(4) NOT NULL DEFAULT '0',      -- 기본값 '0' 설정
  `introduce` VARCHAR(100) DEFAULT NULL,
  PRIMARY KEY (`idMember`)
);

-- Create Post table
CREATE TABLE `Post` (
  `idPost` BIGINT NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(300) NOT NULL,
  `date` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `view` VARCHAR(45) NOT NULL DEFAULT '0', -- 기본값 '0'은 문자열로 설정
  `text` VARCHAR(8000) NOT NULL,
  `Member_idMember` BIGINT NOT NULL,
  PRIMARY KEY (`idPost`),
  CONSTRAINT `fk_Post_Member`
    FOREIGN KEY (`Member_idMember`)
    REFERENCES `Member` (`idMember`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
);

-- Create Keep table
CREATE TABLE `Keep` (
  `idKeep` BIGINT NOT NULL AUTO_INCREMENT,
  `Member_idMember` BIGINT NOT NULL,
  `Post_idPost` BIGINT NOT NULL,
  PRIMARY KEY (`idKeep`),
  CONSTRAINT `fk_Keep_Member`
    FOREIGN KEY (`Member_idMember`)
    REFERENCES `Member` (`idMember`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Keep_Post`
    FOREIGN KEY (`Post_idPost`)
    REFERENCES `Post` (`idPost`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
);

-- Create Image table
CREATE TABLE `Image` (
  `idImage` BIGINT NOT NULL AUTO_INCREMENT,
  `image_name` VARCHAR(100) NOT NULL,
  `image_path` VARCHAR(300) NOT NULL,
  `Post_idPost` BIGINT NOT NULL,
  PRIMARY KEY (`idImage`),
  CONSTRAINT `fk_Image_Post`
    FOREIGN KEY (`Post_idPost`)
    REFERENCES `Post` (`idPost`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
);

-- Create Video table
CREATE TABLE `Video` (
  `idVideo` BIGINT NOT NULL AUTO_INCREMENT,
  `video_name` VARCHAR(100) NOT NULL,
  `video_path` VARCHAR(300) NOT NULL,
  `Post_idPost` BIGINT NOT NULL,
  PRIMARY KEY (`idVideo`),
  CONSTRAINT `fk_Video_Post`
    FOREIGN KEY (`Post_idPost`)
    REFERENCES `Post` (`idPost`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
);

-- Create Like table
CREATE TABLE `Like` (
  `idLike` BIGINT NOT NULL AUTO_INCREMENT,
  `count` BIGINT NOT NULL DEFAULT 0,
  `week_count` BIGINT NOT NULL DEFAULT 0,
  `Post_idPost` BIGINT NOT NULL,
  PRIMARY KEY (`idLike`),
  CONSTRAINT `fk_Like_Post`
    FOREIGN KEY (`Post_idPost`)
    REFERENCES `Post` (`idPost`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
);

-- Create Cocktail table
CREATE TABLE `Cocktail` (
  `idCocktail` BIGINT NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(100) NOT NULL,
  `Post_idPost` BIGINT NOT NULL,
  PRIMARY KEY (`idCocktail`),
  CONSTRAINT `fk_Cocktail_Post`
    FOREIGN KEY (`Post_idPost`)
    REFERENCES `Post` (`idPost`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
	INDEX `idx_Cocktail_idPost` (`idCocktail`, `Post_idPost`)
);

-- Create Ingredient table
CREATE TABLE `Ingredient` (
  `idIngredient` BIGINT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(100) NOT NULL,
  `price` BIGINT NULL,
  `alcohol` TINYINT NOT NULL,
  `Cocktail_idCocktail` BIGINT NOT NULL,
  `Cocktail_Post_idPost` BIGINT NOT NULL,
  PRIMARY KEY (`idIngredient`),
  CONSTRAINT `fk_Ingredient_Cocktail`
    FOREIGN KEY (`Cocktail_idCocktail`, `Cocktail_Post_idPost`)
    REFERENCES `Cocktail` (`idCocktail`, `Post_idPost`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
);

-- Create Theme table
CREATE TABLE `Theme` (
  `idTheme` BIGINT NOT NULL AUTO_INCREMENT,
  `state` VARCHAR(45) NOT NULL,
  `tag` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`idTheme`)
);

-- Create Temp table
CREATE TABLE `Temp` (
  `Theme_idTheme` BIGINT NOT NULL,
  `Post_idPost` BIGINT NOT NULL,
  PRIMARY KEY (`Theme_idTheme`, `Post_idPost`),
  CONSTRAINT `fk_Temp_Theme`
    FOREIGN KEY (`Theme_idTheme`)
    REFERENCES `Theme` (`idTheme`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Temp_Post`
    FOREIGN KEY (`Post_idPost`)
    REFERENCES `Post` (`idPost`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
);