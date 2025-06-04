import streamlit as st
import pandas as pd
import plotly.express as px

# Título general del tablero
st.title("Análisis Integral de Pedidos y Ventas")

# Carga de datos desde Excel
@st.cache_data
def cargar_datos():
    df = pd.read_excel('df_DataBridgeConsulting (4).xlsx')
    df.columns = df.columns.str.strip()  # Limpia espacios en los nombres de columna
    return df

df = cargar_datos()

# Sidebar con filtros interactivos
st.sidebar.header("Filtros Interactivos")
region = st.sidebar.selectbox(
    "Selecciona una región:",
    sorted(df['region'].dropna().unique())
)
categoria = st.sidebar.selectbox(
    "Selecciona categoría de producto:",
    sorted(df['categoria_producto'].dropna().unique())
)

# Conversión de columna de fecha
df['fecha_compra_datetime'] = pd.to_datetime(df['fecha_compra_datetime'], errors='coerce')

rango_fecha = st.sidebar.slider(
    "Rango de fecha de compra:",
    min_value=df['fecha_compra_datetime'].min(),
    max_value=df['fecha_compra_datetime'].max(),
    value=(df['fecha_compra_datetime'].min(), df['fecha_compra_datetime'].max()),
    format="YYYY-MM-DD"
)

# Filtrado de datos
df_filtro = df[
    (df['region'] == region) &
    (df['categoria_producto'] == categoria) &
    (df['fecha_compra_datetime'] >= rango_fecha[0]) &
    (df['fecha_compra_datetime'] <= rango_fecha[1])
]

# Layout con Tabs para organización
tab1, tab2 = st.tabs(["Visualizaciones", "Narrativa del Análisis"])

with tab1:
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Ventas por Categoría de Producto")
        fig1 = px.bar(
            df_filtro,
            x='categoria_producto', 
            y='precio_final', 
            title="Ventas por Categoría"
        )
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        st.subheader("Evolución Temporal de Ventas")
        ventas_por_fecha = df_filtro.groupby('fecha_compra_datetime')['precio_final'].sum().reset_index()
        fig2 = px.line(
            ventas_por_fecha, 
            x='fecha_compra_datetime', 
            y='precio_final', 
            title="Ventas a lo Largo del Tiempo"
        )
        st.plotly_chart(fig2, use_container_width=True)

    col3, col4 = st.columns(2)

    with col3:
        st.subheader("Distribución del Precio Promedio por Pedido")
        fig3 = px.histogram(
            df_filtro, 
            x='precio_promedio_por_pedido', 
            nbins=20, 
            title="Precio Promedio por Pedido"
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
    Este dashboard presenta un análisis integral de los pedidos y ventas registrados, permitiendo filtrar por región, categoría de producto y rango de fechas.

    **Hallazgos**  
    - La gráfica de barras muestra las categorías de producto con mayores ventas.
    - El gráfico temporal permite identificar tendencias estacionales y picos de ventas.
    - El histograma de precio promedio revela la concentración de pedidos en ciertos rangos de precio.
    - El gráfico de pedidos por región destaca las zonas con mayor actividad comercial.

    **Análisis**  
    El análisis revela que ciertas regiones y categorías concentran la mayor parte de las ventas, y que existen temporadas con picos significativos. Además, la distribución de precios ayuda a identificar oportunidades de optimización comercial.

    **Recomendaciones**  
    - Focalizar estrategias comerciales en las regiones y categorías con mayor potencial.
    - Ajustar inventarios y logística en función de los picos de demanda detectados.
    - Analizar a fondo los segmentos de clientes más rentables para personalizar ofertas.
    """)
