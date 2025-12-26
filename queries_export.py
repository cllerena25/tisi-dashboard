import pandas as pd
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from models import Client, Invoice
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Conexión a MySQL
engine = create_engine("mysql+pymysql://tisi_app:TisiApp2025!@localhost:3307/tisi_facturas")
Session = sessionmaker(bind=engine)
session = Session()

# -----------------------------
# 1. Reporte: Total facturado por cliente
# -----------------------------
totales = session.query(Client.name, func.sum(Invoice.total))\
    .join(Invoice, Client.id == Invoice.client_id)\
    .group_by(Client.name).all()

df_totales = pd.DataFrame(totales, columns=["Cliente", "Total Facturado"])

# Exportar a Excel
df_totales.to_excel("report_facturado_por_cliente.xlsx", index=False)
print("✅ Reporte exportado a Excel: report_facturado_por_cliente.xlsx")

# -----------------------------
# 2. Reporte: Ingresos mensuales
# -----------------------------
mensuales = session.query(func.month(Invoice.invoice_date), func.sum(Invoice.total))\
    .group_by(func.month(Invoice.invoice_date)).all()

df_mensuales = pd.DataFrame(mensuales, columns=["Mes", "Ingresos"])

# Exportar a Excel
df_mensuales.to_excel("report_ingresos_mensuales.xlsx", index=False)
print("✅ Reporte exportado a Excel: report_ingresos_mensuales.xlsx")

# -----------------------------
# 3. Exportar a PDF (ambos reportes)
# -----------------------------
pdf_file = "reportes_facturacion.pdf"
c = canvas.Canvas(pdf_file, pagesize=letter)
c.setFont("Helvetica-Bold", 14)
c.drawString(200, 750, "Reporte de Facturación - TI Soluciones Integrales")

# Reporte 1: Totales por cliente
c.setFont("Helvetica", 12)
c.drawString(50, 720, "Total facturado por cliente:")
y = 700
for cliente, total in totales:
    c.drawString(60, y, f"{cliente}: S/. {total}")
    y -= 20

# Reporte 2: Ingresos mensuales
c.setFont("Helvetica", 12)
c.drawString(50, y-20, "Ingresos mensuales:")
y -= 40
for mes, ingreso in mensuales:
    c.drawString(60, y, f"Mes {mes}: S/. {ingreso}")
    y -= 20

c.save()
print(f"✅ Reporte exportado a PDF: {pdf_file}")