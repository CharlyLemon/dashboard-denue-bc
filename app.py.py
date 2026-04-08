import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# CONFIGURACIÓN (DEBE SER PRIMERO)
st.set_page_config(
    page_title="Dashboard DENUE - Baja California",
    page_icon="📊",
    layout="wide"
)

# DATOS INEGI 2024
DATOS_BC = {
    'establecimientos': 41237,
    'empleados': 330000,
    'informalidad': 37.7,
    'formalidad': 62.3,
    'mujeres': 41.3,
    'internet': 45.1,
    'exportaciones': 60558,
}

DATOS_NACIONAL = {
    'establecimientos': 5500000,
    'empleados': 27900000,
    'informalidad': 52.1,
    'formalidad': 47.9,
    'mujeres': 43.2,
    'internet': 26.2,
}

# HEADER
st.markdown("""
<div style='text-align: center; margin-bottom: 30px;'>
    <h1>📊 Dashboard DENUE - Baja California</h1>
    <p style='color: #666;'>Análisis de establecimientos empresariales | INEGI 2024</p>
</div>
""", unsafe_allow_html=True)

# KPI CARDS
col1, col2, col3, col4, col5, col6 = st.columns(6)
col1.metric("Establecimientos", "41,237", "+10.8%")
col2.metric("Empleo", "330K", "+8.2%")
col3.metric("Formalidad", "62.3%", "2º lugar")
col4.metric("Internet", "45.1%", "Líder")
col5.metric("Mujeres", "41.3%", "ocupadas")
col6.metric("Exportaciones", "US$60.6B", "2024")

st.divider()

# SIDEBAR
st.sidebar.markdown("### 🎛️ SECCIONES")
seccion = st.sidebar.radio(
    "Selecciona:",
    ["Visión General", "Competencia por Zona", "BC vs NL", "Sectores", 
     "Tendencias", "Digitalización", "Género & Financiamiento"],
    label_visibility="collapsed"
)

municipio = st.sidebar.selectbox(
    "Municipio:",
    ["Tijuana", "Mexicali", "Ensenada", "Tecate", "Rosarito"]
)

# CONTENIDO
if seccion == "Visión General":
    st.markdown("## Visión General BC 2024")
    
    col1, col2 = st.columns(2)
    
    with col1:
        df = pd.DataFrame({
            'Métrica': ['Establecimientos', 'Empleo', 'Formalidad %', 'Internet %'],
            'BC': [41.2, 330, 62.3, 45.1],
            'Nacional': [5500, 27900, 47.9, 26.2]
        })
        
        fig = px.bar(df, x='Métrica', y=['BC', 'Nacional'], barmode='group',
                     color_discrete_map={'BC': '#3498db', 'Nacional': '#95a5a6'})
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        df_pie = pd.DataFrame({
            'Estado': ['Formal', 'Informal'],
            'Porcentaje': [62.3, 37.7]
        })
        fig = px.pie(df_pie, values='Porcentaje', names='Estado',
                     color_discrete_map={'Formal': '#27ae60', 'Informal': '#e74c3c'})
        st.plotly_chart(fig, use_container_width=True)
    
    st.info("✅ BC destaca por formalidad (62.3% vs 47.9% nacional) y liderazgo digital")

elif seccion == "Competencia por Zona":
    st.markdown("## Análisis por Zona Geográfica")
    
    df_mun = pd.DataFrame({
        'Municipio': ['Tijuana', 'Mexicali', 'Ensenada', 'Tecate', 'Rosarito'],
        'Establecimientos': [18500, 12300, 4200, 3100, 3137],
        'Empleo': [185000, 95000, 28000, 15000, 7000],
        'Densidad': [95, 72, 45, 28, 35]
    })
    
    mun_sel = df_mun[df_mun['Municipio'] == municipio].iloc[0]
    col1, col2, col3 = st.columns(3)
    col1.metric("Establecimientos", f"{mun_sel['Establecimientos']:,}")
    col2.metric("Empleo", f"{mun_sel['Empleo']:,}")
    col3.metric("Densidad", f"{mun_sel['Densidad']:.0f}/100")
    
    col1, col2 = st.columns(2)
    with col1:
        fig = px.bar(df_mun, x='Municipio', y='Establecimientos',
                     color='Densidad', color_continuous_scale='Reds',
                     title="Establecimientos")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.bar(df_mun, x='Municipio', y='Densidad',
                     color='Densidad', color_continuous_scale='RdYlGn_r',
                     title="Densidad Empresarial")
        st.plotly_chart(fig, use_container_width=True)

