from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from models import Client, Invoice
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet

# Conexión a MySQL
engine = create_engine("mysql+pymysql://tisi_app:TisiApp2025!@localhost:3307/tisi_facturas")
Session = sessionmaker(bind=engine)
session = Session()

# Paleta institucional
rojo = colors.HexColor("#FF0000")
negro = colors.HexColor("#000000")
blanco = colors.HexColor("#FFFFFF")

# Crear documento PDF
pdf_file = "reportes_facturacion_avanzado.pdf"
doc = SimpleDocTemplate(pdf_file, pagesize=letter)
elements = []

# Estilos
styles = getSampleStyleSheet()
title_style = styles["Title"]
title_style.textColor = rojo
normal_style = styles["Normal"]

# Logo institucional (asegúrate de tener 'logo_tisi.png' en tu carpeta)
try:
    logo = Image("logo_tisi.png", width=120, height=60)
    elements.append(logo)
except:
    elements.append(Paragraph("TI Soluciones Integrales", title_style))

elements.append(Spacer(1, 20))
elements.append(Paragraph("📊 Reporte de Facturación", title_style))
elements.append(Spacer(1, 20))

# -----------------------------
# 1. Totales por cliente
# -----------------------------
totales = session.query(Client.name, func.sum(Invoice.total))\
    .join(Invoice, Client.id == Invoice.client_id)\
    .group_by(Client.name).all()

data_totales = [["Cliente", "Total Facturado (S/.)"]] + [[c[0], f"{c[1]:.2f}"] for c in totales]
tabla_totales = Table(data_totales, colWidths=[200, 200])
tabla_totales.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), rojo),
    ("TEXTCOLOR", (0,0), (-1,0), blanco),
    ("ALIGN", (0,0), (-1,-1), "CENTER"),
    ("GRID", (0,0), (-1,-1), 1, negro),
]))
elements.append(Paragraph("Total facturado por cliente:", normal_style))
elements.append(tabla_totales)
elements.append(Spacer(1, 20))

# -----------------------------
# 2. Ingresos mensuales
# -----------------------------
mensuales = session.query(func.month(Invoice.invoice_date), func.sum(Invoice.total))\
    .group_by(func.month(Invoice.invoice_date)).all()

data_mensuales = [["Mes", "Ingresos (S/.)"]] + [[m[0], f"{m[1]:.2f}"] for m in mensuales]
tabla_mensuales = Table(data_mensuales, colWidths=[200, 200])
tabla_mensuales.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), negro),
    ("TEXTCOLOR", (0,0), (-1,0), blanco),
    ("ALIGN", (0,0), (-1,-1), "CENTER"),
    ("GRID", (0,0), (-1,-1), 1, negro),
]))
elements.append(Paragraph("Ingresos mensuales:", normal_style))
elements.append(tabla_mensuales)
elements.append(Spacer(1, 20))

# Construir PDF
doc.build(elements)
print(f"✅ Reporte PDF generado: {pdf_file}")