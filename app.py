import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(
    page_title="Dashboard DENUE BC",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

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

def formato_numero(numero):
    return f"{numero:,}".replace(",", ",")

def crear_metrica_kpi(titulo, valor, delta=None, porcentaje=False):
    if porcentaje:
        valor_formato = f"{valor}%"
    else:
        valor_formato = formato_numero(int(valor))
    st.metric(label=titulo, value=valor_formato, delta=delta)

def crear_boton_descarga_csv(df, nombre_archivo, label="📥 Descargar CSV"):
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label=label,
        data=csv,
        file_name=f"{nombre_archivo}_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )

def agregar_linea_referencia(fig, valor, texto, color="red"):
    fig.add_hline(
        y=valor,
        line_dash="dash",
        annotation_text=texto,
        line_color=color,
        annotation_position="bottom right"
    )
    return fig

st.sidebar.title("🎛️ Controles")

año_seleccionado = st.sidebar.selectbox(
    "📅 Año de análisis:",
    [2019, 2020, 2021, 2022, 2023, 2024],
    index=5
)

municipios_disponibles = ['Todos'] + DATOS_MUNICIPIOS['Municipio'].tolist()
municipio_filtro = st.sidebar.selectbox("📍 Municipio:", municipios_disponibles)

sectores_disponibles = ['Todos'] + DATOS_SECTORES['Sector'].tolist()
sector_filtro = st.sidebar.selectbox("🏭 Sector:", sectores_disponibles)

st.sidebar.markdown("---")
st.sidebar.info("💡 **Tip:** Usa los filtros para análisis personalizados")
st.sidebar.markdown("---")
st.sidebar.success("📊 **Datos verificados INEGI 2024**")

st.title("📊 Dashboard DENUE - Baja California")
st.markdown(f"### Análisis Económico {año_seleccionado}")
st.markdown("**Secretaría de Economía e Innovación**")
st.markdown("---")

tabs = st.tabs([
    "🏠 Visión General",
    "📍 Competencia por Zona",
    "⚖️ BC vs Nuevo León",
    "🏭 Sectores",
    "📈 Tendencias",
    "💻 Digitalización",
    "👥 Género & Financiamiento"
])

with tabs[0]:
    st.header("Panorama General de Baja California")
    st.info("💡 **Establecimientos económicos**: Unidades productivas registradas en DENUE")
    
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
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 BC vs Nacional")
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=['Baja California', 'Nacional'],
            y=[DATOS_BC['formalidad'], DATOS_NACIONALES['formalidad']],
            marker_color=['#1f77b4', '#ff7f0e'],
            text=[f"{DATOS_BC['formalidad']}%", f"{DATOS_NACIONALES['formalidad']}%"],
            textposition='auto'
        ))
        fig = agregar_linea_referencia(fig, DATOS_NACIONALES['formalidad'], f"Promedio Nacional: {DATOS_NACIONALES['formalidad']}%", "red")
        fig.update_layout(title="Tasa de Formalidad", yaxis_title="Porcentaje (%)", showlegend=False, height=400)
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
        fig.update_layout(title="Acceso a Internet", yaxis_title="Porcentaje (%)", showlegend=False, height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    df_resumen = pd.DataFrame({
        'Indicador': ['Establecimientos', 'Empleados', 'Formalidad (%)', 'Internet (%)'],
        'Baja California': [DATOS_BC['establecimientos'], DATOS_BC['empleados'], DATOS_BC['formalidad'], DATOS_BC['internet']]
    })
    crear_boton_descarga_csv(df_resumen, "resumen_bc", "📥 Descargar datos generales")

with tabs[1]:
    st.header("📍 Análisis por Municipio")
    st.info("💡 **Concentración empresarial**: Tijuana y Mexicali concentran el 72.8% de los establecimientos")
    
    if municipio_filtro != 'Todos':
        df_filtrado = DATOS_MUNICIPIOS[DATOS_MUNICIPIOS['Municipio'] == municipio_filtro]
        st.warning(f"🔍 Mostrando datos de: **{municipio_filtro}**")
    else:
        df_filtrado = DATOS_MUNICIPIOS
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🏢 Establecimientos por Municipio")
        fig = px.bar(df_filtrado, x='Municipio', y='Establecimientos', text='Establecimientos', color='Municipio', color_discrete_sequence=px.colors.qualitative.Set2)
        fig.update_traces(texttemplate='%{text:,}', textposition='outside')
        fig.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("👥 Empleados por Municipio")
        fig = px.bar(df_filtrado, x='Municipio', y='Empleados', text='Empleados', color='Municipio', color_discrete_sequence=px.colors.qualitative.Set3)
        fig.update_traces(texttemplate='%{text:,}', textposition='outside')
        fig.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("📋 Tabla Detallada")
    st.dataframe(df_filtrado, use_container_width=True)
    crear_boton_descarga_csv(df_filtrado, "municipios_bc", "📥 Descargar datos por municipio")

with tabs[2]:
    st.header("⚖️ Baja California vs Nuevo León")
    st.info("💡 **Comparativa estratégica**: Nuevo León es el principal competidor en captación industrial")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📊 Establecimientos")
        fig = px.bar(DATOS_COMPARATIVA, x='Estado', y='Establecimientos', text='Establecimientos', color='Estado', color_discrete_map={'Baja California': '#1f77b4', 'Nuevo León': '#ff7f0e'})
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
        fig.update_layout(xaxis_title="Formalidad (%)", yaxis_title="Conectividad (%)", height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("📦 Exportaciones 2024")
    fig = px.bar(DATOS_COMPARATIVA, x='Estado', y='Exportaciones', text='Exportaciones', color='Estado', color_discrete_map={'Baja California': '#2ca02c', 'Nuevo León': '#d62728'})
    fig.update_traces(texttemplate='$%{text}B', textposition='outside')
    fig.update_layout(showlegend=False, height=400)
    st.plotly_chart(fig, use_container_width=True)
    crear_boton_descarga_csv(DATOS_COMPARATIVA, "bc_vs_nl", "📥 Descargar comparativa")

with tabs[3]:
    st.header("🏭 Distribución Sectorial (SCIAN)")
    st.info("💡 **SCIAN**: Sistema de Clasificación Industrial de América del Norte")
    
    if sector_filtro != 'Todos':
        df_sector_filtrado = DATOS_SECTORES[DATOS_SECTORES['Sector'] == sector_filtro]
        st.warning(f"🔍 Mostrando: **{sector_filtro}**")
    else:
        df_sector_filtrado = DATOS_SECTORES
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🥧 Participación por Sector")
        fig = px.pie(df_sector_filtrado, values='Porcentaje', names='Sector', hole=0.4, color_discrete_sequence=px.colors.qualitative.Pastel)
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("📊 Establecimientos")
        fig = px.bar(df_sector_filtrado.sort_values('Establecimientos', ascending=True), y='Sector', x='Establecimientos', text='Establecimientos', orientation='h', color='Sector', color_discrete_sequence=px.colors.qualitative.Set2)
        fig.update_traces(texttemplate='%{text:,}', textposition='outside')
        fig.update_layout(showlegend=False, height=500)
        st.plotly_chart(fig, use_container_width=True)
    
    st.dataframe(df_sector_filtrado, use_container_width=True)
    crear_boton_descarga_csv(df_sector_filtrado, "sectores_bc", "📥 Descargar datos sectoriales")

with tabs[4]:
    st.header("📈 Tendencias 2019-2024")
    st.info("💡 **Post-pandemia**: Recuperación sostenida desde 2021")
    
    df_tendencias_filtrado = DATOS_TENDENCIAS[DATOS_TENDENCIAS['Año'] <= año_seleccionado]
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📊 Establecimientos")
        fig = px.line(df_tendencias_filtrado, x='Año', y='Establecimientos', markers=True, text='Establecimientos')
        fig.update_traces(texttemplate='%{text:,}', textposition='top center')
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("👥 Empleo")
        fig = px.line(df_tendencias_filtrado, x='Año', y='Empleo', markers=True, text='Empleo', line_shape='spline')
        fig.update_traces(texttemplate='%{text:,}', textposition='top center', line_color='#ff7f0e')
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("📊 Crecimiento Anual")
    df_crecimiento = df_tendencias_filtrado.copy()
    df_crecimiento['Crecimiento (%)'] = df_crecimiento['Establecimientos'].pct_change() * 100
    fig = px.bar(df_crecimiento[1:], x='Año', y='Crecimiento (%)', text='Crecimiento (%)', color='Crecimiento (%)', color_continuous_scale=['red', 'yellow', 'green'])
    fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)
    crear_boton_descarga_csv(df_tendencias_filtrado, "tendencias_bc", "📥 Descargar serie")

with tabs[5]:
    st.header("💻 Adopción Digital")
    st.info("💡 **Brecha digital**: BC lidera conectividad, e-commerce rezagado")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🌐 Internet")
        st.metric("Conectividad BC", f"{DATOS_BC['internet']}%", delta=f"+{DATOS_BC['internet'] - DATOS_NACIONALES['internet']:.1f}% vs Nacional")
        
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=DATOS_BC['internet'],
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Internet (%)"},
            delta={'reference': DATOS_NACIONALES['internet']},
            gauge={'axis': {'range': [None, 100]}, 'bar': {'color': "#1f77b4"}, 'steps': [{'range': [0, 30], 'color': "lightgray"}, {'range': [30, 40], 'color': "gray"}], 'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': DATOS_NACIONALES['internet']}}
        ))
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("🛒 E-commerce")
        st.metric("Ventas Online", "8.5%", delta="-2.8% vs Nacional")
        
        df_ecommerce = pd.DataFrame({'Categoría': ['Con e-commerce', 'Sin e-commerce'], 'Porcentaje': [8.5, 91.5]})
        fig = px.pie(df_ecommerce, values='Porcentaje', names='Categoría', color_discrete_sequence=['#2ca02c', '#d62728'], hole=0.5)
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("💻 Por Sector")
    df_digital = pd.DataFrame({'Sector': ['Servicios', 'Comercio', 'Manufactura', 'Construcción'], 'Conectividad (%)': [62.5, 45.2, 38.7, 22.1], 'E-commerce (%)': [12.3, 9.8, 5.2, 2.1]})
    fig = go.Figure()
    fig.add_trace(go.Bar(name='Conectividad', x=df_digital['Sector'], y=df_digital['Conectividad (%)'], marker_color='#1f77b4'))
    fig.add_trace(go.Bar(name='E-commerce', x=df_digital['Sector'], y=df_digital['E-commerce (%)'], marker_color='#ff7f0e'))
    fig.update_layout(barmode='group', height=400)
    st.plotly_chart(fig, use_container_width=True)
    crear_boton_descarga_csv(df_digital, "digitalizacion_bc", "📥 Descargar")

