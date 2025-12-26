CREATE DATABASE IF NOT EXISTS tisi_factura;

CREATE USER IF NOT EXISTS 'tisi_app'@'localhost' IDENTIFIED BY 'TisiApp2025!';

GRANT ALL PRIVILEGES ON tisi_factura.* TO 'tisi_app'@'localhost';

FLUSH PRIVILEGES;
