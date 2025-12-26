USE tisi_factura;

INSERT INTO clients (ruc, name, contact, email, phone) VALUES
('20123456789', 'Cliente A SAC', 'Juan Pérez', 'clienteA@example.com', '999111222'),
('20987654321', 'Cliente B SRL', 'María López', 'clienteB@example.com', '988333444'),
('20567891234', 'Cliente C EIRL', 'Carlos Díaz', 'clienteC@example.com', '977555666');

INSERT INTO invoices (invoice_number, client_id, invoice_date, total, currency, status, description) VALUES
('F001-0001', 1, '2025-01-05', 1500.00, 'PEN', 'Pendiente', 'Servicios de consultoría'),
('F001-0002', 1, '2025-01-10', 2500.00, 'USD', 'Pagada', 'Licencias de software'),
('F002-0001', 2, '2025-01-15', 800.00, 'PEN', 'Vencida', 'Mantenimiento de equipos'),
('F003-0001', 3, '2025-01-20', 1200.00, 'PEN', 'Pendiente', 'Implementación de sistema');