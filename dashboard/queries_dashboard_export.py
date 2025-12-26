import streamlit as st
import pandas as pd
import mysql.connector
from io import BytesIO

def get_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            port=3307,
            user="tisi_app",
            password="TisiApp2025!",
            database="tisi_factura"
        )
        return conn
    except mysql.connector.Error as err:
        st.error(f"❌ Error al conectar con la base de datos: {err}")
        return None

def convert_df_to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Facturas")
    return output.getvalue()

st.title("📊 Dashboard de Facturación - TISI")

st.sidebar.header("🔎 Filtros")
filter_client = st.sidebar.text_input("RUC o Razón Social")
filter_status = st.sidebar.selectbox("Estado de factura", ["", "Pendiente", "Pagada", "Vencida"])
filter_currency = st.sidebar.selectbox("Moneda", ["", "PEN", "USD"])

conn = get_connection()
if conn:
    try:
        query = """
            SELECT i.invoice_number, c.ruc, c.name, i.invoice_date, i.total, i.currency, i.status, i.description
            FROM invoices i
            JOIN clients c ON i.client_id = c.id
        """
        df_invoices = pd.read_sql(query, conn)
        conn.close()
    except Exception as e:
        st.error(f"❌ Error al ejecutar la consulta: {e}")
        st.stop()

    if filter_client:
        df_invoices = df_invoices[
            df_invoices["ruc"].str.contains(filter_client, case=False) |
            df_invoices["name"].str.contains(filter_client, case=False)
        ]

    if filter_status:
        df_invoices = df_invoices[df_invoices["status"] == filter_status]

    if filter_currency:
        df_invoices = df_invoices[df_invoices["currency"] == filter_currency]

    if df_invoices.empty:
        st.warning("⚠️ No hay facturas que coincidan con los filtros aplicados en el dashboard.")
    else:
        st.subheader("📑 Facturas encontradas")
        st.dataframe(df_invoices, use_container_width=True)

        st.download_button(
            label="📥 Exportar facturas a Excel",
            data=convert_df_to_excel(df_invoices),
            file_name="facturas_filtradas.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )