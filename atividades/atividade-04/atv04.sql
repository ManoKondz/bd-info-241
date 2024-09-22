CREATE DATABASE NoroesteCearense;

USE NoroesteCearense;

-- Tabela de Estado
CREATE TABLE Estado (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(100)
);

-- Inserindo o estado do Ceará
INSERT INTO Estado (nome) VALUES ('Ceará');

-- Tabela de MesoRegiao
CREATE TABLE MesoRegiao (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(100),
    estado_id INT,
    FOREIGN KEY (estado_id) REFERENCES Estado(id)
);

-- Inserindo uma mesorregião
INSERT INTO MesoRegiao (nome, estado_id) VALUES ('Noroeste Cearense', 1);

-- Tabela de MicroRegiao
CREATE TABLE MicroRegiao (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(100),
    mesoregiao_id INT,
    FOREIGN KEY (mesoregiao_id) REFERENCES MesoRegiao(id)
);

-- Inserindo uma microrregião
INSERT INTO MicroRegiao (nome, mesoregiao_id) VALUES ('Sobral', 1);

-- Tabela de Município
CREATE TABLE Municipio (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(100),
    microregiao_id INT,
    FOREIGN KEY (microregiao_id) REFERENCES MicroRegiao(id)
);

-- Inserindo o município de Sobral
INSERT INTO Municipio (nome, microregiao_id) VALUES ('Sobral', 1);

-- Tabela IFCampus
CREATE TABLE IFCampus (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(100),
    endereco VARCHAR(255),
    longitude FLOAT,
    latitude FLOAT,
    municipio_id INT,
    FOREIGN KEY (municipio_id) REFERENCES Municipio(id)
);

-- Inserindo o IFCE Campus Sobral
INSERT INTO IFCampus (nome, endereco, longitude, latitude, municipio_id) 
VALUES ('IFCE Campus Sobral', 'Av. Dr. Guarany, 317, Betania, CEP: 62042-030', -40.349, -3.681, 1);

-- Tabela EscolaCampo
CREATE TABLE EscolaCampo (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(100),
    endereco VARCHAR(255),
    longitude FLOAT,
    latitude FLOAT,
    municipio_id INT,
    FOREIGN KEY (municipio_id) REFERENCES Municipio(id)
);

-- Inserindo uma escola do campo fictícia
INSERT INTO EscolaCampo (nome, endereco, longitude, latitude, municipio_id) 
VALUES ('Escola Rural de Sobral', 'Estrada da Fazenda, Zona Rural, Sobral, CEP: 62000-000', -40.335, -3.710, 1);

-- Tabela Assentamento
CREATE TABLE Assentamento (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(100),
    endereco VARCHAR(255),
    longitude FLOAT,
    latitude FLOAT,
    municipio_id INT,
    FOREIGN KEY (municipio_id) REFERENCES Municipio(id)
);

-- Inserindo um assentamento fictício
INSERT INTO Assentamento (nome, endereco, longitude, latitude, municipio_id) 
VALUES ('Assentamento Novo Horizonte', 'Área Rural, Sobral, CEP: 62000-001', -40.330, -3.705, 1);
