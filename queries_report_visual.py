import matplotlib.pyplot as plt
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from models import Client, Invoice

# Conexión a MySQL
engine = create_engine("mysql+pymysql://tisi_app:TisiApp2025!@localhost:3307/tisi_facturas")
Session = sessionmaker(bind=engine)
session = Session()

# Paleta institucional
rojo = "#FF0000"
blanco = "#FFFFFF"
negro = "#000000"

# -----------------------------
# 1. Total facturado por cliente (barras)
# -----------------------------
totales = session.query(Client.name, func.sum(Invoice.total))\
    .join(Invoice, Client.id == Invoice.client_id)\
    .group_by(Client.name).all()

clientes = [c[0] for c in totales]
valores = [c[1] for c in totales]

plt.figure(figsize=(10,6))
plt.bar(clientes, valores, color=rojo)
plt.title("Total facturado por cliente", color=negro)
plt.xticks(rotation=45, color=negro)
plt.yticks(color=negro)
plt.gca().set_facecolor(blanco)
plt.tight_layout()
plt.savefig("report_facturado_por_cliente.png", dpi=300)
plt.show()

# -----------------------------
# 2. Ingresos mensuales (línea)
# -----------------------------
mensuales = session.query(func.month(Invoice.invoice_date), func.sum(Invoice.total))\
    .group_by(func.month(Invoice.invoice_date)).all()

meses = [m[0] for m in mensuales]
ingresos = [m[1] for m in mensuales]

plt.figure(figsize=(8,5))
plt.plot(meses, ingresos, marker="o", color=rojo)
plt.title("Ingresos mensuales", color=negro)
plt.xlabel("Mes", color=negro)
plt.ylabel("Ingresos (S/.)", color=negro)
plt.gca().set_facecolor(blanco)
plt.grid(True, color=negro, alpha=0.2)
plt.tight_layout()
plt.savefig("report_ingresos_mensuales.png", dpi=300)
plt.show()

# -----------------------------
# 3. Estado de facturas (pastel)
# -----------------------------
estado_facturas = session.query(Invoice.status, func.count(Invoice.id))\
    .group_by(Invoice.status).all()

labels = [e[0] for e in estado_facturas]
sizes = [e[1] for e in estado_facturas]
colors = [rojo, negro, blanco]

plt.figure(figsize=(6,6))
plt.pie(sizes, labels=labels, colors=colors, autopct="%1.1f%%", textprops={'color':negro})
plt.title("Estado de facturas", color=negro)
plt.savefig("report_estado_facturas.png", dpi=300)
plt.show()