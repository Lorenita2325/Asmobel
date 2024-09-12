CREATE DATABASE IF NOT EXISTS asmobel;

USE asmobel;

CREATE TABLE IF NOT EXISTS datos_combinados (
    id_productor INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    direccion VARCHAR(255),
    telefono VARCHAR(20),
    correo VARCHAR(255),
    fecha_ingreso DATE,
    area_cultivo DECIMAL(10, 2),
    tipo_cultivo VARCHAR(255),
    fecha_venta DATE,
    cantidad_kilos DECIMAL(10, 2),
    precio_por_kilo DECIMAL(10, 2),
    total_venta DECIMAL(10, 2)
);
