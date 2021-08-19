DROP DATABASE IF EXISTS `galerie_images`;
CREATE DATABASE `galerie_images`;
USE `galerie_images`;
DROP TABLE IF EXISTS `membre`;
CREATE TABLE `membre` (`pseudonyme` varchar(100) NOT NULL,
 `mot_de_passe` varchar(255) NOT NULL, PRIMARY KEY (`pseudonyme`) )
 ENGINE = InnoDB AUTO_INCREMENT = 1 DEFAULT CHARSET = latin1;
DROP TABLE IF EXISTS `image`;
CREATE TABLE `image`(`nom_du_fichier` varchar(200) NOT NULL,
 `date_de_mise_en_ligne` DATETIME NOT NULL DEFAULT NOW(), `titre` varchar(200) NOT NULL,
  `createur` varchar(100) NOT NULL, PRIMARY KEY (`nom_du_fichier`) )
  ENGINE = InnoDB AUTO_INCREMENT = 1 DEFAULT CHARSET = latin1;