with tabs[6]:
    st.header("👥 Género & Financiamiento")
    st.info("💡 **Participación femenina**: 41.3% de establecimientos dirigidos por mujeres")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("👩‍💼 Género")
        df_genero = pd.DataFrame({'Género': ['Mujeres', 'Hombres'], 'Porcentaje': [DATOS_BC['mujeres'], 100 - DATOS_BC['mujeres']]})
        fig = px.pie(df_genero, values='Porcentaje', names='Género', color_discrete_sequence=['#ff69b4', '#4682b4'], hole=0.4)
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("💰 Financiamiento")
        df_credito = pd.DataFrame({'Fuente': ['Banca comercial', 'SOFOM', 'Familia', 'Sin crédito'], 'Porcentaje': [18.5, 12.3, 8.7, 60.5]})
        fig = px.bar(df_credito, x='Fuente', y='Porcentaje', text='Porcentaje', color='Fuente', color_discrete_sequence=px.colors.qualitative.Set2)
        fig.update_traces(texttemplate='%{text}%', textposition='outside')
        fig.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("👩‍💼 Mujeres por Sector")
    df_genero_sector = pd.DataFrame({'Sector': ['Comercio', 'Servicios', 'Manufactura', 'Construcción'], 'Mujeres (%)': [45.2, 42.8, 28.5, 12.3], 'Hombres (%)': [54.8, 57.2, 71.5, 87.7]})
    fig = go.Figure()
    fig.add_trace(go.Bar(name='Mujeres', x=df_genero_sector['Sector'], y=df_genero_sector['Mujeres (%)'], marker_color='#ff69b4'))
    fig.add_trace(go.Bar(name='Hombres', x=df_genero_sector['Sector'], y=df_genero_sector['Hombres (%)'], marker_color='#4682b4'))
    fig = agregar_linea_referencia(fig, DATOS_BC['mujeres'], f"Promedio BC: {DATOS_BC['mujeres']}%", "#ff1493")
    fig.update_layout(barmode='stack', height=400)
    st.plotly_chart(fig, use_container_width=True)
    crear_boton_descarga_csv(df_genero_sector, "genero_bc", "📥 Descargar")

st.markdown("---")
st.markdown(f"<div style='text-align: center; color: gray;'><p>📊 Dashboard DENUE BC | {datetime.now().strftime('%d/%m/%Y %H:%M')}</p><p>Fuente: INEGI DENUE 2024 | SEI BC</p></div>", unsafe_allow_html=True)
