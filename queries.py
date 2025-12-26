from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import User, Client, Invoice, Payment, AuditLog

# Conexión a MySQL
engine = create_engine("mysql+pymysql://tisi_app:TisiApp2025!@localhost:3307/tisi_facturas")
Session = sessionmaker(bind=engine)
session = Session()

# -----------------------------
# 1. Listar todos los clientes
# -----------------------------
print("\n📋 Lista de clientes:")
for cliente in session.query(Client).all():
    print(f"{cliente.id} - {cliente.name} - {cliente.email}")

# -----------------------------
# 2. Facturas pendientes
# -----------------------------
print("\n📋 Facturas pendientes:")
pendientes = session.query(Invoice).filter_by(status="pending").all()
for f in pendientes:
    print(f"Factura {f.id} | Cliente {f.client_id} | Total {f.total}")

# -----------------------------
# 3. Pagos por cliente
# -----------------------------
print("\n📋 Pagos por cliente:")
pagos = session.query(Payment).all()
for p in pagos:
    print(f"Pago {p.id} | Factura {p.invoice_id} | Monto {p.amount} | Método {p.method}")

# -----------------------------
# 4. Auditoría reciente
# -----------------------------
print("\n📋 Auditoría reciente:")
logs = session.query(AuditLog).order_by(AuditLog.log_date.desc()).limit(10).all()
for log in logs:
    print(f"{log.log_date} | Usuario {log.user_id} | Acción: {log.action}")

# -----------------------------
# 5. Facturas y cliente asociado
# -----------------------------
print("\n📋 Facturas con cliente asociado:")
facturas = session.query(Invoice).join(Client).all()
for f in facturas:
    print(f"Factura {f.id} | Cliente: {f.client.name} | Estado: {f.status} | Total: {f.total}")