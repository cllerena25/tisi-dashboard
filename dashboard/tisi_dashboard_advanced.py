import streamlit as st
import pandas as pd
import mysql.connector
import altair as alt
from io import BytesIO
from datetime import date, timedelta
from fpdf import FPDF

# --------------------------------------
# Configuración general de la página
# --------------------------------------
st.set_page_config(page_title="Dashboard de Facturación - TISI", page_icon="💼", layout="wide")

# --------------------------------------
# Conexión MySQL
# --------------------------------------
def get_connection():
    try:
        return mysql.connector.connect(
            host="localhost",
            port=3307,
            user="tisi_app",
            password="TisiApp2025!",
            database="tisi_factura"
        )
    except mysql.connector.Error as err:
        st.error(f"❌ Error al conectar con la base de datos: {err}")
        return None

# --------------------------------------
# Utilidades
# --------------------------------------
def convert_df_to_excel(df, sheet_name="Reporte"):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name=sheet_name)
    return output.getvalue()

def convert_df_to_pdf(df):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=10)
    col_width = pdf.w / (len(df.columns) + 1)
    row_height = pdf.font_size * 1.5
    # Encabezados
    for col in df.columns:
        pdf.cell(col_width, row_height, col, border=1)
    pdf.ln(row_height)
    # Filas
    for i in range(len(df)):
        for col in df.columns:
            pdf.cell(col_width, row_height, str(df.iloc[i][col]), border=1)
        pdf.ln(row_height)
    return pdf.output(dest="S").encode("latin-1")

@st.cache_data(ttl=300)
def load_invoices():
    conn = get_connection()
    if not conn:
        return pd.DataFrame()
    try:
        query = """
            SELECT i.id, i.invoice_number, c.ruc, c.name, i.invoice_date, i.total, i.currency, i.status, i.description, i.client_id, i.category
            FROM invoices i
            JOIN clients c ON i.client_id = c.id
        """
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"❌ Error al cargar facturas: {e}")
        return pd.DataFrame()

@st.cache_data(ttl=300)
def load_clients():
    conn = get_connection()
    if not conn:
        return pd.DataFrame()
    try:
        df = pd.read_sql("SELECT id, ruc, name, contact, email, phone FROM clients", conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"❌ Error al cargar clientes: {e}")
        return pd.DataFrame()

def refresh_data():
    load_invoices.clear()
    load_clients.clear()

# --------------------------------------
# Barra superior
# --------------------------------------
st.title("📊 Dashboard de Facturación - TISI")

col_a, col_b, col_c = st.columns([1,1,2])
with col_a:
    if st.button("🔄 Refrescar datos"):
        refresh_data()
        st.success("Datos refrescados")
