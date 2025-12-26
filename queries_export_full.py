import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
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
rojo = "#FF0000"
blanco = "#FFFFFF"
negro = "#000000"

# -----------------------------
# 1. Consultas de datos
# -----------------------------
totales = session.query(Client.name, func.sum(Invoice.total))\
    .join(Invoice, Client.id == Invoice.client_id)\
    .group_by(Client.name).all()

mensuales = session.query(func.month(Invoice.invoice_date), func.sum(Invoice.total))\
    .group_by(func.month(Invoice.invoice_date)).all()

estado_facturas = session.query(Invoice.status, func.count(Invoice.id))\
    .group_by(Invoice.status).all()

# -----------------------------
# 2. Exportar a Excel
# -----------------------------
df_totales = pd.DataFrame(totales, columns=["Cliente", "Total Facturado"])
df_mensuales = pd.DataFrame(mensuales, columns=["Mes", "Ingresos"])
df_totales.to_excel("report_facturado_por_cliente.xlsx", index=False)
df_mensuales.to_excel("report_ingresos_mensuales.xlsx", index=False)

print("✅ Excel generado: report_facturado_por_cliente.xlsx, report_ingresos_mensuales.xlsx")

# -----------------------------
# 3. Exportar a PDF avanzado
# -----------------------------
pdf_file = "reportes_facturacion_avanzado.pdf"
doc = SimpleDocTemplate(pdf_file, pagesize=letter)
elements = []
styles = getSampleStyleSheet()
title_style = styles["Title"]
title_style.textColor = colors.HexColor(rojo)
normal_style = styles["Normal"]

# Logo institucional
try:
    logo = Image("logo_tisi.png", width=120, height=60)
    elements.append(logo)
except:
    elements.append(Paragraph("TI Soluciones Integrales", title_style))

elements.append(Spacer(1, 20))
elements.append(Paragraph("📊 Reporte de Facturación", title_style))
elements.append(Spacer(1, 20))

# Tabla Totales por Cliente
data_totales = [["Cliente", "Total Facturado (S/.)"]] + [[c[0], f"{c[1]:.2f}"] for c in totales]
tabla_totales = Table(data_totales, colWidths=[200, 200])
tabla_totales.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), colors.HexColor(rojo)),
    ("TEXTCOLOR", (0,0), (-1,0), colors.HexColor(blanco)),
    ("ALIGN", (0,0), (-1,-1), "CENTER"),
    ("GRID", (0,0), (-1,-1), 1, colors.HexColor(negro)),
]))
elements.append(Paragraph("Total facturado por cliente:", normal_style))
elements.append(tabla_totales)
elements.append(Spacer(1, 20))

# Tabla Ingresos Mensuales
data_mensuales = [["Mes", "Ingresos (S/.)"]] + [[m[0], f"{m[1]:.2f}"] for m in mensuales]
tabla_mensuales = Table(data_mensuales, colWidths=[200, 200])
tabla_mensuales.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), colors.HexColor(negro)),
    ("TEXTCOLOR", (0,0), (-1,0), colors.HexColor(blanco)),
    ("ALIGN", (0,0), (-1,-1), "CENTER"),
    ("GRID", (0,0), (-1,-1), 1, colors.HexColor(negro)),
]))
elements.append(Paragraph("Ingresos mensuales:", normal_style))
elements.append(tabla_mensuales)
elements.append(Spacer(1, 20))

doc.build(elements)
print(f"✅ PDF generado: {pdf_file}")

# -----------------------------
# 4. Gráficos PNG
# -----------------------------
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
plt.close()

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
plt.close()

labels = [e[0] for e in estado_facturas]
sizes = [e[1] for e in estado_facturas]
colors_pie = [rojo, negro, blanco]

plt.figure(figsize=(6,6))
plt.pie(sizes, labels=labels, colors=colors_pie, autopct="%1.1f%%", textprops={'color':negro})
plt.title("Estado de facturas", color=negro)
plt.savefig("report_estado_facturas.png", dpi=300)
plt.close()

print("✅ Gráficos PNG generados: report_facturado_por_cliente.png, report_ingresos_mensuales.png, report_estado_facturas.png")