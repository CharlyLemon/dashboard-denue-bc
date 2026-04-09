# 📊 Dashboard DENUE - Baja California

Dashboard analítico para la Secretaría de Economía e Innovación (SEI) de Baja California con datos del Directorio Estadístico Nacional de Unidades Económicas (DENUE) 2024.

## 🎯 Características

- **138,604 establecimientos** activos en BC (dato oficial INEGI 2024)
- Análisis por municipio (Tijuana, Mexicali, Ensenada, Tecate, Rosarito)
- Comparativa BC vs Nacional y BC vs Nuevo León
- Distribución sectorial SCIAN
- Indicadores de digitalización, género y financiamiento
- Series temporales 2019-2024

## 🚀 Deployment en Streamlit Cloud

### Paso 1: Estructura de archivos en GitHub
```
dashboard-denue-bc/
├── app.py
├── requirements.txt
├── runtime.txt (NUEVO)
├── .streamlit/
│   └── config.toml
└── README.md
```

### Paso 2: Crear carpeta .streamlit en GitHub

**IMPORTANTE:** GitHub no permite crear carpetas vacías directamente.

1. Ve a tu repositorio: https://github.com/CharlyLemon/dashboard-denue-bc
2. Click en **"Add file"** → **"Create new file"**
3. En el campo de nombre escribe: `.streamlit/config.toml`
   - GitHub creará automáticamente la carpeta `.streamlit/`
4. Pega el contenido del archivo `config.toml` proporcionado
5. Commit changes

### Paso 3: Subir archivos nuevos

Sube estos archivos en la raíz del repositorio:
- ✅ `requirements.txt` (versión OPTIMIZADA)
- ✅ `runtime.txt` (NUEVO - especifica Python 3.11.7)

### Paso 4: Forzar re-deploy en Streamlit Cloud

1. Ve a https://share.streamlit.io/
2. Encuentra tu app: `dashboard-denue-bc`
3. Click en **⋮** (menú) → **"Reboot app"**
4. Si persiste error, click en **"Delete app"** y vuélvela a crear desde cero

### Paso 5: Verificar logs

Si hay error:
1. En Streamlit Cloud, click en **"Manage app"**
2. Ve a la pestaña **"Logs"**
3. Busca líneas que digan `ERROR` o `FAILED`
4. Copia el mensaje completo y compártelo para diagnosticar

## 📊 Datos Utilizados

Todos los datos están verificados contra fuentes oficiales INEGI 2024:

- **DENUE Interactivo 2024** - Número de establecimientos
- **Censos Económicos 2024** - Distribución sectorial
- **EDN 2023** - Demografía de negocios
- **PIBEF 2023** - PIB por entidad

## 🔧 Desarrollo Local

Para correr el dashboard en tu computadora:

```bash
# Clonar repositorio
git clone https://github.com/CharlyLemon/dashboard-denue-bc.git
cd dashboard-denue-bc

# Instalar dependencias
pip install -r requirements.txt

# Correr app
streamlit run app.py
```

La app se abrirá en http://localhost:8501

## 📝 Notas Técnicas

- **Python:** 3.11.7 (especificado en runtime.txt)
- **Streamlit:** 1.32.2
- **Pandas:** 2.2.1
- **Plotly:** 5.20.0

## 📫 Contacto

Secretaría de Economía e Innovación - Baja California

---

**Última actualización:** Abril 2026
