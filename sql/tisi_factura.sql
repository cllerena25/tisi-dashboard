CREATE DATABASE IF NOT EXISTS tisi_factura;
USE tisi_factura;

CREATE TABLE IF NOT EXISTS clients (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ruc VARCHAR(11) NOT NULL UNIQUE,
    name VARCHAR(255) NOT NULL,
    contact VARCHAR(255),
    email VARCHAR(255),
    phone VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS invoices (
    id INT AUTO_INCREMENT PRIMARY KEY,
    invoice_number VARCHAR(20) NOT NULL UNIQUE,
    client_id INT NOT NULL,
    invoice_date DATE NOT NULL,
    total DECIMAL(12,2) NOT NULL,
    currency VARCHAR(3) NOT NULL,
    status ENUM('Pendiente','Pagada','Vencida') DEFAULT 'Pendiente',
    description TEXT,
    FOREIGN KEY (client_id) REFERENCES clients(id)
);