with col_b:
    st.download_button(
        "📥 Exportar facturas (Excel)",
        data=convert_df_to_excel(load_invoices(), sheet_name="Facturas"),
        file_name="facturas_tisi.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

# --------------------------------------
# Filtros
# --------------------------------------
with st.sidebar:
    st.header("🔎 Filtros")
    df_clients = load_clients()
    df_invoices = load_invoices()

    min_date = pd.to_datetime(df_invoices["invoice_date"]).min() if not df_invoices.empty else date.today() - timedelta(days=90)
    max_date = pd.to_datetime(df_invoices["invoice_date"]).max() if not df_invoices.empty else date.today()
    date_range = st.date_input("Rango de fechas", [min_date.date(), max_date.date()])

    client_opt = ["(Todos)"] + sorted(df_clients["name"].tolist()) if not df_clients.empty else ["(Todos)"]
    client_selected = st.selectbox("Cliente", client_opt)

    status_selected = st.multiselect("Estado", ["Pendiente", "Pagada", "Vencida"], default=["Pendiente","Pagada","Vencida"])
    currency_selected = st.multiselect("Moneda", ["PEN","USD"], default=["PEN","USD"])
    category_selected = st.multiselect("Categoría", ["Consultoría","Licencias","Mantenimiento","Implementación","General"], default=["Consultoría","Licencias","Mantenimiento","Implementación","General"])

def apply_filters(df):
    if df.empty:
        return df
    d1, d2 = date_range
    dff = df.copy()
    dff = dff[(pd.to_datetime(dff["invoice_date"]).dt.date >= d1) & (pd.to_datetime(dff["invoice_date"]).dt.date <= d2)]
    if client_selected != "(Todos)":
        dff = dff[dff["name"] == client_selected]
    if status_selected:
        dff = dff[dff["status"].isin(status_selected)]
    if currency_selected:
        dff = dff[dff["currency"].isin(currency_selected)]
    if category_selected:
        dff = dff[dff["category"].isin(category_selected)]
    return dff

df_filtered = apply_filters(df_invoices)

# --------------------------------------
# Métricas ejecutivas
# --------------------------------------
st.subheader("📈 Métricas ejecutivas")
col1, col2, col3, col4 = st.columns(4)
total_facturado = df_filtered["total"].sum() if not df_filtered.empty else 0
pendiente = df_filtered[df_filtered["status"]=="Pendiente"]["total"].sum() if not df_filtered.empty else 0
pagado = df_filtered[df_filtered["status"]=="Pagada"]["total"].sum() if not df_filtered.empty else 0
vencido = df_filtered[df_filtered["status"]=="Vencida"]["total"].sum() if not df_filtered.empty else 0

with col1: st.metric("Total facturado", f"{total_facturado:,.2f}")
with col2: st.metric("Pendiente", f"{pendiente:,.2f}")
with col3: st.metric("Pagado", f"{pagado:,.2f}")
with col4: st.metric("Vencido", f"{vencido:,.2f}")

# --------------------------------------
# Tabs
# --------------------------------------
tab1, tab2, tab3 = st.tabs(["Tabla y exportación","Gráficos y tendencias","Registrar clientes y facturas"])

# Tab 1
with tab1:
    st.subheader("📑 Facturas filtradas")
    if df_filtered.empty:
        st.warning("⚠️ No hay facturas que coincidan con los filtros actuales.")
    else:
        st.dataframe(df_filtered[["invoice_number","ruc","name","invoice_date","total","currency","status","category","description"]], use_container_width=True)
        st.download_button("📥 Exportar filtradas a Excel", data=convert_df_to_excel(df_filtered,"Facturas filtradas"), file_name="facturas_filtradas.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        st.download_button("📄 Exportar filtradas a PDF", data=convert_df_to_pdf(df_filtered), file_name="facturas_filtradas.pdf", mime="application/pdf")

# Tab 2
with tab2:
    st.subheader("📊 Facturación por categoría")
    if not df_filtered.empty:
        df_cat = df_filtered.groupby("category", as_index=False)["total"].sum()
        chart_cat = alt.Chart(df_cat).mark_bar().encode(
            x=alt.X("category:N", sort="-y"),
            y=alt.Y("total:Q", axis=alt.Axis(format=",.2f")),
            tooltip=["category", alt.Tooltip("total", format=",.2f")]
        ).properties(height=350)
        st.altair_chart(chart_cat, use_container_width=True)
    else:
        st.info("Sin datos para el gráfico por categoría.")

    st.subheader("📊 Distribución por estado")
    if not df_filtered.empty:
        df_state = df_filtered.groupby("status", as_index=False)["total"].sum()
        chart_state = alt.Chart(df_state).mark_arc(innerRadius=40).encode(
            theta=alt.Theta(field="total", type="quantitative"),
            color=alt.Color(field="status", type="nominal"),
            tooltip=["status", alt.Tooltip("total", format=",.2f")]
        ).properties(width=350, height=300)
        st.altair_chart(chart_state, use_container_width=False)

    st.subheader("📊 Evolución mensual por moneda")
    if not df_filtered.empty:
        df_month_currency = df_filtered.copy()
        df_month_currency["month"] = pd.to_datetime(df_month_currency["invoice_date"]).dt.to_period("M").dt.to