import streamlit as st
import pandas as pd
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
# Consultas de datos
# -----------------------------
totales = session.query(Client.name, func.sum(Invoice.total))\
    .join(Invoice, Client.id == Invoice.client_id)\
    .group_by(Client.name).all()

mensuales = session.query(func.month(Invoice.invoice_date), func.sum(Invoice.total))\
    .group_by(func.month(Invoice.invoice_date)).all()

estado_facturas = session.query(Invoice.status, func.count(Invoice.id))\
    .group_by(Invoice.status).all()

# -----------------------------
# Dashboard Streamlit
# -----------------------------
st.set_page_config(page_title="Dashboard Facturación TI Soluciones", layout="wide")

st.title("📊 Dashboard de Facturación - TI Soluciones Integrales")
st.markdown("---")

# Totales por cliente
st.subheader("Total facturado por cliente")
df_totales = pd.DataFrame(totales, columns=["Cliente", "Total Facturado"])
st.dataframe(df_totales)

fig1, ax1 = plt.subplots()
ax1.bar(df_totales["Cliente"], df_totales["Total Facturado"], color=rojo)
ax1.set_title("Total facturado por cliente", color=negro)
ax1.set_facecolor(blanco)
st.pyplot(fig1)

# Ingresos mensuales
st.subheader("Ingresos mensuales")
df_mensuales = pd.DataFrame(mensuales, columns=["Mes", "Ingresos"])
st.dataframe(df_mensuales)

fig2, ax2 = plt.subplots()
ax2.plot(df_mensuales["Mes"], df_mensuales["Ingresos"], marker="o", color=rojo)
ax2.set_title("Ingresos mensuales", color=negro)
ax2.set_facecolor(blanco)
st.pyplot(fig2)

# Estado de facturas
st.subheader("Estado de facturas")
df_estado = pd.DataFrame(estado_facturas, columns=["Estado", "Cantidad"])
st.dataframe(df_estado)

fig3, ax3 = plt.subplots()
ax3.pie(df_estado["Cantidad"], labels=df_estado["Estado"], autopct="%1.1f%%", colors=[rojo, negro, blanco],
        textprops={'color': negro})
ax3.set_title("Estado de facturas", color=negro)
st.pyplot(fig3)

st.markdown("---")
st.success("✅ Dashboard cargado con éxito. Usa los filtros de Streamlit para explorar tus datos.")