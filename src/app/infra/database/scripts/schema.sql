-- Active: 1712258180714@@127.0.0.1@3306@smart-farming
CREATE DATABASE IF NOT EXISTS `smart-farming`;

USE DATABASE `smart-farming`;

CREATE TABLE IF NOT EXISTS sensors_records (
  id CHAR(36) DEFAULT (UUID()) PRIMARY KEY NOT NULL,
  soil_humidity INT NOT NULL,
  ambient_humidity INT NOT NULL,
  temperature DECIMAL(10, 2) NOT NULL,
  water_volume DECIMAL(10, 2) NOT NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  plant_id CHAR(36) DEFAULT '4544afe3-0661-11ef-9512-0242ac140002',
  FOREIGN KEY (plant_id) REFERENCES plants(id)
);

CREATE TABLE IF NOT EXISTS checklist_records (
  id CHAR(36) DEFAULT (UUID()) PRIMARY KEY NOT NULL,
  soil_ph DECIMAL(10, 2) NOT NULL,
  soil_humidity DECIMAL(10, 2) NOT NULL,
  water_consumption DECIMAL(10, 2) NOT NULL,
  air_humidity DECIMAL(10, 2) NOT NULL,
  temperature DECIMAL(10, 2) NOT NULL,
  illuminance DECIMAL(10, 2) NOT NULL,
  lai DECIMAL(10, 2),
  leaf_appearance ENUM('SAUDAVEL', 'MURCHA', 'NÃO REGISTRADO') DEFAULT 'NÃO REGISTRADO',
  leaf_color ENUM(
   'VERDE CLARO PREDOMINANTE',
   'VERDE ESCURO PREDOMINANTE',
   'VERDE CLARO COM ALGUMAS MANCHAS CLARAS',
   'VERDE CLARO COM VARIAS MANCHAS CLARAS',
   'VERDE CLARO COM ALGUMAS MANCHAS ESCURAS',
   'VERDE CLARO COM VARIAS MANCHAS ESCURAS',
   'VERDE ESCURO COM ALGUMAS MANCHAS CLARAS',
   'VERDE ESCURO COM VARIAS MANCHAS CLARAS',
   'VERDE ESCURO COM ALGUMAS MANCHAS ESCURAS',
   'VERDE ESCURO COM VARIAS MANCHAS ESCURAS',
   'OPACO PREDOMINANTE',
   'AVERMELHADO PREDOMINANTE', 
   'NÃO REGISTRADO'
   ) DEFAULT 'NÃO REGISTRADO',
  plantation_type ENUM('PLANTIO INTERNO (FATEC)', 'PLANTIO EXTERNO (CASA)') DEFAULT 'PLANTIO INTERNO (FATEC)',
  fertilizer_expiration_date DATE NOT NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  report TEXT,
  plant_id CHAR(36) DEFAULT 'd196b612-034c-11ef-bd0e-0242ac140002',
  FOREIGN KEY (plant_id) REFERENCES plants(id)
);

CREATE TABLE IF NOT EXISTS plants (
  id CHAR(36) DEFAULT (UUID()) PRIMARY KEY NOT NULL,
  name VARCHAR(255) NOT NULL,
  hex_color VARCHAR(7) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS user (
  id CHAR(36) DEFAULT (UUID()) PRIMARY KEY NOT NULL,
  email VARCHAR(255) NOT NULL UNIQUE,
  password VARCHAR(255) NOT NULL
);