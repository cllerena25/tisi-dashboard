from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from models import Client, Invoice, Payment, AuditLog

# Conexión a MySQL
engine = create_engine("mysql+pymysql://tisi_app:TisiApp2025!@localhost:3307/tisi_facturas")
Session = sessionmaker(bind=engine)
session = Session()

# -----------------------------
# 1. Total facturado por cliente
# -----------------------------
print("\n📊 Total facturado por cliente:")
totales = session.query(Client.name, func.sum(Invoice.total))\
    .join(Invoice, Client.id == Invoice.client_id)\
    .group_by(Client.name).all()

for nombre, total in totales:
    print(f"{nombre}: S/. {total}")

# -----------------------------
# 2. Ingresos mensuales
# -----------------------------
print("\n📊 Ingresos mensuales:")
mensuales = session.query(func.month(Invoice.invoice_date), func.sum(Invoice.total))\
    .group_by(func.month(Invoice.invoice_date)).all()

for mes, total in mensuales:
    print(f"Mes {mes}: S/. {total}")

# -----------------------------
# 3. Facturas pendientes vs. pagadas
# -----------------------------
print("\n📊 Estado de facturas:")
estado_facturas = session.query(Invoice.status, func.count(Invoice.id))\
    .group_by(Invoice.status).all()

for estado, cantidad in estado_facturas:
    print(f"{estado}: {cantidad} facturas")

# -----------------------------
# 4. Top 5 clientes por facturación
# -----------------------------
print("\n📊 Top 5 clientes por facturación:")
top_clientes = session.query(Client.name, func.sum(Invoice.total))\
    .join(Invoice, Client.id == Invoice.client_id)\
    .group_by(Client.name)\
    .order_by(func.sum(Invoice.total).desc())\
    .limit(5).all()

for nombre, total in top_clientes:
    print(f"{nombre}: S/. {total}")

# -----------------------------
# 5. Acciones de auditoría más frecuentes
# -----------------------------
print("\n📊 Acciones de auditoría más frecuentes:")
acciones = session.query(AuditLog.action, func.count(AuditLog.id))\
    .group_by(AuditLog.action)\
    .order_by(func.count(AuditLog.id).desc()).all()

for accion, cantidad in acciones:
    print(f"{accion}: {cantidad} veces")