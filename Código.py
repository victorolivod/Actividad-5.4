import streamlit as st
import pandas as pd
import plotly.express as px

# Título general del tablero
st.title("Análisis Integral de Pedidos y Ventas")

# Carga de datos desde Excel
@st.cache_data
def cargar_datos():
    df = pd.read_excel('df_DataBridgeConsulting (4).xlsx')
    # Limpieza de nombres de columnas
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
    return df

df = cargar_datos()

# Sidebar con filtros interactivos
st.sidebar.header("Filtros Interactivos")
region = st.sidebar.selectbox(
    "Selecciona una región:",
    sorted(df['region'].dropna().unique())
)
categoria = st.sidebar.selectbox(
    "Selecciona categoría simplificada:",
    sorted(df['categoria_simplificada'].dropna().unique())
)

# Conversión de columna de fecha
df['orden_compra_timestamp'] = pd.to_datetime(df['orden_compra_timestamp'], errors='coerce')
fechas_validas = df['orden_compra_timestamp'].dropna()

# Convertir a tipo date para el slider
min_fecha = fechas_validas.min().date()
max_fecha = fechas_validas.max().date()

rango_fecha = st.sidebar.slider(
    "Rango de fecha de compra:",
    min_value=min_fecha,
    max_value=max_fecha,
    value=(min_fecha, max_fecha),
    format="YYYY-MM-DD"
)

# Filtrado de datos usando fechas como date
df_filtro = df[
    (df['region'] == region) &
    (df['categoria_simplificada'] == categoria) &
    (df['orden_compra_timestamp'].dt.date >= rango_fecha[0]) &
    (df['orden_compra_timestamp'].dt.date <= rango_fecha[1])
]

# Layout con Tabs para organización
tab1, tab2 = st.tabs(["Visualizaciones", "Narrativa del Análisis"])

with tab1:
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Ventas por Categoría Simplificada")
        fig1 = px.bar(
            df_filtro,
            x='categoria_simplificada', 
            y='precio_final', 
            title="Ventas por Categoría Simplificada"
        )
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        st.subheader("Evolución Temporal de Ventas")
        ventas_por_fecha = df_filtro.groupby('orden_compra_timestamp')['precio_final'].sum().reset_index()
        fig2 = px.line(
            ventas_por_fecha, 
            x='orden_compra_timestamp', 
            y='precio_final', 
            title="Ventas a lo Largo del Tiempo"
        )
        st.plotly_chart(fig2, use_container_width=True)

    col3, col4 = st.columns(2)

    with col3:
        st.subheader("Distribución del Ticket Promedio")
        fig3 = px.histogram(
            df_filtro, 
            x='ticket_promedio', 
            nbins=20, 
            title="Ticket Promedio"
        )
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        st.subheader("Pedidos por Región")
        pedidos_por_region = df.groupby('region').size().reset_index(name='num_pedidos')
        fig4 = px.bar(
            pedidos_por_region, 
            x='region', 
            y='num_pedidos', 
            title="Pedidos por Región"
        )
        st.plotly_chart(fig4, use_container_width=True)

with tab2:
    st.header("Narrativa del Análisis")
    st.markdown("""
    **Inicio**  
    Este dashboard presenta un análisis integral de los pedidos y ventas registrados, permitiendo filtrar por región, categoría simplificada y rango de fechas.

    **Hallazgos**  
    - La gráfica de barras muestra las categorías simplificadas con mayores ventas.
    - El gráfico temporal permite identificar tendencias estacionales y picos de ventas.
    - El histograma de ticket promedio revela la concentración de pedidos en ciertos rangos de valor.
    - El gráfico de pedidos por región destaca las zonas con mayor actividad comercial.

    **Análisis**  
    El análisis revela que ciertas regiones y categorías concentran la mayor parte de las ventas, y que existen temporadas con picos significativos. Además, la distribución del ticket promedio ayuda a identificar oportunidades de optimización comercial.

    **Recomendaciones**  
    - Focalizar estrategias comerciales en las regiones y categorías con mayor potencial.
    - Ajustar inventarios y logística en función de los picos de demanda detectados.
    - Analizar a fondo los segmentos de clientes más rentables para personalizar ofertas.
    """)

# Nota: Asegúrate de que los nombres de las columnas coincidan exactamente con los de tu archivo Excel.
# Sube este archivo junto con 'df_DataBridgeConsulting (4).xlsx' y un requirements.txt a tu repositorio de GitHub.

