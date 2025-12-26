USE tisi_factura;

-- Añadir columna categoría a la tabla invoices
ALTER TABLE invoices
ADD COLUMN category VARCHAR(50) DEFAULT 'General';

-- Actualizar facturas de prueba con categorías
UPDATE invoices SET category = 'Consultoría' WHERE invoice_number = 'F001-0001';
UPDATE invoices SET category = 'Licencias'   WHERE invoice_number = 'F001-0002';
UPDATE invoices SET category = 'Mantenimiento' WHERE invoice_number = 'F002-0001';
UPDATE invoices SET category = 'Implementación' WHERE invoice_number = 'F003-0001';