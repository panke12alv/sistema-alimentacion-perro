CREATE DATABASE IF NOT EXISTS dogfeeder_db;
USE dogfeeder_db;

CREATE TABLE IF NOT EXISTS perros (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    raza VARCHAR(100),
    edad INT,
    peso FLOAT,
    propietario_nombre VARCHAR(150),
    rutina_id INT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS alimentos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tipo VARCHAR(100) NOT NULL,
    marca VARCHAR(100),
    calorias_por_100g FLOAT,
    unidad VARCHAR(20) DEFAULT 'g',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS comidas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    perro_id INT NOT NULL,
    alimento_id INT NOT NULL,
    cantidad FLOAT NOT NULL,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    notas VARCHAR(255),
    FOREIGN KEY (perro_id) REFERENCES perros(id) ON DELETE CASCADE,
    FOREIGN KEY (alimento_id) REFERENCES alimentos(id) ON DELETE CASCADE
);
