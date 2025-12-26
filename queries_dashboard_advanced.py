import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from models import Client, Invoice
from datetime import datetime

# Conexión a MySQL
engine = create_engine("mysql+pymysql://tisi_app:TisiApp2025!@localhost:3307/tisi_facturas")
Session = sessionmaker(bind=engine)
session = Session()

# Paleta institucional
rojo = "#FF0000"
blanco = "#FFFFFF"
negro = "#000000"

# -----------------------------
# Consultas iniciales
# -----------------------------
clientes = session.query(Client.name).all()
clientes_list = [c[0] for c in clientes]

# -----------------------------
# Configuración del Dashboard
# -----------------------------
st.set_page_config(page_title="Dashboard Avanzado TI Soluciones", layout="wide")

st.title("📊 Dashboard Avanzado de Facturación - TI Soluciones Integrales")
st.markdown("---")

# Filtros dinámicos
st.sidebar.header("Filtros")
cliente_filtro = st.sidebar.selectbox("Seleccionar cliente", ["Todos"] + clientes_list)
fecha_inicio = st.sidebar.date_input("Fecha inicio", datetime(2025, 1, 1))
fecha_fin = st.sidebar.date_input("Fecha fin", datetime.now())
estado_filtro = st.sidebar.multiselect("Estado de facturas", ["pendiente", "pagada", "cancelada"], default=["pendiente","pagada","cancelada"])

# -----------------------------
# Aplicar filtros
# -----------------------------
query = session.query(Invoice).join(Client)

if cliente_filtro != "Todos":
    query = query.filter(Client.name == cliente_filtro)

query = query.filter(Invoice.invoice_date >= fecha_inicio, Invoice.invoice_date <= fecha_fin)
query = query.filter(Invoice.status.in_(estado_filtro))

facturas_filtradas = query.all()

# Convertir a DataFrame
df_facturas = pd.DataFrame([{
    "Cliente": f.client.name,
    "Fecha": f.invoice_date,
    "Total": f.total,
    "Estado": f.status
} for f in facturas_filtradas])

st.subheader("📑 Facturas filtradas")
st.dataframe(df_facturas)
import io
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

# Exportar a Excel desde el dashboard
excel_buffer = io.BytesIO()
df_facturas.to_excel(excel_buffer, index=False)
st.download_button(
    label="📥 Descargar en Excel",
    data=excel_buffer.getvalue(),
    file_name="facturas_filtradas.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

# Exportar a PDF desde el dashboard
pdf_buffer = io.BytesIO()
doc = SimpleDocTemplate(pdf_buffer, pagesize=letter)
elements = []
styles = getSampleStyleSheet()
elements.append(Paragraph("Reporte de Facturación - TI Soluciones Integrales", styles["Title"]))

data = [["Cliente", "Fecha", "Total", "Estado"]] + df_facturas.values.tolist()
tabla = Table(data, colWidths=[100,100,100,100])
tabla.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), colors.red),
    ("TEXTCOLOR", (0,0), (-1,0), colors.white),
    ("GRID", (0,0), (-1,-1), 1, colors.black),
]))
elements.append(tabla)
doc.build(elements)

st.download_button(
    label="📥 Descargar en PDF",
    data=pdf_buffer.getvalue(),
    file_name="facturas_filtradas.pdf",
    mime="application/pdf"
)

# -----------------------------
# Gráfico: Totales por cliente
# -----------------------------
if not df_facturas.empty:
    df_totales = df_facturas.groupby("Cliente")["Total"].sum().reset_index()

    fig1, ax1 = plt.subplots()
    ax1.bar(df_totales["Cliente"], df_totales["Total"], color=rojo)
    ax1.set_title("Total facturado por cliente", color=negro)
    ax1.set_facecolor(blanco)
    st.pyplot(fig1)

    # Gráfico: Ingresos mensuales
    df_facturas["Mes"] = df_facturas["Fecha"].dt.month
    df_mensuales = df_facturas.groupby("Mes")["Total"].sum().reset_index()

    fig2, ax2 = plt.subplots()
    ax2.plot(df_mensuales["Mes"], df_mensuales["Total"], marker="o", color=rojo)
    ax2.set_title("Ingresos mensuales", color=negro)
    ax2.set_facecolor(blanco)
    st.pyplot(fig2)

    # Gráfico: Estado de facturas
    df_estado = df_facturas.groupby("Estado")["Total"].count().reset_index()

    fig3, ax3 = plt.subplots()
    ax3.pie(df_estado["Total"], labels=df_estado["Estado"], autopct="%1.1f%%", colors=[rojo, negro, blanco],
            textprops={'color': negro})
    ax3.set_title("Estado de facturas", color=negro)
    st.pyplot(fig3)
else:
    st.warning("⚠️ No hay facturas que coincidan con los filtros seleccionados.")