elif seccion == "BC vs NL":
    st.markdown("## Baja California vs Nuevo León")
    
    df_comp = pd.DataFrame({
        'Métrica': ['Establecimientos', 'Crecimiento %', 'Formalidad %', 'Internet %'],
        'BC': [41237, 10.8, 62.3, 45.1],
        'NL': [212676, 16.0, 55.0, 38.0]
    })
    
    fig = px.bar(df_comp, x='Métrica', y=['BC', 'NL'], barmode='group',
                 color_discrete_map={'BC': '#3498db', 'NL': '#27ae60'})
    st.plotly_chart(fig, use_container_width=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.success("""
        **✅ Ventajas BC:**
        - Mayor formalidad: 62.3% vs 55%
        - Líder digital: 45.1% internet
        - Menor pobreza laboral: 20.1%
        """)
    with col2:
        st.info("""
        **✅ Ventajas NL:**
        - 5x más establecimientos
        - Crecimiento: 16% vs 10.8%
        - Ecosistema nearshoring
        """)

elif seccion == "Sectores":
    st.markdown("## Sectores Económicos")
    
    df_sect = pd.DataFrame({
        'Sector': ['Comercio', 'Comida/Bebida', 'Manufactura', 'Construcción',
                   'Transporte', 'Servicios Prof.', 'Turismo', 'Otros'],
        'Establecimientos': [10680, 6200, 2150, 1800, 1500, 3400, 1200, 14307],
        'Valor': [12, 8, 45, 18, 20, 25, 10, 15]
    })
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.bar(df_sect.sort_values('Establecimientos'), y='Sector',
                     x='Establecimientos', orientation='h',
                     color='Establecimientos', color_continuous_scale='Blues',
                     title="Establecimientos")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.pie(df_sect, values='Valor', names='Sector',
                     title="Valor Agregado %")
        st.plotly_chart(fig, use_container_width=True)
    
    st.warning("💡 Manufactura: 2.4% establecimientos, 45% valor agregado")

elif seccion == "Tendencias":
    st.markdown("## Tendencias 2019-2024")
    
    df_tend = pd.DataFrame({
        'Año': [2019, 2020, 2021, 2022, 2023, 2024],
        'Establecimientos': [37200, 36800, 38200, 39500, 40300, 41237],
        'Informalidad': [42.0, 44.0, 41.0, 39.0, 38.0, 37.7]
    })
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.line(df_tend, x='Año', y='Establecimientos', markers=True,
                      title="Crecimiento", color_discrete_sequence=['#3498db'])
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.line(df_tend, x='Año', y='Informalidad', markers=True,
                      title="Informalidad %", color_discrete_sequence=['#e74c3c'])
        st.plotly_chart(fig, use_container_width=True)
    
    st.success("✅ +10.8% establecimientos | -4.3pp informalidad")

elif seccion == "Digitalización":
    st.markdown("## Transformación Digital")
    
    df_dig = pd.DataFrame({
        'Estado': ['BC', 'NL', 'Jalisco', 'CDMX', 'Nacional'],
        'Internet': [45.1, 38.0, 32.0, 35.0, 26.2],
        'Computadora': [42.0, 35.0, 30.0, 38.0, 25.3]
    })
    
    fig = px.bar(df_dig, x='Estado', y=['Internet', 'Computadora'],
                 barmode='group', color_discrete_map={'Internet': '#3498db', 'Computadora': '#95a5a6'},
                 title="Adopción de Tecnología")
    st.plotly_chart(fig, use_container_width=True)
    
    st.info("💡 BC lidera Internet (45.1%) - Oportunidad en e-commerce")

elif seccion == "Género & Financiamiento":
    st.markdown("## Género y Acceso a Financiamiento")
    
    df_muj = pd.DataFrame({
        'Sector': ['Comercio', 'Servicios', 'Profesionales', 'Manufactura', 'Construcción'],
        'Participación': [48, 44, 46, 32, 18]
    })
    
    df_fin = pd.DataFrame({
        'Estado': ['BC', 'NL', 'Jalisco', 'EDOMEX', 'Nacional'],
        'Acceso': [48, 52, 46, 42, 45.9],
        'Rechazo': [12, 10, 14, 15, 13.1]
    })
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.bar(df_muj.sort_values('Participación'), y='Sector',
                     x='Participación', orientation='h', color='Participación',
                     color_continuous_scale='Reds', title="Mujeres por Sector %")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.bar(df_fin, x='Estado', y=['Acceso', 'Rechazo'],
                     barmode='group', color_discrete_map={'Acceso': '#27ae60', 'Rechazo': '#e74c3c'},
                     title="Acceso vs Rechazo Crediticio")
        st.plotly_chart(fig, use_container_width=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.info("**👩‍💼 Participación: 41.3%**\nMeta: 45% en 5 años")
    with col2:
        st.success("**💰 Acceso: 48%**\nMejor que nacional 45.9%")

# FOOTER
st.divider()
st.markdown("""
<div style='text-align: center; color: #999; font-size: 11px; padding: 20px;'>
    Dashboard DENUE - Baja California | INEGI Censos Económicos 2024 | Secretaría de Economía e Innovación
</div>
""", unsafe_allow_html=True)
