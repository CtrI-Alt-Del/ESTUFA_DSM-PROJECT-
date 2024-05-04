-- Active: 1713835984566@@127.0.0.1@3306@smart-farming
CREATE DATABASE IF NOT EXISTS `smart-farming`;

USE DATABASE `smart-farming`;

CREATE TABLE IF NOT EXISTS plants (
  id CHAR(36) DEFAULT (UUID()) PRIMARY KEY NOT NULL,
  name VARCHAR(255) NOT NULL,
  hex_color VARCHAR(7) NOT NULL,
  created_at DATETIME DEFAULT (NOW()) NOT NULL
);

INSERT INTO plants (id, name, hex_color) 
VALUES ('4544afe3-0661-11ef-9512-0242ac140002' ,'alface','#D4F7EB');

CREATE TABLE IF NOT EXISTS user (
  id CHAR(36) DEFAULT (UUID()) PRIMARY KEY NOT NULL,
  email VARCHAR(255) NOT NULL UNIQUE,
  password VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS sensors_records (
  id CHAR(36) DEFAULT (UUID()) PRIMARY KEY NOT NULL,
  soil_humidity INTEGER NOT NULL,
  ambient_humidity INTEGER NOT NULL,
  temperature DECIMAL(10, 2) NOT NULL,
  water_volume DECIMAL(10, 2) NOT NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  plant_id CHAR(36) DEFAULT '4544afe3-0661-11ef-9512-0242ac140002',
  FOREIGN KEY (plant_id) REFERENCES plants(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS checklist_records (
  id CHAR(36) DEFAULT (UUID()) PRIMARY KEY NOT NULL,
  soil_ph INTEGER NOT NULL,
  soil_humidity INTEGER NOT NULL,
  air_humidity INTEGER NOT NULL,
  water_consumption DECIMAL(10, 2) NOT NULL,
  temperature DECIMAL(10, 1) NOT NULL,
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
  plant_id CHAR(36) DEFAULT '4544afe3-0661-11ef-9512-0242ac140002',
  FOREIGN KEY (plant_id) REFERENCES plants(id) ON DELETE CASCADE
);

-- DROP TABLES

DROP TABLE IF EXISTS checklist_records;
DROP TABLE IF EXISTS sensors_records;
DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS plants;