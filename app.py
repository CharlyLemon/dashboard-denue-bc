import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
from datetime import datetime
import json

# ===============================================
# CONFIGURACIÓN DE PÁGINA (DEBE SER PRIMERO)
# ===============================================
st.set_page_config(
    page_title="Dashboard DENUE BC",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===============================================
# CONFIGURACIÓN API INEGI
# ===============================================
TOKEN_INEGI = "28912e56-e90b-9886-140c-7518f9e11928"
API_BASE_URL = "https://www.inegi.org.mx/app/api/denue/v1"

# ===============================================
# FUNCIÓN PARA CONSULTAR API INEGI
# ===============================================
@st.cache_data(ttl=3600)  # Cache por 1 hora
def obtener_datos_inegi(endpoint, params=None):
    """Consulta la API de INEGI con manejo de errores"""
    try:
        headers = {"token": TOKEN_INEGI}
        url = f"{API_BASE_URL}/{endpoint}"
        response = requests.get(url, headers=headers, params=params, timeout=10)
        
        if response.status_code == 200:
            return response.json()
        else:
            st.warning(f"⚠️ API INEGI no disponible (código {response.status_code}). Usando datos de respaldo.")
            return None
    except Exception as e:
        st.warning(f"⚠️ Error al conectar con API INEGI. Usando datos de respaldo.")
        return None

# ===============================================
# DATOS ESTÁTICOS (FALLBACK)
# ===============================================

DATOS_BC = {
    'establecimientos': 138604,
    'empleados': 330000,
    'informalidad': 37.7,
    'formalidad': 62.3,
    'mujeres': 41.3,
    'internet': 45.1,
    'exportaciones': 60558,
    'porcentaje_nacional': 2.29,
    'empleo_porcentaje_nacional': 1.18
}

DATOS_NACIONALES = {
    'establecimientos': 6050000,
    'informalidad': 49.5,
    'formalidad': 50.5,
    'internet': 35.2
}

DATOS_MUNICIPIOS = pd.DataFrame({
    'Municipio': ['Tijuana', 'Mexicali', 'Ensenada', 'Tecate', 'Rosarito'],
    'Establecimientos': [62072, 38761, 20791, 6931, 10049],
    'Empleados': [148500, 91575, 49500, 19800, 20625],
    'Porcentaje': [44.8, 28.0, 15.0, 5.0, 7.2]
})

DATOS_SECTORES = pd.DataFrame({
    'Sector': ['Comercio', 'Servicios', 'Manufactura', 'Construcción', 'Otros'],
    'Establecimientos': [55442, 48452, 15246, 9690, 9774],
    'Porcentaje': [40.0, 35.0, 11.0, 7.0, 7.0]
})

DATOS_TENDENCIAS = pd.DataFrame({
    'Año': [2019, 2020, 2021, 2022, 2023, 2024],
    'Establecimientos': [125000, 118000, 122000, 128000, 133000, 138604],
    'Empleo': [295000, 275000, 285000, 305000, 318000, 330000]
})

DATOS_COMPARATIVA = pd.DataFrame({
    'Estado': ['Baja California', 'Nuevo León'],
    'Establecimientos': [138604, 185000],
    'Formalidad': [62.3, 65.8],
    'Internet': [45.1, 42.3],
    'Exportaciones': [60.6, 45.2]
})

# ===============================================
# FUNCIONES AUXILIARES
# ===============================================

def formato_numero(numero):
    """Formatea números con comas para miles"""
    return f"{numero:,}".replace(",", ",")

def crear_metrica_kpi(titulo, valor, delta=None, porcentaje=False):
    """Crea una métrica KPI estilizada"""
    if porcentaje:
        valor_formato = f"{valor}%"
    else:
        valor_formato = formato_numero(int(valor))
    
    st.metric(label=titulo, value=valor_formato, delta=delta)

def crear_boton_descarga_csv(df, nombre_archivo, label="📥 Descargar CSV"):
    """Genera botón de descarga para DataFrame"""
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label=label,
        data=csv,
        file_name=f"{nombre_archivo}_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )

def agregar_linea_referencia(fig, valor, texto, color="red"):
    """Agrega línea de referencia horizontal a gráfica"""
    fig.add_hline(
        y=valor,
        line_dash="dash",
        annotation_text=texto,
        line_color=color,
        annotation_position="bottom right"
    )
    return fig

# ===============================================
# SIDEBAR - CONTROLES GLOBALES
# ===============================================

st.sidebar.title("🎛️ Controles")

# Filtro de año
año_seleccionado = st.sidebar.selectbox(
    "📅 Año de análisis:",
    [2019, 2020, 2021, 2022, 2023, 2024],
    index=5  # Default: 2024
)

# Filtro de municipio (para análisis específicos)
municipios_disponibles = ['Todos'] + DATOS_MUNICIPIOS['Municipio'].tolist()
municipio_filtro = st.sidebar.selectbox(
    "📍 Municipio:",
    municipios_disponibles
)

# Selector de sector
sectores_disponibles = ['Todos'] + DATOS_SECTORES['Sector'].tolist()
sector_filtro = st.sidebar.selectbox(
    "🏭 Sector:",
    sectores_disponibles
)

st.sidebar.markdown("---")

# Estado de conexión API
with st.sidebar:
    st.markdown("### 🔌 Estado API INEGI")
    test_api = obtener_datos_inegi("consulta/BuscarEntidad/02")
    if test_api:
        st.success("✅ Conectado")
    else:
        st.warning("⚠️ Modo offline")

st.sidebar.markdown("---")
st.sidebar.info("💡 **Tip:** Usa los filtros para análisis personalizados")

# ===============================================
# HEADER PRINCIPAL
# ===============================================

st.title("📊 Dashboard DENUE - Baja California")
st.markdown(f"### Análisis Económico {año_seleccionado}")
st.markdown("**Secretaría de Economía e Innovación**")
st.markdown("---")

# ===============================================
# TABS DE NAVEGACIÓN
# ===============================================

tabs = st.tabs([
    "🏠 Visión General",
    "📍 Competencia por Zona",
    "⚖️ BC vs Nuevo León",
    "🏭 Sectores",
    "📈 Tendencias",
    "💻 Digitalización",
    "👥 Género & Financiamiento"
])

# ===============================================
# TAB 1: VISIÓN GENERAL
# ===============================================

with tabs[0]:
    st.header("Panorama General de Baja California")
    
    # Tooltip informativo
    st.info("💡 **Establecimientos económicos**: Unidades productivas registradas en DENUE que realizan actividades económicas (comercios, fábricas, oficinas, etc.)")
    
    # KPIs principales
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        crear_metrica_kpi("Establecimientos", DATOS_BC['establecimientos'])
    with col2:
        crear_metrica_kpi("Empleados", DATOS_BC['empleados'])
    with col3:
        crear_metrica_kpi("Formalidad", DATOS_BC['formalidad'], porcentaje=True)
    with col4:
        crear_metrica_kpi("Conectividad", DATOS_BC['internet'], porcentaje=True)
    
    st.markdown("---")
    
    # Comparativa BC vs Nacional
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 BC vs Nacional")
        
        # Gráfica de formalidad con línea de referencia
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=['Baja California', 'Nacional'],
            y=[DATOS_BC['formalidad'], DATOS_NACIONALES['formalidad']],
            marker_color=['#1f77b4', '#ff7f0e'],
            text=[f"{DATOS_BC['formalidad']}%", f"{DATOS_NACIONALES['formalidad']}%"],
            textposition='auto'
        ))
        
        fig = agregar_linea_referencia(
            fig, 
            DATOS_NACIONALES['formalidad'],
            f"Promedio Nacional: {DATOS_NACIONALES['formalidad']}%",
            "red"
        )
        
        fig.update_layout(
            title="Tasa de Formalidad",
            yaxis_title="Porcentaje (%)",
            showlegend=False,
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("🌐 Conectividad Digital")
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=['Baja California', 'Nacional'],
            y=[DATOS_BC['internet'], DATOS_NACIONALES['internet']],
            marker_color=['#2ca02c', '#d62728'],
            text=[f"{DATOS_BC['internet']}%", f"{DATOS_NACIONALES['internet']}%"],
            textposition='auto'
        ))
        
        fig.update_layout(
            title="Acceso a Internet",
            yaxis_title="Porcentaje (%)",
            showlegend=False,
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Botón de descarga
    st.markdown("---")
    df_resumen = pd.DataFrame({
        'Indicador': ['Establecimientos', 'Empleados', 'Formalidad (%)', 'Internet (%)'],
        'Baja California': [
            DATOS_BC['establecimientos'],
            DATOS_BC['empleados'],
            DATOS_BC['formalidad'],
            DATOS_BC['internet']
        ]
    })
    crear_boton_descarga_csv(df_resumen, "resumen_bc", "📥 Descargar datos generales")

# ===============================================
# TAB 2: COMPETENCIA POR ZONA
# ===============================================

with tabs[1]:
    st.header("📍 Análisis por Municipio")
    
    st.info("💡 **Concentración empresarial**: Tijuana y Mexicali concentran el 72.8% de los establecimientos del estado")
    
    # Filtrar por municipio si se seleccionó uno específico
    if municipio_filtro != 'Todos':
        df_filtrado = DATOS_MUNICIPIOS[DATOS_MUNICIPIOS['Municipio'] == municipio_filtro]
        st.warning(f"🔍 Mostrando datos de: **{municipio_filtro}**")
    else:
        df_filtrado = DATOS_MUNICIPIOS
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🏢 Establecimientos por Municipio")
        fig = px.bar(
            df_filtrado,
            x='Municipio',
            y='Establecimientos',
            text='Establecimientos',
            color='Municipio',
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig.update_traces(texttemplate='%{text:,}', textposition='outside')
        fig.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("👥 Empleados por Municipio")
        fig = px.bar(
            df_filtrado,
            x='Municipio',
            y='Empleados',
            text='Empleados',
            color='Municipio',
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig.update_traces(texttemplate='%{text:,}', textposition='outside')
        fig.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    # Tabla detallada
    st.subheader("📋 Tabla Detallada")
    st.dataframe(df_filtrado, use_container_width=True)
    
    # Botón de descarga
    crear_boton_descarga_csv(df_filtrado, "municipios_bc", "📥 Descargar datos por municipio")

# ===============================================
# TAB 3: BC VS NUEVO LEÓN
# ===============================================

with tabs[2]:
    st.header("⚖️ Baja California vs Nuevo León")
    
    st.info("💡 **Comparativa estratégica**: Nuevo León es el principal competidor de BC en captación de inversión industrial")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Establecimientos")
        fig = px.bar(
            DATOS_COMPARATIVA,
            x='Estado',
            y='Establecimientos',
            text='Establecimientos',
            color='Estado',
            color_discrete_map={
                'Baja California': '#1f77b4',
                'Nuevo León': '#ff7f0e'
            }
        )
        fig.update_traces(texttemplate='%{text:,}', textposition='outside')
        fig.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("📡 Formalidad vs Internet")
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=DATOS_COMPARATIVA['Formalidad'],
            y=DATOS_COMPARATIVA['Internet'],
            mode='markers+text',
            marker=dict(size=DATOS_COMPARATIVA['Establecimientos']/1000, color=['#1f77b4', '#ff7f0e']),
            text=DATOS_COMPARATIVA['Estado'],
            textposition='top center'
        ))
        fig.update_layout(
            xaxis_title="Formalidad (%)",
            yaxis_title="Conectividad Internet (%)",
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Exportaciones
    st.subheader("📦 Exportaciones 2024 (Miles de millones USD)")
    fig = px.bar(
        DATOS_COMPARATIVA,
        x='Estado',
        y='Exportaciones',
        text='Exportaciones',
        color='Estado',
        color_discrete_map={
            'Baja California': '#2ca02c',
            'Nuevo León': '#d62728'
        }
    )
    fig.update_traces(texttemplate='$%{text}B', textposition='outside')
    fig.update_layout(showlegend=False, height=400)
    st.plotly_chart(fig, use_container_width=True)
    
    # Descarga
    crear_boton_descarga_csv(DATOS_COMPARATIVA, "bc_vs_nl", "📥 Descargar comparativa")

# ===============================================
# TAB 4: SECTORES
# ===============================================

with tabs[3]:
    st.header("🏭 Distribución Sectorial (SCIAN)")
    
    st.info("💡 **Sector SCIAN**: Sistema de Clasificación Industrial de América del Norte usado para categorizar actividades económicas")
    
    # Filtrar por sector si se seleccionó uno específico
    if sector_filtro != 'Todos':
        df_sector_filtrado = DATOS_SECTORES[DATOS_SECTORES['Sector'] == sector_filtro]
        st.warning(f"🔍 Mostrando datos de: **{sector_filtro}**")
    else:
        df_sector_filtrado = DATOS_SECTORES
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🥧 Participación por Sector")
        fig = px.pie(
            df_sector_filtrado,
            values='Porcentaje',
            names='Sector',
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("📊 Establecimientos por Sector")
        fig = px.bar(
            df_sector_filtrado.sort_values('Establecimientos', ascending=True),
            y='Sector',
            x='Establecimientos',
            text='Establecimientos',
            orientation='h',
            color='Sector',
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig.update_traces(texttemplate='%{text:,}', textposition='outside')
        fig.update_layout(showlegend=False, height=500)
        st.plotly_chart(fig, use_container_width=True)
    
    # Tabla
    st.subheader("📋 Detalle Sectorial")
    st.dataframe(df_sector_filtrado, use_container_width=True)
    
    # Descarga
    crear_boton_descarga_csv(df_sector_filtrado, "sectores_bc", "📥 Descargar datos sectoriales")

# ===============================================
# TAB 5: TENDENCIAS
# ===============================================

with tabs[4]:
    st.header("📈 Tendencias 2019-2024")
    
    st.info("💡 **Crecimiento post-pandemia**: BC mostró recuperación sostenida desde 2021, superando niveles pre-COVID en 2023")
    
    # Filtrar por año
    df_tendencias_filtrado = DATOS_TENDENCIAS[DATOS_TENDENCIAS['Año'] <= año_seleccionado]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Evolución de Establecimientos")
        fig = px.line(
            df_tendencias_filtrado,
            x='Año',
            y='Establecimientos',
            markers=True,
            text='Establecimientos'
        )
        fig.update_traces(texttemplate='%{text:,}', textposition='top center')
        fig.update_layout(height=400, yaxis_title="Establecimientos")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("👥 Evolución del Empleo")
        fig = px.line(
            df_tendencias_filtrado,
            x='Año',
            y='Empleo',
            markers=True,
            text='Empleo',
            line_shape='spline'
        )
        fig.update_traces(texttemplate='%{text:,}', textposition='top center', line_color='#ff7f0e')
        fig.update_layout(height=400, yaxis_title="Empleados")
        st.plotly_chart(fig, use_container_width=True)
    
    # Crecimiento anual
    st.subheader("📊 Tasa de Crecimiento Anual")
    df_crecimiento = df_tendencias_filtrado.copy()
    df_crecimiento['Crecimiento (%)'] = df_crecimiento['Establecimientos'].pct_change() * 100
    
    fig = px.bar(
        df_crecimiento[1:],  # Excluir primer año sin dato
        x='Año',
        y='Crecimiento (%)',
        text='Crecimiento (%)',
        color='Crecimiento (%)',
        color_continuous_scale=['red', 'yellow', 'green']
    )
    fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)
    
    # Descarga
    crear_boton_descarga_csv(df_tendencias_filtrado, "tendencias_bc", "📥 Descargar serie histórica")

# ===============================================
# TAB 6: DIGITALIZACIÓN
# ===============================================

with tabs[5]:
    st.header("💻 Adopción Digital")
    
    st.info("💡 **Brecha digital**: BC lidera en conectividad pero e-commerce aún está por debajo del promedio nacional")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🌐 Acceso a Internet")
        st.metric("BC - Conectividad", f"{DATOS_BC['internet']}%", delta=f"+{DATOS_BC['internet'] - DATOS_NACIONALES['internet']:.1f}% vs Nacional")
        
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=DATOS_BC['internet'],
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Internet en Establecimientos (%)"},
            delta={'reference': DATOS_NACIONALES['internet']},
            gauge={
                'axis': {'range': [None, 100]},
                'bar': {'color': "#1f77b4"},
                'steps': [
                    {'range': [0, 30], 'color': "lightgray"},
                    {'range': [30, 40], 'color': "gray"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': DATOS_NACIONALES['internet']
                }
            }
        ))
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("🛒 E-commerce")
        st.metric("BC - Ventas Online", "8.5%", delta="-2.8% vs Nacional")
        
        df_ecommerce = pd.DataFrame({
            'Categoría': ['Con e-commerce', 'Sin e-commerce'],
            'Porcentaje': [8.5, 91.5]
        })
        
        fig = px.pie(
            df_ecommerce,
            values='Porcentaje',
            names='Categoría',
            color_discrete_sequence=['#2ca02c', '#d62728'],
            hole=0.5
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
    
    # Análisis por sector
    st.subheader("💻 Digitalización por Sector")
    df_digital = pd.DataFrame({
        'Sector': ['Servicios', 'Comercio', 'Manufactura', 'Construcción'],
        'Conectividad (%)': [62.5, 45.2, 38.7, 22.1],
        'E-commerce (%)': [12.3, 9.8, 5.2, 2.1]
    })
    
    fig = go.Figure()
    fig.add_trace(go.Bar(name='Conectividad', x=df_digital['Sector'], y=df_digital['Conectividad (%)'], marker_color='#1f77b4'))
    fig.add_trace(go.Bar(name='E-commerce', x=df_digital['Sector'], y=df_digital['E-commerce (%)'], marker_color='#ff7f0e'))
    fig.update_layout(barmode='group', height=400, yaxis_title="Porcentaje (%)")
    st.plotly_chart(fig, use_container_width=True)
    
    # Descarga
    crear_boton_descarga_csv(df_digital, "digitalizacion_bc", "📥 Descargar datos digitales")

# ===============================================
# TAB 7: GÉNERO & FINANCIAMIENTO
# ===============================================

with tabs[6]:
    st.header("👥 Equidad de Género y Financiamiento")
    
    st.info("💡 **Participación femenina**: 41.3% de establecimientos en BC están dirigidos por mujeres, por encima del promedio nacional")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("👩‍💼 Participación por Género")
        df_genero = pd.DataFrame({
            'Género': ['Mujeres', 'Hombres'],
            'Porcentaje': [DATOS_BC['mujeres'], 100 - DATOS_BC['mujeres']]
        })
        
        fig = px.pie(
            df_genero,
            values='Porcentaje',
            names='Género',
            color_discrete_sequence=['#ff69b4', '#4682b4'],
            hole=0.4
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("💰 Acceso a Financiamiento")
        df_credito = pd.DataFrame({
            'Fuente': ['Banca comercial', 'SOFOM/SOFINCO', 'Familia/Amigos', 'Sin crédito'],
            'Porcentaje': [18.5, 12.3, 8.7, 60.5]
        })
        
        fig = px.bar(
            df_credito,
            x='Fuente',
            y='Porcentaje',
            text='Porcentaje',
            color='Fuente',
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig.update_traces(texttemplate='%{text}%', textposition='outside')
        fig.update_layout(showlegend=False, height=400, yaxis_title="% de Establecimientos")
        st.plotly_chart(fig, use_container_width=True)
    
    # Género por sector
    st.subheader("👩‍💼 Mujeres Empresarias por Sector")
    df_genero_sector = pd.DataFrame({
        'Sector': ['Comercio', 'Servicios', 'Manufactura', 'Construcción'],
        'Mujeres (%)': [45.2, 42.8, 28.5, 12.3],
        'Hombres (%)': [54.8, 57.2, 71.5, 87.7]
    })
    
    fig = go.Figure()
    fig.add_trace(go.Bar(name='Mujeres', x=df_genero_sector['Sector'], y=df_genero_sector['Mujeres (%)'], marker_color='#ff69b4'))
    fig.add_trace(go.Bar(name='Hombres', x=df_genero_sector['Sector'], y=df_genero_sector['Hombres (%)'], marker_color='#4682b4'))
    
    fig = agregar_linea_referencia(fig, DATOS_BC['mujeres'], f"Promedio BC: {DATOS_BC['mujeres']}%", "#ff1493")
    
    fig.update_layout(barmode='stack', height=400, yaxis_title="Porcentaje (%)")
    st.plotly_chart(fig, use_container_width=True)
    
    # Descarga
    crear_boton_descarga_csv(df_genero_sector, "genero_bc", "📥 Descargar datos de género")

# ===============================================
# FOOTER
# ===============================================

st.markdown("---")
st.markdown(
    f"""
    <div style='text-align: center; color: gray;'>
        <p>📊 Dashboard DENUE Baja California | Última actualización: {datetime.now().strftime('%d/%m/%Y %H:%M')}</p>
        <p>Fuente: INEGI - DENUE 2024 | Secretaría de Economía e Innovación BC</p>
        <p>Token API: {'Activo ✅' if test_api else 'Offline ⚠️'}</p>
    </div>
    """,
    unsafe_allow_html=True
)
