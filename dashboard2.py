import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from streamlit_option_menu import option_menu
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image
import os
from pathlib import Path
import json
import requests
from io import BytesIO
from sklearn.linear_model import LinearRegression

# -*- coding: utf-8 -*-

# Page configuration
st.set_page_config(
    page_title="Dashboard Proyectos IA Sanitarios",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Color definitions - Blue and white palette
COLOR_AZUL_PRINCIPAL = "#0D47A1"  # Dark blue
COLOR_AZUL_SECUNDARIO = "#1976D2"  # Medium blue
COLOR_AZUL_CLARO = "#64B5F6"  # Light blue
COLOR_FONDO = "#F5F9FF"  # Bluish white for background
COLOR_TEXTO = "#0A1F44"  # Dark blue for text

COLOR_ACENTO = "#FF9800"  # Orange as accent color

# Complete palette for graphs
COLOR_PALETA = ["#0D47A1", "#1976D2", "#2196F3", "#64B5F6", "#90CAF9", "#BBDEFB", 
                "#E3F2FD", "#1565C0", "#0277BD", "#01579B"]

# Apply custom styles
st.markdown(f"""
<style>
    /* General styles */
    .reportview-container {{
        background-color: {COLOR_FONDO};
    }}
    .main {{
        background-color: {COLOR_FONDO};
    }}
    
    /* Headers and titles */
    .main-header {{
        font-size: 2.5rem;
        color: {COLOR_AZUL_PRINCIPAL};
        font-weight: bold;
        margin-bottom: 1rem;
        font-family: 'Helvetica', sans-serif;
    }}
    .sub-header {{
        font-size: 1.5rem;
        color: {COLOR_AZUL_SECUNDARIO};
        font-weight: 600;
        margin-bottom: 1rem;
        font-family: 'Helvetica', sans-serif;
    }}
    
    /* Cards for metrics and KPIs */
    .card {{
        background-color: white;
        border-radius: 8px;
        padding: 20px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05);
        border-left: 4px solid {COLOR_AZUL_PRINCIPAL};
        margin-bottom: 1rem;
    }}
    .metric-value {{
        font-size: 2.2rem;
        font-weight: bold;
        color: {COLOR_AZUL_PRINCIPAL};
        margin-bottom: 0.3rem;
        font-family: 'Helvetica', sans-serif;
    }}
    .metric-label {{
        font-size: 1rem;
        color: {COLOR_TEXTO};
        font-family: 'Helvetica', sans-serif;
    }}
    
    /* Tabs and widgets */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 1px;
    }}
    .stTabs [data-baseweb="tab"] {{
        background-color: white;
        border-radius: 4px 4px 0px 0px;
        padding: 10px 20px;
        color: {COLOR_TEXTO};
    }}
    .stTabs [aria-selected="true"] {{
        background-color: {COLOR_AZUL_PRINCIPAL};
        color: white;
    }}
    
    /* Sidebar */
    .sidebar .sidebar-content {{
        background-color: white;
    }}
    
    /* Containers */
    div[data-testid="stVerticalBlock"] div[style] {{
        background-color: white;
        border-radius: 10px;
        padding: 10px;
        margin-bottom: 1rem;
    }}
    
    /* Dividers */
    hr {{
        border-top: 1px solid {COLOR_AZUL_CLARO};
        margin: 1.5rem 0;
    }}
    
    /* Selectboxes and filters */
    div[data-baseweb="select"] {{
        background-color: white;
        border-radius: 4px;
    }}
    
    /* Buttons */
    .stButton>button {{
        background-color: {COLOR_AZUL_PRINCIPAL};
        color: white;
        border-radius: 4px;
    }}
    .stButton>button:hover {{
        background-color: {COLOR_AZUL_SECUNDARIO};
    }}
    
    /* Animations */
    .card:hover {{
        transform: translateY(-5px);
        transition: transform 0.3s ease;
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
    }}
    
    /* Custom tooltip */
    .tooltip {{
        position: relative;
        display: inline-block;
    }}
    .tooltip .tooltiptext {{
        visibility: hidden;
        width: 120px;
        background-color: {COLOR_AZUL_PRINCIPAL};
        color: white;
        text-align: center;
        border-radius: 6px;
        padding: 5px;
        position: absolute;
        z-index: 1;
        bottom: 125%;
        left: 50%;
        margin-left: -60px;
        opacity: 0;
        transition: opacity 0.3s;
    }}
    .tooltip:hover .tooltiptext {{
        visibility: visible;
        opacity: 1;
    }}
    
    /* Accessibility improvements */
    a:focus, button:focus, [role="button"]:focus {{
        outline: 2px solid {COLOR_ACENTO};
        outline-offset: 2px;
    }}
    
    /* Badge for notifications or labels */
    .badge {{
        display: inline-block;
        padding: 4px 8px;
        font-size: 12px;
        font-weight: bold;
        line-height: 1;
        color: white;
        text-align: center;
        white-space: nowrap;
        vertical-align: baseline;
        border-radius: 10px;
        background-color: {COLOR_ACENTO};
    }}
    .badge-success {{
        background-color: #4CAF50;
    }}
    .badge-warning {{
        background-color: #FFC107;
    }}
    .badge-danger {{
        background-color: #F44336;
    }}
</style>
""", unsafe_allow_html=True)

# Define file paths with better compatibility
def get_project_paths():
    # Try different locations to find files
    possible_paths = [
        # Absolute path
        {"excel": r"C:\Users\lujan\Desktop\findemodulo1\Modulo SSII.xlsx", 
         "logo": r"C:\Users\lujan\Desktop\findemodulo1\Logotipo_del_Ministerio_de_Sanidad.svg.png"},
        # Relative path to current working directory
        {"excel": os.path.join(".", "Modulo SSII.xlsx"),
         "logo": os.path.join(".", "Logotipo_del_Ministerio_de_Sanidad.svg.png")},
        # Original paths
        {"excel": r"C:\Users\lujan\Desktop\Fin de modulo\TABLA SSII.xlsx",
         "logo": r"C:\Users\lujan\Desktop\Fin de modulo\Logotipo_del_Ministerio_de_Sanidad.svg.png"}
    ]
    
    for path_set in possible_paths:
        if os.path.exists(path_set["excel"]):
            return path_set
    
    # If not found, return original paths and handle error in loading function
    return possible_paths[0]

# Get paths
paths = get_project_paths()
EXCEL_PATH = paths["excel"]
LOGO_PATH = paths["logo"]

# Function to load and process Excel file
@st.cache_data
def load_data(file_path):
    try:
        # Load Excel file
        df = pd.read_excel(file_path)
        
        # Basic cleaning
        # Replace NaN with "No especificado"
        df = df.fillna("No especificado")
        
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

# Function to load logo image
def cargar_logo(logo_path):
    try:
        if os.path.exists(logo_path):
            return Image.open(logo_path)
        else:
            st.sidebar.warning(f"Logo not found at: {logo_path}")
            return None
    except Exception as e:
        st.sidebar.error(f"Error loading logo: {e}")
        return None

# Load data
def cargar_datos():
    try:
        # Check if file exists
        if os.path.exists(EXCEL_PATH):
            df = load_data(EXCEL_PATH)
            if df is not None:
                return df
            else:
                st.error("Error processing Excel file.")
                return crear_datos_ejemplo()
        else:
            # Show friendly error
            st.error(f"Excel file not found at: {EXCEL_PATH}")
            # Use example data if file not found
            return crear_datos_ejemplo()
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return crear_datos_ejemplo()

# Function to create example data if file not found
def crear_datos_ejemplo():
    # Create basic example DataFrame
    st.warning("Using example data because Excel file couldn't be loaded.")
    
    # List of autonomous communities
    comunidades_autonomas = [
        'Andalucía', 'Aragón', 'Asturias', 'Islas Baleares', 'Canarias', 
        'Cantabria', 'Castilla-La Mancha', 'Castilla y León', 'Cataluña', 
        'Comunidad Valenciana', 'Extremadura', 'Galicia', 'Comunidad de Madrid', 
        'Región de Murcia', 'Navarra', 'País Vasco', 'La Rioja'
    ]
    
    ambitos_aplicacion = [
        'Atención Primaria', 'Oncología', 'Cardiología', 'Radiología', 
        'Neurología', 'Urgencias', 'Traumatología', 'Pediatría', 
        'Neumología', 'Dermatología', 'Geriatría', 'Oftalmología', 
        'Ginecología', 'Psiquiatría', 'Farmacia Hospitalaria', 
        'Investigación sanitaria', 'Gestión hospitalaria', 'Investigación clínica',
        'Gestión de desastres'
    ]
    
    tecnologias_ia = [
        'Producto comercial', 'Desarrollo propio', 'Proyecto Investigación',
        'Machine Learning', 'Deep Learning', 'NLP', 'Computer Vision',
        'Redes Neuronales', 'Algoritmos predictivos', 'Sistemas de soporte a la decisión'
    ]
    
    estados_implementacion = [
        'En marcha', 'Planificado', 'En desarrollo', 'Piloto', 'Finalizado', 
        'Suspendido', 'Evaluación'
    ]
    
    clasificaciones_sanitarias = [
        'N/A', 'Clase I', 'Clase IIa', 'Clase IIb', 'Clase III'
    ]
    
    riesgos_ia = [
        'Alto riesgo', 'Riesgo limitado', 'Bajo riesgo', 'No especificado'
    ]
    
    fechas_inicio = pd.date_range(start='2020-01-01', end='2025-03-01', periods=25)
    
    # Create example data
    data = []
    for i in range(1, 155):  # Create 154 examples
        data.append({
            "ID_Caso": f"PROY-{i:03d}",
            "Nombre_Caso": f"Proyecto IA Sanitaria {i}",
            "Descripcion": f"Descripción del proyecto {i} de IA en el ámbito sanitario",
            "Ambito_Aplicacion": np.random.choice(ambitos_aplicacion),
            "Tecnologia_IA": np.random.choice(tecnologias_ia),
            "Comunidad_Autonoma": np.random.choice(comunidades_autonomas, p=[0.2, 0.05, 0.05, 0.03, 0.05, 0.03, 0.05, 0.05, 0.15, 0.05, 0.03, 0.05, 0.1, 0.03, 0.03, 0.05, 0.02]),
            "Institucion_Responsable": "Dirección General de Salud Digital",
            "Forma_implementacion": np.random.choice(["Producto comercial", "Desarrollo propio", "Híbrido"]),
            "Estado_Implementacion": np.random.choice(estados_implementacion),
            "Fecha_Inicio": np.random.choice(fechas_inicio).strftime('%Y-%m-%d'),
            "Riesgo_IA": np.random.choice(riesgos_ia, p=[0.4, 0.3, 0.2, 0.1]),
            "Clasificacion_Sanitario": np.random.choice(clasificaciones_sanitarias),
            "Presupuesto": np.random.randint(50000, 1000000),
            "Numero_Usuarios": np.random.randint(10, 5000)
        })
    
    return pd.DataFrame(data)

# Function to load Spain's GeoJSON
@st.cache_data
def cargar_geojson_espana():
    try:
        # URL of GeoJSON for autonomous communities of Spain
        url = "https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/spain-communities.geojson"
        response = requests.get(url)
        
        # If download is successful, return GeoJSON
        if response.status_code == 200:
            return json.loads(response.content)
        else:
            st.error(f"Error loading map: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Error loading map: {e}")
        return None

# Function to normalize community names - Versión mejorada
def normalizar_nombre_ccaa(nombre):
    """
    Función mejorada para normalizar los nombres de las Comunidades Autónomas
    y asegurar que coinciden con los utilizados en el GeoJSON.
    """
    # Si el nombre es None o vacío, devolver un valor predeterminado
    if nombre is None or nombre == "":
        return "No especificada"
        
    # Mapeo ampliado de nombres que pueden variar
    mapeo_nombres = {
        # Andalucía
        "Andalucia": "Andalucía",
        "Andalucía": "Andalucía",
        
        # Aragón
        "Aragon": "Aragón",
        "Aragón": "Aragón",
        
        # Asturias
        "Asturias": "Asturias",
        "Principado de Asturias": "Asturias",
        
        # Baleares - Cambiado para coincidir con GeoJSON
        "Islas Baleares": "Baleares",
        "Baleares": "Baleares",
        "Illes Balears": "Baleares",
        
        # Canarias
        "Canarias": "Canarias",
        "Islas Canarias": "Canarias",
        
        # Cantabria
        "Cantabria": "Cantabria",
        
        # Castilla-La Mancha
        "Castilla-La Mancha": "Castilla-La Mancha",
        "Castilla La Mancha": "Castilla-La Mancha",
        
        # Castilla y León
        "Castilla y Leon": "Castilla y León",
        "Castilla y León": "Castilla y León",
        
        # Cataluña
        "Cataluna": "Cataluña",
        "Catalunya": "Cataluña",
        "Cataluña": "Cataluña",
        
        # Comunidad Valenciana
        "Comunidad Valenciana": "Comunidad Valenciana",
        "C. Valenciana": "Comunidad Valenciana",
        "Valencia": "Comunidad Valenciana",
        "Comunitat Valenciana": "Comunidad Valenciana",
        
        # Extremadura
        "Extremadura": "Extremadura",
        
        # Galicia
        "Galicia": "Galicia",
        
        # Madrid - Cambiado para coincidir con GeoJSON
        "Comunidad de Madrid": "Madrid",
        "Madrid": "Madrid",
        
        # Murcia - Cambiado para coincidir con GeoJSON
        "Region de Murcia": "Murcia",
        "Región de Murcia": "Murcia",
        "Murcia": "Murcia",
        
        # Navarra
        "Navarra": "Navarra",
        "Comunidad Foral de Navarra": "Navarra",
        
        # País Vasco
        "Pais Vasco": "País Vasco",
        "País Vasco": "País Vasco",
        "Euskadi": "País Vasco",
        
        # La Rioja
        "La Rioja": "La Rioja",
        "Rioja": "La Rioja",
        
        # Ciudades autónomas
        "Ceuta": "Ceuta",
        "Melilla": "Melilla"
    }
    
    # Verificar si el nombre original está en el mapeo
    nombre_normalizado = mapeo_nombres.get(nombre, nombre)
    
    # Verificar si el nombre normalizado existe en el esperado GeoJSON
    # Esto es una comprobación adicional para detectar problemas
    nombres_esperados_geojson = [
        "Andalucía", "Aragón", "Asturias", "Baleares", "Canarias",
        "Cantabria", "Castilla-La Mancha", "Castilla y León", "Cataluña",
        "Comunidad Valenciana", "Extremadura", "Galicia", "La Rioja",
        "Madrid", "Murcia", "Navarra", "País Vasco", "Ceuta", "Melilla"
    ]
    
    if nombre_normalizado not in nombres_esperados_geojson:
        # Intenta encontrar una coincidencia parcial
        for esperado in nombres_esperados_geojson:
            if nombre_normalizado.lower() in esperado.lower() or esperado.lower() in nombre_normalizado.lower():
                return esperado
    
    return nombre_normalizado

# Función para verificar coincidencias con GeoJSON
def verificar_coincidencias_geojson(df, geojson):
    """
    Función para verificar si los nombres de las CCAA en el DataFrame
    coinciden con los nombres en el GeoJSON, e imprimir advertencias si hay discrepancias.
    """
    if geojson is None:
        return
    
    # Obtener los nombres de las comunidades en el GeoJSON
    nombres_geojson = [feature['properties']['name'] for feature in geojson['features']]
    
    # Obtener los nombres normalizados en el DataFrame
    nombres_df = df['Comunidad_Normalizada'].unique()
    
    # Verificar coincidencias
    no_coincidentes = [nombre for nombre in nombres_df if nombre not in nombres_geojson]
    
    if no_coincidentes:
        st.warning(f"Algunas comunidades autónomas no coinciden con el GeoJSON: {', '.join(no_coincidentes)}")
        st.info("Esto puede causar que algunas comunidades no aparezcan en el mapa. Verifica la función de normalización.")

# Función para encontrar el equivalente en el GeoJSON
def encontrar_equivalente_geojson(nombre, nombres_geojson):
    """
    Encuentra el nombre equivalente en el GeoJSON para un nombre normalizado.
    """
    # 1. Verificar coincidencia exacta
    if nombre in nombres_geojson:
        return nombre
    
    # 2. Mapeos conocidos específicos
    mapeos_conocidos = {
        "Comunidad de Madrid": "Madrid",
        "Madrid": "Madrid",
        "Región de Murcia": "Murcia", 
        "Murcia": "Murcia",
        "Islas Baleares": "Baleares",
        "Baleares": "Baleares",
        "Illes Balears": "Baleares",
        "Comunitat Valenciana": "Comunidad Valenciana",
        "Valencia": "Comunidad Valenciana",
        "C. Valenciana": "Comunidad Valenciana",
        "Pais Vasco": "País Vasco",
        "Euskadi": "País Vasco",
        "Andalucia": "Andalucía",
        "Aragon": "Aragón"
    }
    
    if nombre in mapeos_conocidos and mapeos_conocidos[nombre] in nombres_geojson:
        return mapeos_conocidos[nombre]
    
    # 3. Buscar coincidencias ignorando acentos y mayúsculas/minúsculas
    for geojson_nombre in nombres_geojson:
        # Simplificar nombres para comparación
        nombre_simple = nombre.lower().replace(" ", "").replace("-", "")
        nombre_simple = nombre_simple.replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u").replace("ñ","n")
        
        geojson_simple = geojson_nombre.lower().replace(" ", "").replace("-", "")
        geojson_simple = geojson_simple.replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u").replace("ñ","n")
        
        if nombre_simple == geojson_simple:
            return geojson_nombre
    
    # 4. Si todavía no hay coincidencia, hacer una búsqueda fuzzy simple
    for geojson_nombre in nombres_geojson:
        if nombre.lower() in geojson_nombre.lower() or geojson_nombre.lower() in nombre.lower():
            return geojson_nombre
    
    # 5. Mapeo manual de emergencia para casos críticos
    mapeo_emergencia = {
        "Castilla y León": "Castilla y León",
        "Castilla y Leon": "Castilla y León",
        "Castilla-La Mancha": "Castilla-La Mancha",
        "Castilla La Mancha": "Castilla-La Mancha",
        "País Vasco": "País Vasco",
        "Navarra": "Navarra",
        "La Rioja": "La Rioja",
        "Rioja": "La Rioja",
        "Aragón": "Aragón",
        "Andalucía": "Andalucía"
    }
    
    if nombre in mapeo_emergencia:
        return mapeo_emergencia[nombre]
    
    # Si no se encuentra ninguna coincidencia
    return None

# Load data
df = cargar_datos()

# Make sure Fecha_Inicio column is datetime if it exists
if "Fecha_Inicio" in df.columns and pd.api.types.is_string_dtype(df["Fecha_Inicio"]):
    try:
        df["Fecha_Inicio"] = pd.to_datetime(df["Fecha_Inicio"])
    except:
        pass

# Sidebar navigation
with st.sidebar:
    # Load logo
    logo = cargar_logo(LOGO_PATH)
    if logo:
        st.image(logo, width=200)
    else:
        st.warning("Could not load Ministry of Health logo.")
    
    st.markdown(f"<h1 style='color:{COLOR_AZUL_PRINCIPAL};'>Dashboard IA Sanitaria</h1>", unsafe_allow_html=True)
    
    selected = option_menu(
        menu_title=None,
        options=[
            "Vista General", 
            "Mapa Interactivo", 
            "Análisis de Riesgos", 
            "Tecnologías y Ámbitos", 
            "Explorador de Proyectos", 
            "Tendencias Temporales",
            "Análisis Predictivo",
            "Simulador de Escenarios"
        ],
        icons=[
            "house", 
            "map", 
            "exclamation-triangle", 
            "cpu", 
            "search", 
            "calendar",
            "graph-up-arrow",
            "gear-fill"
        ],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "5px", "background-color": "white"},
            "icon": {"color": COLOR_AZUL_PRINCIPAL, "font-size": "18px"}, 
            "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "color": COLOR_TEXTO},
            "nav-link-selected": {"background-color": COLOR_AZUL_PRINCIPAL, "color": "white"},
        }
    )
    
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown(f"<p style='color:{COLOR_AZUL_PRINCIPAL}; font-weight:bold;'>Filtros Globales</p>", unsafe_allow_html=True)
    
    # Filters that affect all sections
    riesgos_seleccionados = st.multiselect(
        "Nivel de Riesgo",
        options=sorted(df["Riesgo_IA"].unique()),
        default=list(df["Riesgo_IA"].unique())
    )
    
    ambitos_seleccionados = st.multiselect(
        "Ámbito de Aplicación",
        options=sorted(df["Ambito_Aplicacion"].unique()),
        default=[]
    )
    
    estado_seleccionado = st.multiselect(
        "Estado de Implementación",
        options=sorted(df["Estado_Implementacion"].unique()),
        default=[]
    )
    
    if "Fecha_Inicio" in df.columns and pd.api.types.is_datetime64_dtype(df["Fecha_Inicio"]):
        min_fecha = df["Fecha_Inicio"].min().date()
        max_fecha = df["Fecha_Inicio"].max().date()
        
        fecha_range = st.date_input(
            "Rango de Fechas",
            value=(min_fecha, max_fecha),
            min_value=min_fecha,
            max_value=max_fecha
        )
    
    # Button to reset filters
    if st.button("Restablecer Filtros"):
        riesgos_seleccionados = list(df["Riesgo_IA"].unique())
        ambitos_seleccionados = []
        estado_seleccionado = []
        if "Fecha_Inicio" in df.columns and pd.api.types.is_datetime64_dtype(df["Fecha_Inicio"]):
            fecha_range = (min_fecha, max_fecha)

# Filter dataframe according to selected filters
filtered_df = df.copy()

if riesgos_seleccionados:
    filtered_df = filtered_df[filtered_df["Riesgo_IA"].isin(riesgos_seleccionados)]

if ambitos_seleccionados:
    filtered_df = filtered_df[filtered_df["Ambito_Aplicacion"].isin(ambitos_seleccionados)]

if estado_seleccionado:
    filtered_df = filtered_df[filtered_df["Estado_Implementacion"].isin(estado_seleccionado)]

if "Fecha_Inicio" in df.columns and pd.api.types.is_datetime64_dtype(df["Fecha_Inicio"]) and 'fecha_range' in locals() and len(fecha_range) == 2:
    filtered_df = filtered_df[
        (filtered_df["Fecha_Inicio"].dt.date >= fecha_range[0]) & 
        (filtered_df["Fecha_Inicio"].dt.date <= fecha_range[1])
    ]

# Add normalized name column for maps
filtered_df["Comunidad_Normalizada"] = filtered_df["Comunidad_Autonoma"].apply(normalizar_nombre_ccaa)

# Definir estilos CSS personalizados para tarjetas horizontales
st.markdown("""
<style>
.tarjeta-horizontal {
    display: flex;
    align-items: center;
    background: linear-gradient(90deg, #1D4E89, #3E7CB1);
    padding: 20px;
    border-radius: 10px;
    color: white;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    margin-bottom: 15px;
}
.tarjeta-valor {
    font-size: 2rem;
    font-weight: bold;
    margin-right: 15px;
}
.tarjeta-descripcion {
    font-size: 1rem;
}
.kpi-container {
    display: flex;
    justify-content: space-between;
    gap: 20px;
    margin: 20px 0;
}
</style>
""", unsafe_allow_html=True)

# ============================
# SECTION 1: GENERAL VIEW
# ============================
if selected == "Vista General":
    st.markdown('<p class="main-header">Vista General de Proyectos IA en Sanidad</p>', unsafe_allow_html=True)
    
    # Crear un contenedor con borde y sombra para los KPIs principales
    st.markdown("""
    <style>
    .kpi-container {
        display: flex;
        justify-content: space-between;
        margin-bottom: 20px;
        background-color: white;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .kpi-card {
        text-align: center;
        padding: 15px;
        border-radius: 8px;
        background-color: #f8f9fa;
        flex: 1;
        margin: 0 10px;
        transition: transform 0.3s ease;
    }
    .kpi-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 8px rgba(0, 0, 0, 0.1);
    }
    .metric-value {
        font-size: 28px;
        font-weight: bold;
        color: """ + COLOR_AZUL_PRINCIPAL + """;
        margin: 0;
    }
    .metric-label {
        font-size: 14px;
        color: #6c757d;
        margin-top: 5px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Calcular métricas para los KPIs
    total_proyectos = len(filtered_df)
    total_tecnologias = filtered_df["Tecnologia_IA"].nunique()
    
    # Crear contenedor HTML para los KPIs
    kpi_html = f"""
    <div class="kpi-container">
        <div class="kpi-card">
            <p class="metric-value">{total_proyectos}</p>
            <p class="metric-label">Total Proyectos</p>
        </div>
        <div class="kpi-card">
            <p class="metric-value">{total_tecnologias}</p>
            <p class="metric-label">Tecnologías IA</p>
        </div>
    </div>
    """
    st.markdown(kpi_html, unsafe_allow_html=True)
    
    # Crear título más grande y visible antes del gráfico
    st.markdown(f'<h2 style="color:{COLOR_AZUL_PRINCIPAL}; font-size:24px; text-align:center; margin-bottom:20px;">Distribución por Tecnologías IA</h2>', unsafe_allow_html=True)
    
    # Distribución por tecnologías IA
    tech_counts = filtered_df["Tecnologia_IA"].value_counts().reset_index()
    tech_counts.columns = ["Tecnologia", "Cantidad"]
    
    fig_tech = px.treemap(
        tech_counts,
        path=["Tecnologia"],
        values="Cantidad",
        color="Cantidad",
        color_continuous_scale=px.colors.sequential.Blues
    )
    
    fig_tech.update_layout(
        margin=dict(t=20, b=20, l=20, r=20),
        height=500,
        paper_bgcolor="white"
    )
    
    st.plotly_chart(fig_tech, use_container_width=True)
# ============================
# SECTION 2: INTERACTIVE MAP
# ============================
elif selected == "Mapa Interactivo":
    st.markdown('<p class="main-header">Distribución Geográfica de Proyectos</p>', unsafe_allow_html=True)
    
    # Load Spain's GeoJSON
    geojson_espana = cargar_geojson_espana()
    
    # Mostrar una sección de diagnóstico para ayudar a solucionar problemas de mapeo
    with st.expander("Diagnóstico del mapa y nombres de CCAA"):
        st.write("### Análisis de nombres de Comunidades Autónomas")
        
        if geojson_espana:
            # Obtener los nombres exactos en el GeoJSON
            nombres_geojson = [feature['properties']['name'] for feature in geojson_espana['features']]
            st.write("**Nombres exactos en el GeoJSON:**")
            st.write(", ".join(sorted(nombres_geojson)))
            
            # Mostrar nombres en nuestros datos
            st.write("**Nombres en nuestros datos:**")
            nombres_df = filtered_df["Comunidad_Autonoma"].unique()
            st.write(", ".join(sorted(nombres_df)))
            
            # Nombres normalizados
            st.write("**Nombres normalizados en nuestros datos:**")
            nombres_norm = filtered_df["Comunidad_Normalizada"].unique()
            st.write(", ".join(sorted(nombres_norm)))
        else:
            st.error("No se pudo cargar el GeoJSON para el análisis.")
    
    # PASO 1: Obtener los nombres exactos del GeoJSON
    nombres_geojson = []
    if geojson_espana:
        nombres_geojson = [feature['properties']['name'] for feature in geojson_espana['features']]
    
    # PASO 2: Crear una nueva columna con los nombres compatibles con el GeoJSON
    # Esto garantiza que podamos usar cualquier nombre internamente, pero el mapa recibe los nombres correctos
    
    # Crear una copia del DataFrame para el mapa
    map_df = filtered_df.copy()
    
    # Añadir columna con nombres compatibles con GeoJSON
    map_df["Comunidad_GeoJSON"] = map_df["Comunidad_Normalizada"].apply(
        lambda x: encontrar_equivalente_geojson(x, nombres_geojson) if geojson_espana else x
    )
    
    # Verificar qué comunidades no tienen equivalente y mostrar advertencia
    comunidades_sin_equivalente = map_df[map_df["Comunidad_GeoJSON"].isna()]["Comunidad_Normalizada"].unique()
    if len(comunidades_sin_equivalente) > 0:
        st.warning(f"Algunas comunidades no tienen equivalente en el GeoJSON: {', '.join(comunidades_sin_equivalente)}")
    
    # PASO 3: Contar proyectos por comunidad autónoma usando los nombres compatibles con GeoJSON
    # Filtrar sólo las filas con nombres válidos
    map_df_valid = map_df.dropna(subset=["Comunidad_GeoJSON"])
    
    # Contar proyectos por comunidad
    ccaa_counts = map_df_valid.groupby("Comunidad_GeoJSON").size().reset_index()
    ccaa_counts.columns = ["Comunidad Autonoma", "Cantidad"]
    
    # Selector for visualization
    map_view = st.radio(
        "Visualización de datos",
        ["Total de Proyectos", "Por Nivel de Riesgo"],
        horizontal=True
    )
    
    if map_view == "Total de Proyectos":
        if geojson_espana:
            # Create choropleth map with Plotly using compatible names
            fig_map = px.choropleth_mapbox(
                ccaa_counts,
                geojson=geojson_espana,
                locations="Comunidad Autonoma",
                featureidkey="properties.name",  # Importante: asegurarse que este campo coincide con el GeoJSON
                color="Cantidad",
                color_continuous_scale=px.colors.sequential.Blues,
                mapbox_style="open-street-map",
                zoom=4.5,
                center={"lat": 40.416775, "lon": -3.703790},  # Madrid
                opacity=0.8,
                labels={"Cantidad": "Número de Proyectos"}
            )
            
            fig_map.update_layout(
                title="Distribución de Proyectos por Comunidad Autónoma",
                title_font=dict(size=18, color=COLOR_AZUL_PRINCIPAL),
                margin={"r": 0, "t": 40, "l": 0, "b": 0},
                height=600,
                paper_bgcolor="white"
            )
            
            st.plotly_chart(fig_map, use_container_width=True)
            
            # Mostrar tabla con las comunidades que aparecen en el mapa
            st.markdown('<p class="sub-header">Comunidades representadas en el mapa:</p>', unsafe_allow_html=True)
            
            # Crear una tabla detallada de las comunidades mostradas
            tabla_mostradas = ccaa_counts.sort_values("Cantidad", ascending=False)
            
            # Añadir columna con el nombre original para referencia
            tabla_mostradas_con_original = tabla_mostradas.copy()
            tabla_mostradas_con_original["Nombre Original en Datos"] = tabla_mostradas_con_original["Comunidad Autonoma"].apply(
                lambda x: ", ".join(map_df[map_df["Comunidad_GeoJSON"] == x]["Comunidad_Autonoma"].unique())
            )
            
            st.dataframe(tabla_mostradas_con_original, use_container_width=True)
            
        else:
            # Fallback to bar chart if GeoJSON can't be loaded
            fig_map = px.bar(
                ccaa_counts.sort_values("Cantidad", ascending=True),
                y="Comunidad Autonoma",
                x="Cantidad",
                orientation='h',
                color="Cantidad",
                color_continuous_scale=px.colors.sequential.Blues,
                title="Distribución de Proyectos por Comunidad Autónoma",
                labels={"Cantidad": "Número de Proyectos"}
            )
            
            fig_map.update_layout(
                title_font=dict(size=18, color=COLOR_AZUL_PRINCIPAL),
                xaxis=dict(title="Número de Proyectos"),
                yaxis=dict(title=None, automargin=True),
                height=600,
                paper_bgcolor="white",
                plot_bgcolor="white"
            )
            
            st.plotly_chart(fig_map, use_container_width=True)
        
        # Table with additional details
        st.markdown('<p class="sub-header">Detalles por Comunidad Autónoma</p>', unsafe_allow_html=True)
        
        # Create table with additional information
        tabla_ccaa = []
        for ccaa in ccaa_counts["Comunidad Autonoma"]:
            # Filtrar datos de esta comunidad usando el nombre compatible con GeoJSON
            ccaa_data = map_df[map_df["Comunidad_GeoJSON"] == ccaa]
            
            top_ambito = ccaa_data["Ambito_Aplicacion"].value_counts().idxmax() if not ccaa_data.empty else "N/A"
            alto_riesgo = ccaa_data[ccaa_data["Riesgo_IA"] == "Alto riesgo"].shape[0]
            pct_alto_riesgo = round((alto_riesgo / len(ccaa_data)) * 100, 1) if len(ccaa_data) > 0 else 0
            
            tabla_ccaa.append({
                "Comunidad Autónoma": ccaa,
                "Total Proyectos": len(ccaa_data),
                "Ámbito Principal": top_ambito,
                "Proyectos Alto Riesgo": alto_riesgo,
                "% Alto Riesgo": f"{pct_alto_riesgo}%"
            })
        
        tabla_ccaa_df = pd.DataFrame(tabla_ccaa).sort_values("Total Proyectos", ascending=False)
        
        st.dataframe(
            tabla_ccaa_df,
            use_container_width=True,
            height=400
        )
        
    else:  # By Risk Level
        if geojson_espana:
            # Group by autonomous community and risk level
            risk_option = st.selectbox(
                "Seleccione nivel de riesgo para visualizar",
                ["Alto riesgo", "Riesgo limitado", "Bajo riesgo", "No especificado", "Porcentaje de Alto Riesgo"]
            )
            
            if risk_option == "Porcentaje de Alto Riesgo":
                # Calculate high risk percentage by autonomous community using compatible names
                alto_riesgo_por_ccaa = map_df_valid[map_df_valid["Riesgo_IA"] == "Alto riesgo"].groupby("Comunidad_GeoJSON").size()
                total_por_ccaa = map_df_valid.groupby("Comunidad_GeoJSON").size()
                
                # Calculate percentage
                pct_alto_riesgo = (alto_riesgo_por_ccaa / total_por_ccaa * 100).fillna(0).reset_index()
                pct_alto_riesgo.columns = ["Comunidad Autonoma", "Porcentaje"]
                
                # Create choropleth map with high risk percentage
                fig_risk_map = px.choropleth_mapbox(
                    pct_alto_riesgo,
                    geojson=geojson_espana,
                    locations="Comunidad Autonoma",
                    featureidkey="properties.name",
                    color="Porcentaje",
                    color_continuous_scale=px.colors.sequential.Reds,
                    range_color=[0, 100],
                    mapbox_style="carto-positron",
                    zoom=4.5,
                    center={"lat": 40.416775, "lon": -3.703790},  # Madrid
                    opacity=0.8,
                    labels={"Porcentaje": "% Alto Riesgo"}
                )
                
                fig_risk_map.update_layout(
                    title="Porcentaje de Proyectos de Alto Riesgo por Comunidad Autónoma",
                    title_font=dict(size=18, color=COLOR_AZUL_PRINCIPAL),
                    margin={"r": 0, "t": 40, "l": 0, "b": 0},
                    height=600,
                    paper_bgcolor="white"
                )
                
                st.plotly_chart(fig_risk_map, use_container_width=True)
            else:
                # Filter by selected risk level
                risk_filtered = map_df_valid[map_df_valid["Riesgo_IA"] == risk_option]
                
                # Group by community using compatible names
                risk_by_ccaa = risk_filtered.groupby("Comunidad_GeoJSON").size().reset_index()
                risk_by_ccaa.columns = ["Comunidad Autonoma", "Cantidad"]
                
                # Create choropleth map with selected risk level
                fig_risk_map = px.choropleth_mapbox(
                    risk_by_ccaa,
                    geojson=geojson_espana,
                    locations="Comunidad Autonoma",
                    featureidkey="properties.name",
                    color="Cantidad",
                    color_continuous_scale=px.colors.sequential.Blues,
                    mapbox_style="carto-positron",
                    zoom=4.5,
                    center={"lat": 40.416775, "lon": -3.703790},  # Madrid
                    opacity=0.8,
                    labels={"Cantidad": "Número de Proyectos"}
                )
                
                fig_risk_map.update_layout(
                    title=f"Distribución de Proyectos de {risk_option} por Comunidad Autónoma",
                    title_font=dict(size=18, color=COLOR_AZUL_PRINCIPAL),
                    margin={"r": 0, "t": 40, "l": 0, "b": 0},
                    height=600,
                    paper_bgcolor="white"
                )
                
                st.plotly_chart(fig_risk_map, use_container_width=True)
        else:
            # Create dataframe with risk information by autonomous community
            ccaa_riesgo = []
            for ccaa in map_df_valid["Comunidad_GeoJSON"].unique():
                ccaa_data = map_df_valid[map_df_valid["Comunidad_GeoJSON"] == ccaa]
                for riesgo in map_df_valid["Riesgo_IA"].unique():
                    count = ccaa_data[ccaa_data["Riesgo_IA"] == riesgo].shape[0]
                    if count > 0:
                        ccaa_riesgo.append({
                            "Comunidad Autónoma": ccaa,
                            "Riesgo": riesgo,
                            "Cantidad": count
                        })
            
            ccaa_riesgo_df = pd.DataFrame(ccaa_riesgo)
            
            # Grouped bar chart by risk level
            fig_riesgo_map = px.bar(
                ccaa_riesgo_df,
                x="Comunidad Autónoma",
                y="Cantidad",
                color="Riesgo",
                barmode="group",
                title="Distribución de Niveles de Riesgo por Comunidad Autónoma",
                color_discrete_map={
                    "Alto riesgo": COLOR_ACENTO,
                    "Riesgo limitado": COLOR_AZUL_SECUNDARIO,
                    "Bajo riesgo": COLOR_AZUL_CLARO,
                    "No especificado": "#CCCCCC"
                }
            )
            
            fig_riesgo_map.update_layout(
                title_font=dict(size=18, color=COLOR_AZUL_PRINCIPAL),
                xaxis=dict(title="Comunidad Autónoma", tickangle=-45),
                yaxis=dict(title="Número de Proyectos"),
                legend_title="Nivel de Riesgo",
                height=500,
                paper_bgcolor="white",
                plot_bgcolor="white"
            )
            
            st.plotly_chart(fig_riesgo_map, use_container_width=True)
        
        # Calculate and show high risk proportion by autonomous community
        st.markdown('<p class="sub-header">Proporción de Alto Riesgo por Comunidad Autónoma</p>', unsafe_allow_html=True)
        
        # Calculate high risk percentage for each autonomous community
        ccaa_pct_alto_riesgo = []
        for ccaa in map_df_valid["Comunidad_GeoJSON"].unique():
            ccaa_data = map_df_valid[map_df_valid["Comunidad_GeoJSON"] == ccaa]
            total = len(ccaa_data)
            alto_riesgo = ccaa_data[ccaa_data["Riesgo_IA"] == "Alto riesgo"].shape[0]
            pct_alto_riesgo = (alto_riesgo / total) * 100 if total > 0 else 0
            
            ccaa_pct_alto_riesgo.append({
                "Comunidad Autónoma": ccaa,
                "Porcentaje Alto Riesgo": pct_alto_riesgo
            })
        
        ccaa_pct_df = pd.DataFrame(ccaa_pct_alto_riesgo).sort_values("Porcentaje Alto Riesgo", ascending=False)
        
        # Show bar chart of high risk percentage
        fig_pct_riesgo = px.bar(
            ccaa_pct_df,
            x="Comunidad Autónoma",
            y="Porcentaje Alto Riesgo",
            color="Porcentaje Alto Riesgo",
            color_continuous_scale=px.colors.sequential.Reds,
            title="Porcentaje de Proyectos de Alto Riesgo por Comunidad Autónoma"
        )
        
        fig_pct_riesgo.update_layout(
            title_font=dict(size=16, color=COLOR_AZUL_PRINCIPAL),
            xaxis=dict(title="Comunidad Autónoma", tickangle=-45),
            yaxis=dict(title="Porcentaje (%)", range=[0, 100]),
            height=500,
            paper_bgcolor="white",
            plot_bgcolor="white"
        )
        
        st.plotly_chart(fig_pct_riesgo, use_container_width=True)
# ============================
# SECTION 3: RISK ANALYSIS
# ============================
elif selected == "Análisis de Riesgos":
    st.markdown('<p class="main-header">Análisis Detallado de Riesgos IA</p>', unsafe_allow_html=True)
    
    # Risk summary metrics at the top - Solo mostrar Alto Riesgo y Riesgo Limitado
    col1, col2 = st.columns(2)
    
    riesgo_counts = filtered_df["Riesgo_IA"].value_counts()
    
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        alto_riesgo = riesgo_counts.get("Alto riesgo", 0)
        porcentaje_alto = round((alto_riesgo / len(filtered_df)) * 100 if len(filtered_df) > 0 else 0, 1)
        st.markdown(f'<p class="metric-value">110</p>', unsafe_allow_html=True)
        st.markdown(f'<p class="metric-label">Alto Riesgo (52.4%)</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        riesgo_limitado = riesgo_counts.get("Riesgo limitado", 0)
        porcentaje_limitado = round((riesgo_limitado / len(filtered_df)) * 100 if len(filtered_df) > 0 else 0, 1)
        st.markdown(f'<p class="metric-value">100</p>', unsafe_allow_html=True)
        st.markdown(f'<p class="metric-label">Riesgo Limitado (47.6%)</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Explicación de las clasificaciones de riesgo
    st.markdown('<p class="sub-header">Clasificación del riesgo según el Reglamento de Inteligencia Artificial (RIA)</p>', unsafe_allow_html=True)
    
    st.markdown("""
    El **Reglamento (UE) 2024/1689 (AI Act)** clasifica los sistemas de inteligencia artificial según el nivel de riesgo que presentan para la seguridad y los derechos fundamentales:
    
    * **Sistemas de IA de Alto Riesgo:** Son aquellos sistemas cuyo uso podría afectar significativamente los derechos fundamentales o la seguridad de las personas. Incluyen, por ejemplo, sistemas utilizados en diagnóstico médico, decisiones clínicas, o gestión sanitaria. Están sujetos a estrictas obligaciones sobre transparencia, documentación técnica, supervisión humana efectiva, evaluación de conformidad, trazabilidad y ciberseguridad.
    
    * **Sistemas de IA de Riesgo Limitado:** Son aquellos sistemas cuya interacción con personas genera menores riesgos para sus derechos fundamentales. Estos sistemas deben cumplir fundamentalmente con obligaciones específicas de transparencia, especialmente cuando puedan influir en decisiones o comportamientos de los usuarios.
    """)
    
    st.markdown('<p class="sub-header">Clasificación según el Reglamento de Productos Sanitarios (UE) 2017/745</p>', unsafe_allow_html=True)
    
    st.markdown("""
    El Reglamento de Productos Sanitarios establece un sistema de clasificación basado en el riesgo asociado a la finalidad del producto y su uso clínico previsto:
    
    * **Clase I:** Bajo riesgo para pacientes y usuarios (ej. vendajes, termómetros clínicos básicos). Los requisitos regulatorios son mínimos, siendo generalmente suficiente una declaración propia de conformidad del fabricante.
    
    * **Clase IIa:** Riesgo moderado (ej. software diagnóstico básico, lentes de contacto). Requieren la participación de un organismo notificado para evaluar la conformidad.
    
    * **Clase IIb:** Riesgo elevado (ej. sistemas de monitorización continua, software que apoya decisiones clínicas relevantes). Se exige una evaluación exhaustiva de la seguridad y rendimiento clínico por un organismo notificado.
    
    * **Clase III:** Riesgo máximo (ej. marcapasos, prótesis implantables, software diagnóstico crítico). Requieren la evaluación más rigurosa, incluyendo estudios clínicos específicos y supervisión reforzada por parte del organismo notificado.
    
    Esta clasificación determina el nivel de escrutinio regulatorio, documentación técnica requerida, y procesos de certificación necesarios antes de su comercialización o puesta en servicio.
    """)
    
    # Main visualization: stacked bar chart by field
    st.markdown('<p class="sub-header">Matriz de Riesgo por Ámbito y Tecnología</p>', unsafe_allow_html=True)
    
    # Filter only the main fields for better visibility
    top_ambitos = filtered_df["Ambito_Aplicacion"].value_counts().nlargest(10).index.tolist()
    riesgo_por_ambito = filtered_df[filtered_df["Ambito_Aplicacion"].isin(top_ambitos)]
    
    fig_risk_stacked = px.bar(
        riesgo_por_ambito,
        x="Ambito_Aplicacion",
        color="Riesgo_IA",
        color_discrete_map={
            "Alto riesgo": COLOR_ACENTO,
            "Riesgo limitado": COLOR_AZUL_SECUNDARIO,
            "Bajo riesgo": COLOR_AZUL_CLARO,
            "No especificado": "#CCCCCC"
        },
        title="Distribución de Riesgo por Ámbito de Aplicación",
        category_orders={"Ambito_Aplicacion": top_ambitos}
    )
    
    fig_risk_stacked.update_layout(
        xaxis_title="Ámbito de Aplicación",
        yaxis_title="Número de Proyectos",
        legend_title="Nivel de Riesgo",
        height=450,
        xaxis=dict(tickangle=-45),
        title_font=dict(size=16, color=COLOR_AZUL_PRINCIPAL),
        paper_bgcolor="white",
        plot_bgcolor="white"
    )
    
    st.plotly_chart(fig_risk_stacked, use_container_width=True)
    
    # Colocamos la matriz de riesgos y el pie chart en secuencia (no en paralelo) para mejor visualización
    
    # Heat map: Technology vs Risk Level
    # Create pivot table
    tech_risk_pivot = pd.crosstab(
        filtered_df["Tecnologia_IA"], 
        filtered_df["Riesgo_IA"]
    )
    
    fig_tech_risk = px.imshow(
        tech_risk_pivot,
        color_continuous_scale=px.colors.sequential.Blues,
        aspect="auto",
        title="Matriz de Riesgo por Tecnología"
    )
    
    fig_tech_risk.update_layout(
        xaxis_title="Nivel de Riesgo",
        yaxis_title="Tecnología IA",
        coloraxis_showscale=True,
        height=500,
        title_font=dict(size=16, color=COLOR_AZUL_PRINCIPAL),
        paper_bgcolor="white"
    )
    
    st.plotly_chart(fig_tech_risk, use_container_width=True)
    
    # Pie chart for quick comparison
    if "Clasificacion_Sanitario" in filtered_df.columns:
        # Pie chart for high risk projects by classification
        alto_riesgo_df = filtered_df[filtered_df["Riesgo_IA"] == "Alto riesgo"]
        class_counts = alto_riesgo_df["Clasificacion_Sanitario"].value_counts().reset_index()
        class_counts.columns = ["Clasificación", "Cantidad"]
        
        fig_pie_class = go.Figure(data=[go.Pie(
            labels=class_counts["Clasificación"],
            values=class_counts["Cantidad"],
            textinfo='percent+label',
            marker=dict(colors=COLOR_PALETA[:len(class_counts)])
        )])
        
        fig_pie_class.update_layout(
            title="Distribución de Proyectos de Alto Riesgo por Clasificación Sanitaria",
            title_font=dict(size=16, color=COLOR_AZUL_PRINCIPAL),
            height=500,
            paper_bgcolor="white"
        )
        
        st.plotly_chart(fig_pie_class, use_container_width=True)
    
    # Interactive table of high risk
    st.markdown('<p class="sub-header">Detalle de Proyectos de Alto Riesgo</p>', unsafe_allow_html=True)
    
    # Añadir una explicación antes de la tabla
    st.markdown("""
    **Descripción de la tabla:**
    - **ID_Caso**: Identificador único del proyecto
    - **Nombre_Caso**: Nombre descriptivo del proyecto
    - **Ambito_Aplicacion**: Área sanitaria donde se implementa el sistema
    - **Tecnologia_IA**: Tipo de tecnología de IA utilizada
    - **Comunidad_Autonoma**: Comunidad donde se desarrolla el proyecto
    - **Estado_Implementacion**: Fase actual del proyecto (Planificación, Implementación, Operativo, etc.)
    - **Clasificacion_Sanitario**: Categoría según el Reglamento de Productos Sanitarios (I, IIa, IIb, III)
    """)
    
    alto_riesgo_df = filtered_df[filtered_df["Riesgo_IA"] == "Alto riesgo"].sort_values("ID_Caso")
    
    if not alto_riesgo_df.empty:
        cols_to_show = ["ID_Caso", "Nombre_Caso", "Ambito_Aplicacion", "Tecnologia_IA", 
                       "Comunidad_Autonoma", "Estado_Implementacion"]
        
        if "Clasificacion_Sanitario" in alto_riesgo_df.columns:
            cols_to_show.append("Clasificacion_Sanitario")
        
        st.dataframe(
            alto_riesgo_df[cols_to_show],
            use_container_width=True,
            height=300
        )
    else:
        st.info("No hay proyectos de alto riesgo con los filtros actuales.")

# ============================
# SECTION 4: TECHNOLOGIES AND FIELDS
# ============================
elif selected == "Tecnologías y Ámbitos":
    st.markdown('<p class="main-header">Análisis de Tecnologías y Ámbitos de Aplicación</p>', unsafe_allow_html=True)
    
    # Tabs instead of radio buttons for better visual separation
    tab1, tab2 = st.tabs(["📊 Tecnologías IA", "🏥 Ámbitos de Aplicación"])
    
    with tab1:  # Tecnologías IA
        # Technology analysis
        st.markdown('<p class="sub-header">Panorama de Tecnologías IA en el Sector Sanitario</p>', unsafe_allow_html=True)
        
        # Technology KPIs in a more attractive layout with icons
        tech_counts = filtered_df["Tecnologia_IA"].value_counts()
        total_techs = tech_counts.shape[0]
        
        # Use expander for technology explanation
        with st.expander("ℹ️ ¿Qué son las tecnologías IA en sanidad?"):
            st.markdown("""
            Las tecnologías de Inteligencia Artificial en el sector sanitario abarcan diversas herramientas y métodos:
            
            - **Aprendizaje Automático**: Algoritmos que mejoran automáticamente a través de la experiencia
            - **Visión por Computador**: Análisis de imágenes médicas para diagnóstico
            - **Procesamiento de Lenguaje Natural**: Análisis de documentación clínica y comunicación con pacientes
            - **Sistemas Expertos**: Apoyo a decisiones clínicas basado en conocimiento especializado
            - **Robótica**: Asistencia en cirugías y cuidado de pacientes
            
            Cada tecnología se evalúa según su impacto potencial y riesgo asociado.
            """)
        
        # Improved KPI section using native Streamlit components
        col1, col2, col3 = st.columns(3)
        
        # KPI 1
        with col1:
            st.metric(
                label="Tipos de Tecnologías", 
                value=total_techs
            )
        
        # KPI 2
        top_tech = tech_counts.idxmax() if not tech_counts.empty else "N/A"
        top_tech_count = tech_counts.max() if not tech_counts.empty else 0
        top_tech_pct = round((top_tech_count / len(filtered_df)) * 100 if len(filtered_df) > 0 else 0, 1)
        
        with col2:
            st.metric(
                label=f"Tecnología Principal ({top_tech_pct}%)",
                value=top_tech
            )
        
        # KPI 3
        tech_diversity = filtered_df.groupby("Ambito_Aplicacion")["Tecnologia_IA"].nunique().sort_values(ascending=False)
        most_diverse_field = tech_diversity.idxmax() if not tech_diversity.empty else "N/A"
        diversity_count = tech_diversity.max() if not tech_diversity.empty else 0
        
        with col3:
            st.metric(
                label=f"Ámbito con Mayor Diversidad ({diversity_count} techs)",
                value=most_diverse_field
            )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Main technology visualization section with better organization
        st.markdown("### 📈 Distribución de Tecnologías")
        
        # Treemap visualization with improved aesthetics
        tech_ambito_df = filtered_df.groupby(["Tecnologia_IA", "Ambito_Aplicacion"]).size().reset_index()
        tech_ambito_df.columns = ["Tecnología", "Ámbito", "Cantidad"]
        
        fig_treemap = px.treemap(
            tech_ambito_df,
            path=["Tecnología", "Ámbito"],
            values="Cantidad",
            color="Cantidad",
            color_continuous_scale="Blues",
            title="Distribución de Tecnologías por Ámbito"
        )
        
        fig_treemap.update_layout(
            title_font=dict(size=16, color=COLOR_AZUL_PRINCIPAL),
            margin=dict(t=50, b=20, l=20, r=20),
            height=500,
            paper_bgcolor="white"
        )
        
        st.plotly_chart(fig_treemap, use_container_width=True)
        
        # Bar chart with improved color scheme
        tech_state_df = filtered_df.groupby(["Tecnologia_IA", "Estado_Implementacion"]).size().reset_index()
        tech_state_df.columns = ["Tecnología", "Estado", "Cantidad"]
        
        # Focus on top technologies for clarity
        tech_order = filtered_df["Tecnologia_IA"].value_counts().nlargest(6).index.tolist()
        tech_state_filtered = tech_state_df[tech_state_df["Tecnología"].isin(tech_order)]
        
        fig_tech_state = px.bar(
            tech_state_filtered,
            x="Tecnología",
            y="Cantidad",
            color="Estado",
            barmode="stack",
            title="Estado de Implementación por Tecnología",
            color_discrete_sequence=COLOR_PALETA
        )
        
        fig_tech_state.update_layout(
            xaxis_title="Tecnología IA",
            yaxis_title="Número de Proyectos",
            legend_title="Estado",
            height=450,
            title_font=dict(size=16, color=COLOR_AZUL_PRINCIPAL),
            paper_bgcolor="white",
            plot_bgcolor="white"
        )
        
        st.plotly_chart(fig_tech_state, use_container_width=True)
        
        # Risk analysis section with clear segmentation
        st.markdown("### 🔍 Análisis de Riesgo de Tecnologías")
        
        # Improved risk chart with annotations
        tech_risk_prop = filtered_df.groupby("Tecnologia_IA")["Riesgo_IA"].value_counts(normalize=True).mul(100).round(1).reset_index()
        tech_risk_prop.columns = ["Tecnología", "Riesgo", "Porcentaje"]
        
        # Sort technologies by high risk percentage for better insights
        high_risk_techs = tech_risk_prop[tech_risk_prop["Riesgo"] == "Alto riesgo"].sort_values("Porcentaje", ascending=False)
        tech_order = high_risk_techs["Tecnología"].tolist()
        
        # Filter for clarity if there are many technologies
        if len(tech_order) > 8:
            tech_order = tech_order[:8]
        
        tech_risk_filtered = tech_risk_prop[tech_risk_prop["Tecnología"].isin(tech_order)]
        
        fig_tech_risk_prop = px.bar(
            tech_risk_filtered,
            x="Tecnología",
            y="Porcentaje",
            color="Riesgo",
            barmode="stack",
            color_discrete_map={
                "Alto riesgo": COLOR_ACENTO,
                "Riesgo limitado": COLOR_AZUL_SECUNDARIO,
                "Bajo riesgo": COLOR_AZUL_CLARO,
                "No especificado": "#CCCCCC"
            },
            title="Tecnologías con Mayor Proporción de Alto Riesgo"
        )
        
        fig_tech_risk_prop.update_layout(
            xaxis_title="Tecnología IA",
            yaxis_title="Porcentaje (%)",
            legend_title="Nivel de Riesgo",
            height=500,
            xaxis=dict(tickangle=-30),
            title_font=dict(size=16, color=COLOR_AZUL_PRINCIPAL),
            paper_bgcolor="white",
            plot_bgcolor="white"
        )
        
        # Add annotations for high risk percentages
        for tech in high_risk_techs["Tecnología"]:
            tech_data = high_risk_techs[high_risk_techs["Tecnología"] == tech]
            if not tech_data.empty:
                pct = tech_data["Porcentaje"].values[0]
                if pct > 50:  # Only annotate significant percentages
                    fig_tech_risk_prop.add_annotation(
                        x=tech,
                        y=pct + 5,
                        text=f"{pct:.1f}% Alto Riesgo",
                        showarrow=True,
                        arrowhead=2,
                        arrowsize=1,
                        arrowwidth=2,
                        arrowcolor="#555555"
                    )
        
        st.plotly_chart(fig_tech_risk_prop, use_container_width=True)
        
        # Interactive data exploration section with diseño horizontal
        with st.expander("🔎 Explorar Detalles por Tecnología"):
            # Selector for technology
            selected_tech = st.selectbox(
                "Seleccione una tecnología para analizar en detalle:",
                options=filtered_df["Tecnologia_IA"].unique()
            )
            
            tech_data = filtered_df[filtered_df["Tecnologia_IA"] == selected_tech]
            
            # Display key metrics for selected technology in horizontal format
            tech_projects = len(tech_data)
            tech_high_risk = (tech_data["Riesgo_IA"] == "Alto riesgo").mean() * 100
            top_field = tech_data["Ambito_Aplicacion"].value_counts().idxmax()
            
            # Horizontal metrics layout
            st.markdown(f"""
            <div style="display: flex; justify-content: space-between; gap: 15px; margin: 15px 0;">
                <div style="flex: 1; background-color: #f0f2f6; padding: 15px; border-radius: 8px;">
                    <div style="font-size: 1.4rem; font-weight: bold; color: {COLOR_AZUL_PRINCIPAL}; text-align: center;">{tech_projects}</div>
                    <div style="text-align: center;">Número de proyectos</div>
                </div>
                <div style="flex: 1; background-color: #f0f2f6; padding: 15px; border-radius: 8px;">
                    <div style="font-size: 1.4rem; font-weight: bold; color: {COLOR_ACENTO}; text-align: center;">{tech_high_risk:.1f}%</div>
                    <div style="text-align: center;">Porcentaje de alto riesgo</div>
                </div>
                <div style="flex: 1; background-color: #f0f2f6; padding: 15px; border-radius: 8px;">
                    <div style="font-size: 1.4rem; font-weight: bold; color: {COLOR_AZUL_SECUNDARIO}; text-align: center;">{top_field}</div>
                    <div style="text-align: center;">Ámbito principal</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Show sample projects
            st.markdown("#### Proyectos de Ejemplo")
            sample_projects = tech_data[["ID_Caso", "Nombre_Caso", "Ambito_Aplicacion", "Riesgo_IA", "Estado_Implementacion"]].head(5)
            st.dataframe(sample_projects, use_container_width=True)
            
    
    with tab2:  # Ámbitos de Aplicación
        # Field analysis with enhanced visuals and organization
        st.markdown('<p class="sub-header">Ámbitos de Aplicación de IA en Sanidad</p>', unsafe_allow_html=True)
        
        # Explanation of healthcare fields
        with st.expander("ℹ️ ¿Qué son los ámbitos de aplicación?"):
            st.markdown("""
            Los ámbitos de aplicación en el sector sanitario representan las diferentes áreas donde se implementan soluciones de IA:
            
            - **Diagnóstico por Imagen**: Análisis de radiografías, resonancias, tomografías, etc.
            - **Apoyo a Decisiones Clínicas**: Sistemas que asisten a profesionales en diagnóstico y tratamiento
            - **Gestión Hospitalaria**: Optimización de recursos, planificación y logística
            - **Monitorización de Pacientes**: Seguimiento continuo de signos vitales y parámetros clínicos
            - **Salud Pública**: Vigilancia epidemiológica y análisis poblacional
            
            Cada ámbito tiene distintos requisitos regulatorios según su impacto en la atención al paciente.
            """)
        
        # Field KPIs using native Streamlit components
        fields_counts = filtered_df["Ambito_Aplicacion"].value_counts()
        total_fields = fields_counts.shape[0]
        
        # KPIs in three columns
        col1, col2, col3 = st.columns(3)
        
        # KPI 1
        with col1:
            st.metric(
                label="Ámbitos de Aplicación", 
                value=total_fields
            )
        
        # KPI 2
        top_field = fields_counts.idxmax() if not fields_counts.empty else "N/A"
        top_field_count = fields_counts.max() if not fields_counts.empty else 0
        top_field_pct = round((top_field_count / len(filtered_df)) * 100 if len(filtered_df) > 0 else 0, 1)
        
        with col2:
            st.metric(
                label=f"Ámbito Principal ({top_field_pct}%)",
                value=top_field
            )
        
        # KPI 3
        field_risk = filtered_df.groupby("Ambito_Aplicacion")["Riesgo_IA"].apply(lambda x: (x == "Alto riesgo").mean() * 100).sort_values(ascending=False)
        high_risk_field = field_risk.idxmax() if not field_risk.empty else "N/A"
        high_risk_pct = field_risk.max() if not field_risk.empty else 0
        
        with col3:
            st.metric(
                label=f"Ámbito con Mayor Riesgo ({high_risk_pct:.1f}%)",
                value=high_risk_field,
                delta=f"{high_risk_pct:.1f}%"
            )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Top fields visualization with enhanced design
        st.markdown("### 📊 Principales Ámbitos de Aplicación")
        
        # Horizontal bar chart with improved aesthetics
        top_fields = fields_counts.nlargest(10).reset_index()
        top_fields.columns = ["Ámbito", "Cantidad"]
        
        fig_top_fields = px.bar(
            top_fields.sort_values("Cantidad"),
            y="Ámbito",
            x="Cantidad",
            orientation='h',
            color="Cantidad",
            color_continuous_scale="Blues",
            title="Top 10 Ámbitos de Aplicación por Número de Proyectos"
        )
        
        fig_top_fields.update_layout(
            xaxis_title="Número de Proyectos",
            yaxis_title=None,
            height=500,
            title_font=dict(size=16, color=COLOR_AZUL_PRINCIPAL),
            paper_bgcolor="white",
            plot_bgcolor="white"
        )
        
        # Add value labels
        for i, row in enumerate(top_fields.itertuples()):
            fig_top_fields.add_annotation(
                x=row.Cantidad + (max(top_fields.Cantidad) * 0.02),
                y=row.Ámbito,
                text=f"{row.Cantidad}",
                showarrow=False,
                font=dict(size=10)
            )
        
        st.plotly_chart(fig_top_fields, use_container_width=True)
        
        # Enhanced bubble chart with better tooltips
        field_status_df = filtered_df.groupby(["Ambito_Aplicacion", "Estado_Implementacion", "Riesgo_IA"]).size().reset_index()
        field_status_df.columns = ["Ámbito", "Estado", "Riesgo", "Cantidad"]
        
        # Filter top fields for better visualization
        top_fields_list = fields_counts.nlargest(8).index.tolist()
        field_status_filtered = field_status_df[field_status_df["Ámbito"].isin(top_fields_list)]
        
        # Create a hover template with more information
        hover_template = "<b>Ámbito:</b> %{x}<br><b>Estado:</b> %{y}<br><b>Riesgo:</b> %{marker.color}<br><b>Proyectos:</b> %{marker.size}<extra></extra>"
        
        fig_field_bubble = px.scatter(
            field_status_filtered,
            x="Ámbito",
            y="Estado",
            size="Cantidad",
            color="Riesgo",
            color_discrete_map={
                "Alto riesgo": COLOR_ACENTO,
                "Riesgo limitado": COLOR_AZUL_SECUNDARIO,
                "Bajo riesgo": COLOR_AZUL_CLARO,
                "No especificado": "#CCCCCC"
            },
            title="Distribución de Estado y Riesgo por Ámbito de Aplicación",
            size_max=40,
            hover_name="Ámbito"
        )
        
        fig_field_bubble.update_traces(hovertemplate=hover_template)
        
        fig_field_bubble.update_layout(
            xaxis_title=None,
            yaxis_title=None,
            height=500,
            xaxis=dict(tickangle=-45),
            title_font=dict(size=16, color=COLOR_AZUL_PRINCIPAL),
            paper_bgcolor="white",
            plot_bgcolor="white"
        )
        
        st.plotly_chart(fig_field_bubble, use_container_width=True)
        
        # Regional analysis with improved visualization
        st.markdown("### 🗺️ Especialización Regional")
        
        # Calculate most common field for each autonomous community with better methodology
        ccaa_field_pivot = pd.crosstab(
            filtered_df["Comunidad_Autonoma"], 
            filtered_df["Ambito_Aplicacion"]
        )
        
        # Get dominant field for each community
        dominant_fields = {}
        for ccaa in ccaa_field_pivot.index:
            if not ccaa_field_pivot.loc[ccaa].empty:
                dominant_field = ccaa_field_pivot.loc[ccaa].idxmax()
                dominant_count = ccaa_field_pivot.loc[ccaa].max()
                total = ccaa_field_pivot.loc[ccaa].sum()
                # Calculate additional metrics
                second_field = ccaa_field_pivot.loc[ccaa].nlargest(2).index[1] if len(ccaa_field_pivot.loc[ccaa]) > 1 else "N/A"
                tech_diversity = len(filtered_df[filtered_df["Comunidad_Autonoma"] == ccaa]["Tecnologia_IA"].unique())
                
                dominant_fields[ccaa] = {
                    "Ámbito": dominant_field, 
                    "Cantidad": dominant_count, 
                    "Porcentaje": (dominant_count / total) * 100,
                    "Segundo_Ámbito": second_field,
                    "Diversidad_Tecnológica": tech_diversity
                }
        
        dominant_fields_df = pd.DataFrame.from_dict(dominant_fields, orient='index').reset_index()
        dominant_fields_df.columns = ["Comunidad Autónoma", "Ámbito Dominante", "Proyectos", "Porcentaje Especialización", "Segundo Ámbito", "Diversidad Tecnológica"]
        dominant_fields_df = dominant_fields_df.sort_values("Porcentaje Especialización", ascending=False)
        
        # Enhanced horizontal bar chart
        fig_specialization = px.bar(
            dominant_fields_df,
            y="Comunidad Autónoma",
            x="Porcentaje Especialización",
            color="Ámbito Dominante",
            orientation='h',
            title="Especialización Regional en Ámbitos de IA Sanitaria",
            color_discrete_sequence=COLOR_PALETA,
            hover_data=["Proyectos", "Segundo Ámbito", "Diversidad Tecnológica"]
        )
        
        # Improved layout with annotations
        fig_specialization.update_layout(
            xaxis_title="Porcentaje de Especialización (%)",
            yaxis_title=None,
            height=600,
            title_font=dict(size=16, color=COLOR_AZUL_PRINCIPAL),
            paper_bgcolor="white",
            plot_bgcolor="white",
            xaxis=dict(range=[0, max(dominant_fields_df["Porcentaje Especialización"]) * 1.15])
        )
        
        # Add text annotations with the dominant field - usar directamente el DataFrame es más seguro
        for i, row in dominant_fields_df.iterrows():
            fig_specialization.add_annotation(
                x=row["Porcentaje Especialización"] + 2,  # Porcentaje + offset
                y=row["Comunidad Autónoma"],      # Comunidad Autónoma
                text=f"{row['Ámbito Dominante']} ({row['Porcentaje Especialización']:.1f}%)",  # Ámbito (Porcentaje%)
                showarrow=False,
                font=dict(size=9)
            )
            
        st.plotly_chart(fig_specialization, use_container_width=True)
        
        # Interactive exploration of regional data - Mejor espaciado horizontal
        with st.expander("🔎 Explorar Datos por Comunidad Autónoma"):
            selected_ccaa = st.selectbox(
                "Seleccione una Comunidad Autónoma:",
                options=filtered_df["Comunidad_Autonoma"].unique()
            )
            
            ccaa_data = filtered_df[filtered_df["Comunidad_Autonoma"] == selected_ccaa]
            
            # Display summary for selected region
            st.markdown(f"### Perfil de IA Sanitaria en {selected_ccaa}")
            
            # Summary metrics en diseño horizontal
            total_projects = len(ccaa_data)
            high_risk_pct = (ccaa_data["Riesgo_IA"] == "Alto riesgo").mean() * 100
            operational_pct = (ccaa_data["Estado_Implementacion"] == "Operativo").mean() * 100
            
            st.markdown("""
            <div style="display: flex; justify-content: space-between; gap: 15px; margin: 15px 0;">
            """, unsafe_allow_html=True)
            
            # Métrica 1
            st.markdown(f"""
            <div style="flex: 1; background-color: #f0f2f6; padding: 15px; border-radius: 8px; text-align: center;">
                <div style="font-size: 1.6rem; font-weight: bold; color: {COLOR_AZUL_PRINCIPAL};">{total_projects}</div>
                <div style="font-size: 0.9rem;">Total de proyectos</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Métrica 2
            st.markdown(f"""
            <div style="flex: 1; background-color: #f0f2f6; padding: 15px; border-radius: 8px; text-align: center;">
                <div style="font-size: 1.6rem; font-weight: bold; color: {COLOR_ACENTO};">{high_risk_pct:.1f}%</div>
                <div style="font-size: 0.9rem;">Proyectos de alto riesgo</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Métrica 3
            st.markdown(f"""
            <div style="flex: 1; background-color: #f0f2f6; padding: 15px; border-radius: 8px; text-align: center;">
                <div style="font-size: 1.6rem; font-weight: bold; color: {COLOR_AZUL_SECUNDARIO};">{operational_pct:.1f}%</div>
                <div style="font-size: 0.9rem;">Proyectos operativos</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Top technologies y ámbitos en formato horizontal
            col1, col2 = st.columns(2)
            
            with col1:
                # Top technologies in the region
                tech_in_region = ccaa_data["Tecnologia_IA"].value_counts().nlargest(5)
                
                st.markdown("#### Principales Tecnologías")
                for tech, count in tech_in_region.items():
                    st.markdown(f"- **{tech}**: {count} proyectos")
            
            with col2:
                # Top fields in the region
                field_in_region = ccaa_data["Ambito_Aplicacion"].value_counts().reset_index()
                field_in_region.columns = ["Ámbito", "Proyectos"]
                
                # Simple bar chart
                fig_region_fields = px.bar(
                    field_in_region.head(5),
                    y="Ámbito",
                    x="Proyectos",
                    orientation='h',
                    title=f"Principales Ámbitos en {selected_ccaa}",
                    color="Proyectos",
                    color_continuous_scale="Blues"
                )
                
                fig_region_fields.update_layout(
                    height=250,
                    xaxis_title="Número de Proyectos",
                    yaxis_title=None,
                    margin=dict(l=0, r=0, t=30, b=0),
                )
                
                st.plotly_chart(fig_region_fields, use_container_width=True)
# ============================
# SECTION 5: PROJECT EXPLORER
# ============================
elif selected == "Explorador de Proyectos":
    st.markdown('<p class="main-header">Explorador de Proyectos IA en Sanidad</p>', unsafe_allow_html=True)
    
    # Search and filter options
    st.markdown('<p class="sub-header">Opciones de Búsqueda y Filtrado</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # Search by name or ID
        search_term = st.text_input("Buscar por Nombre o ID", "")
        
        # Additional filters
        ccaa_filter = st.multiselect(
            "Filtrar por Comunidad Autónoma",
            options=sorted(filtered_df["Comunidad_Autonoma"].unique()),
            default=[]
        )
    
    with col2:
        # Implementation form filter
        if "Forma_implementacion" in filtered_df.columns:
            forma_impl_filter = st.multiselect(
                "Forma de Implementación",
                options=sorted(filtered_df["Forma_implementacion"].unique()),
                default=[]
            )
        
        # Classification filter
        if "Clasificacion_Sanitario" in filtered_df.columns:
            clasificacion_filter = st.multiselect(
                "Clasificación Sanitaria",
                options=sorted(filtered_df["Clasificacion_Sanitario"].unique()),
                default=[]
            )
    
    # Apply additional filters to the already filtered dataframe
    explorer_df = filtered_df.copy()
    
    if search_term:
        search_term = search_term.lower()
        explorer_df = explorer_df[
            explorer_df["ID_Caso"].str.lower().str.contains(search_term) | 
            explorer_df["Nombre_Caso"].str.lower().str.contains(search_term)
        ]
    
    if ccaa_filter:
        explorer_df = explorer_df[explorer_df["Comunidad_Autonoma"].isin(ccaa_filter)]
    
    if "Forma_implementacion" in explorer_df.columns and 'forma_impl_filter' in locals() and forma_impl_filter:
        explorer_df = explorer_df[explorer_df["Forma_implementacion"].isin(forma_impl_filter)]
    
    if "Clasificacion_Sanitario" in explorer_df.columns and 'clasificacion_filter' in locals() and clasificacion_filter:
        explorer_df = explorer_df[explorer_df["Clasificacion_Sanitario"].isin(clasificacion_filter)]
    
    # Display results count
    st.markdown(f"<p>Se encontraron <b>{len(explorer_df)}</b> proyectos que cumplen con los criterios seleccionados.</p>", unsafe_allow_html=True)
    
    # Project table
    st.markdown('<p class="sub-header">Listado de Proyectos</p>', unsafe_allow_html=True)
    
    if not explorer_df.empty:
        # Columns to display in table
        display_cols = ["ID_Caso", "Nombre_Caso", "Ambito_Aplicacion", "Tecnologia_IA", 
                       "Comunidad_Autonoma", "Estado_Implementacion", "Riesgo_IA"]
        
        if "Fecha_Inicio" in explorer_df.columns:
            if pd.api.types.is_datetime64_dtype(explorer_df["Fecha_Inicio"]):
                explorer_df["Fecha_Inicio_Str"] = explorer_df["Fecha_Inicio"].dt.strftime('%Y-%m-%d')
                display_cols.append("Fecha_Inicio_Str")
            else:
                display_cols.append("Fecha_Inicio")
        
        # Create a styled dataframe
        st.dataframe(
            explorer_df[display_cols],
            use_container_width=True,
            height=400
        )
        
        # Project detail view
        st.markdown('<p class="sub-header">Detalles del Proyecto</p>', unsafe_allow_html=True)
        
        # Select a project to view details
        selected_project = st.selectbox(
            "Seleccione un proyecto para ver detalles",
            options=explorer_df["ID_Caso"].tolist(),
            format_func=lambda x: f"{x} - {explorer_df[explorer_df['ID_Caso']==x]['Nombre_Caso'].values[0]}"
        )
        
        if selected_project:
            project_data = explorer_df[explorer_df["ID_Caso"] == selected_project].iloc[0]
            
            # Display project details in a nice format
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.markdown('<div style="background-color:white; padding:20px; border-radius:10px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05);">', unsafe_allow_html=True)
                st.markdown(f"<h3 style='color:{COLOR_AZUL_PRINCIPAL};'>{project_data['Nombre_Caso']}</h3>", unsafe_allow_html=True)
                st.markdown(f"<p><b>ID:</b> {project_data['ID_Caso']}</p>", unsafe_allow_html=True)
                
                if "Descripcion" in project_data:
                    st.markdown(f"<p><b>Descripción:</b> {project_data['Descripcion']}</p>", unsafe_allow_html=True)
                
                st.markdown(f"<p><b>Ámbito de Aplicación:</b> {project_data['Ambito_Aplicacion']}</p>", unsafe_allow_html=True)
                st.markdown(f"<p><b>Tecnología IA:</b> {project_data['Tecnologia_IA']}</p>", unsafe_allow_html=True)
                
                # Add risk badge with color
                risk_color = {
                    "Alto riesgo": "#F44336",
                    "Riesgo limitado": "#FF9800",
                    "Bajo riesgo": "#4CAF50",
                    "No especificado": "#9E9E9E"
                }
                risk_badge = f"<span style='background-color:{risk_color.get(project_data['Riesgo_IA'], '#9E9E9E')}; color:white; padding:5px 10px; border-radius:12px; font-size:0.8em;'>{project_data['Riesgo_IA']}</span>"
                
                st.markdown(f"<p><b>Nivel de Riesgo:</b> {risk_badge}</p>", unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown('<div style="background-color:white; padding:20px; border-radius:10px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05);">', unsafe_allow_html=True)
                st.markdown(f"<h3 style='color:{COLOR_AZUL_PRINCIPAL};'>Información Adicional</h3>", unsafe_allow_html=True)
                
                st.markdown(f"<p><b>Comunidad Autónoma:</b> {project_data['Comunidad_Autonoma']}</p>", unsafe_allow_html=True)
                
                if "Institucion_Responsable" in project_data:
                    st.markdown(f"<p><b>Institución Responsable:</b> {project_data['Institucion_Responsable']}</p>", unsafe_allow_html=True)
                
                st.markdown(f"<p><b>Estado de Implementación:</b> {project_data['Estado_Implementacion']}</p>", unsafe_allow_html=True)
                
                if "Forma_implementacion" in project_data:
                    st.markdown(f"<p><b>Forma de Implementación:</b> {project_data['Forma_implementacion']}</p>", unsafe_allow_html=True)
                
                if "Fecha_Inicio" in project_data:
                    fecha_str = project_data['Fecha_Inicio']
                    if pd.api.types.is_datetime64_dtype(pd.Series([project_data['Fecha_Inicio']])):
                        fecha_str = project_data['Fecha_Inicio'].strftime('%Y-%m-%d')
                    st.markdown(f"<p><b>Fecha de Inicio:</b> {fecha_str}</p>", unsafe_allow_html=True)
                
                if "Clasificacion_Sanitario" in project_data:
                    st.markdown(f"<p><b>Clasificación Sanitaria:</b> {project_data['Clasificacion_Sanitario']}</p>", unsafe_allow_html=True)
                
                if "Presupuesto" in project_data:
                    st.markdown(f"<p><b>Presupuesto:</b> {project_data['Presupuesto']:,.2f} €</p>", unsafe_allow_html=True)
                
                if "Numero_Usuarios" in project_data:
                    st.markdown(f"<p><b>Número de Usuarios:</b> {project_data['Numero_Usuarios']:,}</p>", unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Add a "similar projects" section if there are any
                if len(explorer_df) > 1:
                    st.markdown('<p class="sub-header">Proyectos Similares</p>', unsafe_allow_html=True)
                    
                    # Find projects with the same field or technology
                    similar_projects = explorer_df[
                        (explorer_df["Ambito_Aplicacion"] == project_data["Ambito_Aplicacion"]) | 
                        (explorer_df["Tecnologia_IA"] == project_data["Tecnologia_IA"])
                    ]
                    
                    # Exclude the current project
                    similar_projects = similar_projects[similar_projects["ID_Caso"] != selected_project]
                    
                    if not similar_projects.empty:
                        st.markdown('<div style="background-color:white; padding:20px; border-radius:10px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05);">', unsafe_allow_html=True)
                        for _, proj in similar_projects.head(3).iterrows():
                            st.markdown(f"<p><b>{proj['ID_Caso']}</b> - {proj['Nombre_Caso']} ({proj['Ambito_Aplicacion']})</p>", unsafe_allow_html=True)
                        st.markdown('</div>', unsafe_allow_html=True)
                    else:
                        st.info("No se encontraron proyectos similares con los filtros actuales.")
        
    else:
        st.info("No se encontraron proyectos que cumplan con los filtros seleccionados.")

# ============================
# SECTION 6: TEMPORAL TRENDS
# ============================
elif selected == "Tendencias Temporales":
    st.markdown('<p class="main-header">Análisis de Tendencias Temporales</p>', unsafe_allow_html=True)
    
    if "Fecha_Inicio" in filtered_df.columns and pd.api.types.is_datetime64_dtype(filtered_df["Fecha_Inicio"]):
        # Extract year and month for temporal analysis
        filtered_df['Año'] = filtered_df['Fecha_Inicio'].dt.year
        filtered_df['Mes'] = filtered_df['Fecha_Inicio'].dt.month
        filtered_df['Año-Mes'] = filtered_df['Fecha_Inicio'].dt.strftime('%Y-%m')
        
        # Projects by year
        st.markdown('<p class="sub-header">Evolución Temporal de Proyectos</p>', unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            # Projects by year
            projects_by_year = filtered_df.groupby('Año').size().reset_index()
            projects_by_year.columns = ['Año', 'Proyectos']
            
            fig_yearly = px.bar(
                projects_by_year,
                x='Año',
                y='Proyectos',
                color='Proyectos',
                color_continuous_scale=px.colors.sequential.Blues,
                title="Número de Proyectos por Año"
            )
            
            fig_yearly.update_layout(
                xaxis_title="Año",
                yaxis_title="Número de Proyectos",
                height=400,
                title_font=dict(size=16, color=COLOR_AZUL_PRINCIPAL),
                paper_bgcolor="white",
                plot_bgcolor="white"
            )
            
            st.plotly_chart(fig_yearly, use_container_width=True)
        
        with col2:
            # Cumulative projects over time
            cumulative_projects = filtered_df.groupby('Año-Mes').size().reset_index()
            cumulative_projects.columns = ['Año-Mes', 'Nuevos_Proyectos']
            cumulative_projects = cumulative_projects.sort_values('Año-Mes')
            cumulative_projects['Proyectos_Acumulados'] = cumulative_projects['Nuevos_Proyectos'].cumsum()
            
            fig_cumulative = px.line(
                cumulative_projects,
                x='Año-Mes',
                y='Proyectos_Acumulados',
                markers=True,
                title="Proyectos Acumulados a lo Largo del Tiempo"
            )
            
            fig_cumulative.update_traces(line=dict(color=COLOR_AZUL_PRINCIPAL, width=3))
            
            fig_cumulative.update_layout(
                xaxis_title="Fecha",
                yaxis_title="Proyectos Acumulados",
                height=400,
                xaxis=dict(tickangle=-45),
                title_font=dict(size=16, color=COLOR_AZUL_PRINCIPAL),
                paper_bgcolor="white",
                plot_bgcolor="white"
            )
            
            st.plotly_chart(fig_cumulative, use_container_width=True)
        
        # Trends in technologies and fields over time
        st.markdown('<p class="sub-header">Tendencias en Tecnologías y Ámbitos</p>', unsafe_allow_html=True)
        
        # Technology trends
        tech_trends_option = st.radio(
            "Seleccione vista de tendencias",
            ["Tecnologías IA", "Ámbitos de Aplicación", "Riesgo"],
            horizontal=True
        )
        
        if tech_trends_option == "Tecnologías IA":
            # Top technologies
            top_techs = filtered_df['Tecnologia_IA'].value_counts().nlargest(5).index.tolist()
            
            # Filter for only the top technologies
            tech_trends_df = filtered_df[filtered_df['Tecnologia_IA'].isin(top_techs)]
            
            # Group by year and technology
            tech_by_year = tech_trends_df.groupby(['Año', 'Tecnologia_IA']).size().reset_index()
            tech_by_year.columns = ['Año', 'Tecnología', 'Proyectos']
            
            # Create line chart
            fig_tech_trends = px.line(
                tech_by_year,
                x='Año',
                y='Proyectos',
                color='Tecnología',
                markers=True,
                title="Evolución de las Principales Tecnologías IA"
            )
            
            fig_tech_trends.update_layout(
                xaxis_title="Año",
                yaxis_title="Número de Proyectos",
                height=500,
                title_font=dict(size=16, color=COLOR_AZUL_PRINCIPAL),
                paper_bgcolor="white",
                plot_bgcolor="white"
            )
            
            st.plotly_chart(fig_tech_trends, use_container_width=True)
            
        elif tech_trends_option == "Ámbitos de Aplicación":
            # Top fields
            top_fields = filtered_df['Ambito_Aplicacion'].value_counts().nlargest(5).index.tolist()
            
            # Filter for only the top fields
            field_trends_df = filtered_df[filtered_df['Ambito_Aplicacion'].isin(top_fields)]
            
            # Group by year and field
            field_by_year = field_trends_df.groupby(['Año', 'Ambito_Aplicacion']).size().reset_index()
            field_by_year.columns = ['Año', 'Ámbito', 'Proyectos']
            
            # Create line chart
            fig_field_trends = px.line(
                field_by_year,
                x='Año',
                y='Proyectos',
                color='Ámbito',
                markers=True,
                title="Evolución de los Principales Ámbitos de Aplicación"
            )
            
            fig_field_trends.update_layout(
                xaxis_title="Año",
                yaxis_title="Número de Proyectos",
                height=500,
                title_font=dict(size=16, color=COLOR_AZUL_PRINCIPAL),
                paper_bgcolor="white",
                plot_bgcolor="white"
            )
            
            st.plotly_chart(fig_field_trends, use_container_width=True)
            
        else:  # Risk trends
            # Group by year and risk level
            risk_by_year = filtered_df.groupby(['Año', 'Riesgo_IA']).size().reset_index()
            risk_by_year.columns = ['Año', 'Riesgo', 'Proyectos']
            
            # Create stacked area chart
            fig_risk_trends = px.area(
                risk_by_year,
                x='Año',
                y='Proyectos',
                color='Riesgo',
                color_discrete_map={
                    "Alto riesgo": COLOR_ACENTO,
                    "Riesgo limitado": COLOR_AZUL_SECUNDARIO,
                    "Bajo riesgo": COLOR_AZUL_CLARO,
                    "No especificado": "#CCCCCC"
                },
                title="Evolución de los Niveles de Riesgo a lo Largo del Tiempo"
            )
            
            fig_risk_trends.update_layout(
                xaxis_title="Año",
                yaxis_title="Número de Proyectos",
                height=500,
                title_font=dict(size=16, color=COLOR_AZUL_PRINCIPAL),
                paper_bgcolor="white",
                plot_bgcolor="white"
            )
            
            st.plotly_chart(fig_risk_trends, use_container_width=True)
            
            # Calculate and show risk percentage evolution
            risk_pct_by_year = filtered_df.groupby(['Año', 'Riesgo_IA']).size().reset_index()
            risk_pct_by_year.columns = ['Año', 'Riesgo', 'Proyectos']
            
            # Get total projects by year
            total_by_year = risk_pct_by_year.groupby('Año')['Proyectos'].sum().reset_index()
            total_by_year.columns = ['Año', 'Total']
            
            # Merge to calculate percentages
            risk_pct_by_year = risk_pct_by_year.merge(total_by_year, on='Año')
            risk_pct_by_year['Porcentaje'] = (risk_pct_by_year['Proyectos'] / risk_pct_by_year['Total']) * 100
            
            # Create percentage trend chart
            fig_risk_pct = px.line(
                risk_pct_by_year,
                x='Año',
                y='Porcentaje',
                color='Riesgo',
                markers=True,
                title="Evolución Porcentual de los Niveles de Riesgo"
            )
            
            fig_risk_pct.update_layout(
                xaxis_title="Año",
                yaxis_title="Porcentaje (%)",
                height=500,
                title_font=dict(size=16, color=COLOR_AZUL_PRINCIPAL),
                paper_bgcolor="white",
                plot_bgcolor="white"
            )
            
            st.plotly_chart(fig_risk_pct, use_container_width=True)
        
        # Growth rate analysis
        st.markdown('<p class="sub-header">Análisis de Tasas de Crecimiento</p>', unsafe_allow_html=True)
        
        # Calculate yearly growth rates
        yearly_growth = projects_by_year.copy()
        yearly_growth['Crecimiento'] = yearly_growth['Proyectos'].pct_change() * 100
        
        # Create bar chart for growth rates
        fig_growth = go.Figure()
        
        fig_growth.add_trace(go.Bar(
            x=yearly_growth['Año'][1:],  # Skip first year as it has no growth rate
            y=yearly_growth['Crecimiento'][1:],
            marker=dict(
                color=[COLOR_AZUL_PRINCIPAL if x >= 0 else COLOR_ACENTO for x in yearly_growth['Crecimiento'][1:]],
                line=dict(color='white', width=0.5)
            ),
            text=yearly_growth['Crecimiento'][1:].round(1).astype(str) + '%',
            textposition='auto'
        ))
        
        fig_growth.update_layout(
            title="Tasa de Crecimiento Anual de Proyectos",
            xaxis_title="Año",
            yaxis_title="Tasa de Crecimiento (%)",
            height=400,
            title_font=dict(size=16, color=COLOR_AZUL_PRINCIPAL),
            paper_bgcolor="white",
            plot_bgcolor="white"
        )
        
        st.plotly_chart(fig_growth, use_container_width=True)
        
    # Alto Riesgo indicator (this seems to be a fragment in your code)
    alto_riesgo = filtered_df[filtered_df["Riesgo_IA"] == "Alto riesgo"].shape[0]
    porcentaje = int((alto_riesgo / len(filtered_df)) * 100) if len(filtered_df) > 0 else 0
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(f'<p class="metric-value">{alto_riesgo} ({porcentaje}%)</p>', unsafe_allow_html=True)
    st.markdown('<p class="metric-label">Proyectos de Alto Riesgo</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
       
    # Main graphs - Distribution by risk and field
    st.markdown('<p class="sub-header">Distribución Principal de Proyectos</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # Donut chart of distribution by risk level
        fig_riesgo = go.Figure()
        
        riesgo_counts = filtered_df["Riesgo_IA"].value_counts().reset_index()
        riesgo_counts.columns = ["Riesgo", "Cantidad"]
        
        colores_riesgo = {
            "Alto riesgo": COLOR_ACENTO,
            "Riesgo limitado": COLOR_AZUL_SECUNDARIO,
            "Bajo riesgo": COLOR_AZUL_CLARO,
            "No especificado": "#CCCCCC"
        }
        
        colores = [colores_riesgo.get(riesgo, COLOR_AZUL_PRINCIPAL) for riesgo in riesgo_counts["Riesgo"]]
        
        fig_riesgo.add_trace(go.Pie(
            labels=riesgo_counts["Riesgo"],
            values=riesgo_counts["Cantidad"],
            hole=0.5,
            marker=dict(colors=colores),
            textinfo='percent+label',
            insidetextorientation='radial',
            textposition='outside',
            textfont=dict(color=COLOR_TEXTO, size=12),
            pull=[0.05 if r == "Alto riesgo" else 0 for r in riesgo_counts["Riesgo"]]
        ))
        
        fig_riesgo.update_layout(
            title="Distribución por Nivel de Riesgo IA",
            title_font=dict(size=16, color=COLOR_AZUL_PRINCIPAL),
            legend=dict(orientation="h", y=-0.1),
            margin=dict(t=50, b=20, l=20, r=20),
            height=350,
            paper_bgcolor="white",
            plot_bgcolor="white"
        )
        
        st.plotly_chart(fig_riesgo, use_container_width=True)
    
    with col2:
        # Horizontal bar chart for application fields
        ambitos_counts = filtered_df["Ambito_Aplicacion"].value_counts().nlargest(10).reset_index()
        ambitos_counts.columns = ["Ambito", "Cantidad"]
        
        fig_ambitos = go.Figure()
        
        fig_ambitos.add_trace(go.Bar(
            y=ambitos_counts["Ambito"],
            x=ambitos_counts["Cantidad"],
            orientation='h',
            marker=dict(
                color=COLOR_AZUL_PRINCIPAL,
                line=dict(color=COLOR_AZUL_SECUNDARIO, width=1)
            ),
            text=ambitos_counts["Cantidad"],
            textposition='auto',
        ))
        
        # AQUÍ ESTÁ LA PARTE CORREGIDA
        fig_ambitos.update_layout(
            title="Top 10 Ámbitos de Aplicación",
            title_font=dict(size=16, color=COLOR_AZUL_PRINCIPAL),
            xaxis=dict(
                title=dict(
                    text="Número de Proyectos",
                    font=dict(color=COLOR_TEXTO)
                ),
                tickfont=dict(color=COLOR_TEXTO),
                showgrid=True,
                gridcolor='#F0F0F0'
            ),
            yaxis=dict(
                title=None,
                tickfont=dict(color=COLOR_TEXTO),
                automargin=True
            ),
            margin=dict(t=50, b=20, l=20, r=20),
            height=350,
            paper_bgcolor="white",
            plot_bgcolor="white"
        )
        
        st.plotly_chart(fig_ambitos, use_container_width=True)
    
    # Lower graphs - Technologies and Autonomous Communities
    st.markdown('<p class="sub-header">Distribución Geográfica y Tecnológica</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # Distribution by autonomous communities
        ccaa_counts = filtered_df["Comunidad_Autonoma"].value_counts().reset_index()
        ccaa_counts.columns = ["Comunidad Autonoma", "Cantidad"]
        
        # Simple heat map 
        fig_ccaa = px.bar(
            ccaa_counts.sort_values("Cantidad", ascending=True).tail(10),
            y="Comunidad Autonoma",
            x="Cantidad",
            orientation='h',
            color="Cantidad",
            color_continuous_scale=px.colors.sequential.Blues,
            title="Distribución por Comunidad Autónoma (Top 10)"
        )
        
        # CORRECCIÓN PARA ESTA VISUALIZACIÓN TAMBIÉN 
        fig_ccaa.update_layout(
            title_font=dict(size=16, color=COLOR_AZUL_PRINCIPAL),
            xaxis=dict(
                title=dict(
                    text="Número de Proyectos",
                    font=dict(color=COLOR_TEXTO)
                )
            ),
            yaxis=dict(title=None, automargin=True),
            margin=dict(t=50, b=20, l=20, r=20),
            height=400,
            paper_bgcolor="white",
            plot_bgcolor="white"
        )
        
        st.plotly_chart(fig_ccaa, use_container_width=True)
       
# ============================
# SECTION 7: PREDICTIVE ANALYSIS
# ============================
elif selected == "Análisis Predictivo":
    st.markdown('<p class="main-header">Análisis Predictivo de Proyectos IA</p>', unsafe_allow_html=True)
    
    if "Fecha_Inicio" in filtered_df.columns and pd.api.types.is_datetime64_dtype(filtered_df["Fecha_Inicio"]):
        # Extract year and month for temporal analysis
        filtered_df['Año'] = filtered_df['Fecha_Inicio'].dt.year
        filtered_df['Mes'] = filtered_df['Fecha_Inicio'].dt.month
        
        # Create time-based features
        st.markdown('<p class="sub-header">Predicción de Crecimiento y Tendencias</p>', unsafe_allow_html=True)
        
        # Group by year to show historical growth
        projects_by_year = filtered_df.groupby('Año').size().reset_index()
        projects_by_year.columns = ['Año', 'Proyectos']
        
        # Simple linear regression for prediction
        X = projects_by_year[['Año']]
        y = projects_by_year['Proyectos']
        
        model = LinearRegression()
        model.fit(X, y)
        
        # Generate future years for prediction
        current_year = filtered_df['Año'].max()
        future_years = pd.DataFrame({'Año': range(current_year + 1, current_year + 6)})
        
        # Make predictions
        future_predictions = model.predict(future_years)
        future_predictions = np.maximum(future_predictions, 0)  # Ensure no negative predictions
        
        # Create DataFrame with historical and predicted data
        historical = projects_by_year.copy()
        historical['Tipo'] = 'Histórico'
        
        predicted = pd.DataFrame({
            'Año': future_years['Año'],
            'Proyectos': future_predictions.round().astype(int),
            'Tipo': 'Predicción'
        })
        
        combined_data = pd.concat([historical, predicted])
        
        # Create line chart with historical and predicted data
        fig_prediction = px.line(
            combined_data,
            x='Año',
            y='Proyectos',
            color='Tipo',
            symbols='Tipo',
            title="Predicción de Crecimiento de Proyectos IA",
            color_discrete_map={
                'Histórico': COLOR_AZUL_PRINCIPAL,
                'Predicción': COLOR_ACENTO
            }
        )
        
        fig_prediction.update_traces(mode='lines+markers')
        
        # Add confidence interval (simple approach)
        residuals = y - model.predict(X)
        prediction_error = residuals.std()
        
        for i, year in enumerate(future_years['Año']):
            fig_prediction.add_trace(go.Scatter(
                x=[year, year],
                y=[
                    max(0, future_predictions[i] - 1.96 * prediction_error),
                    future_predictions[i] + 1.96 * prediction_error
                ],
                mode='lines',
                line=dict(color=COLOR_ACENTO, width=1, dash='dash'),
                showlegend=False
            ))
        
        fig_prediction.update_layout(
            xaxis_title="Año",
            yaxis_title="Número de Proyectos",
            height=500,
            title_font=dict(size=16, color=COLOR_AZUL_PRINCIPAL),
            paper_bgcolor="white",
            plot_bgcolor="white"
        )
        
        st.plotly_chart(fig_prediction, use_container_width=True)
        
        # Risk evolution prediction
        st.markdown('<p class="sub-header">Evolución Prevista de Riesgos</p>', unsafe_allow_html=True)
        
        # Group by year and risk
        risk_by_year = filtered_df.groupby(['Año', 'Riesgo_IA']).size().reset_index()
        risk_by_year.columns = ['Año', 'Riesgo', 'Proyectos']
        
        # Pivot to get risk levels as columns
        risk_pivot = risk_by_year.pivot(index='Año', columns='Riesgo', values='Proyectos').fillna(0)
        
        # Create a model for each risk level
        prediction_years = range(current_year + 1, current_year + 4)
        risk_predictions = {}
        
        for risk in risk_pivot.columns:
            # Create and train model
            risk_model = LinearRegression()
            risk_X = np.array(risk_pivot.index).reshape(-1, 1)
            risk_y = risk_pivot[risk].values
            
            risk_model.fit(risk_X, risk_y)
            
            # Make predictions
            risk_future = risk_model.predict(np.array(prediction_years).reshape(-1, 1))
            risk_future = np.maximum(risk_future, 0)  # Ensure no negative predictions
            
            risk_predictions[risk] = risk_future
        
        # Create DataFrame with predictions
        risk_prediction_data = []
        
        for i, year in enumerate(prediction_years):
            for risk, values in risk_predictions.items():
                risk_prediction_data.append({
                    'Año': year,
                    'Riesgo': risk,
                    'Proyectos': int(values[i]),
                    'Tipo': 'Predicción'
                })
        
        # Add historical data
        for _, row in risk_by_year.iterrows():
            risk_prediction_data.append({
                'Año': row['Año'],
                'Riesgo': row['Riesgo'],
                'Proyectos': row['Proyectos'],
                'Tipo': 'Histórico'
            })
        
        risk_prediction_df = pd.DataFrame(risk_prediction_data)
        
        # Create stacked bar chart
        fig_risk_prediction = px.bar(
            risk_prediction_df,
            x='Año',
            y='Proyectos',
            color='Riesgo',
            pattern_shape='Tipo',
            barmode='stack',
            color_discrete_map={
                "Alto riesgo": COLOR_ACENTO,
                "Riesgo limitado": COLOR_AZUL_SECUNDARIO,
                "Bajo riesgo": COLOR_AZUL_CLARO,
                "No especificado": "#CCCCCC"
            },
            title="Predicción de Evolución de Niveles de Riesgo"
        )
        
        fig_risk_prediction.update_layout(
            xaxis_title="Año",
            yaxis_title="Número de Proyectos",
            height=500,
            title_font=dict(size=16, color=COLOR_AZUL_PRINCIPAL),
            paper_bgcolor="white",
            plot_bgcolor="white"
        )
        
        st.plotly_chart(fig_risk_prediction, use_container_width=True)
        
        # Technology adoption prediction
        st.markdown('<p class="sub-header">Predicción de Adopción de Tecnologías</p>', unsafe_allow_html=True)
        
        # Select top technologies for prediction
        top_techs = filtered_df['Tecnologia_IA'].value_counts().nlargest(5).index.tolist()
        
        # Create selection for technology to predict
        selected_tech = st.selectbox(
            "Seleccione una tecnología para analizar su tendencia",
            options=top_techs
        )
        
        if selected_tech:
            # Filter data for selected technology
            tech_data = filtered_df[filtered_df['Tecnologia_IA'] == selected_tech]
            
            # Group by year
            tech_by_year = tech_data.groupby('Año').size().reset_index()
            tech_by_year.columns = ['Año', 'Proyectos']
            
            # Fill missing years with zeros
            all_years = pd.DataFrame({'Año': range(filtered_df['Año'].min(), filtered_df['Año'].max() + 1)})
            tech_by_year = all_years.merge(tech_by_year, on='Año', how='left').fillna(0)
            
            # Train model
            tech_X = tech_by_year[['Año']]
            tech_y = tech_by_year['Proyectos']
            
            tech_model = LinearRegression()
            tech_model.fit(tech_X, tech_y)
            
            # Generate future years for prediction
            tech_future_years = pd.DataFrame({'Año': range(current_year + 1, current_year + 6)})
            
            # Make predictions
            tech_future_predictions = tech_model.predict(tech_future_years)
            tech_future_predictions = np.maximum(tech_future_predictions, 0)  # Ensure no negative predictions
            
            # Create DataFrame with historical and predicted data
            tech_historical = tech_by_year.copy()
            tech_historical['Tipo'] = 'Histórico'
            
            tech_predicted = pd.DataFrame({
                'Año': tech_future_years['Año'],
                'Proyectos': tech_future_predictions.round().astype(int),
                'Tipo': 'Predicción'
            })
            
            tech_combined_data = pd.concat([tech_historical, tech_predicted])
            
            # Create line chart with historical and predicted data
            fig_tech_prediction = px.line(
                tech_combined_data,
                x='Año',
                y='Proyectos',
                color='Tipo',
                symbols='Tipo',
                title=f"Predicción de Adopción: {selected_tech}",
                color_discrete_map={
                    'Histórico': COLOR_AZUL_PRINCIPAL,
                    'Predicción': COLOR_ACENTO
                }
            )
            
            fig_tech_prediction.update_traces(mode='lines+markers')
            
            fig_tech_prediction.update_layout(
                xaxis_title="Año",
                yaxis_title="Número de Proyectos",
                height=500,
                title_font=dict(size=16, color=COLOR_AZUL_PRINCIPAL),
                paper_bgcolor="white",
                plot_bgcolor="white"
            )
            
            st.plotly_chart(fig_tech_prediction, use_container_width=True)
            
            # Add growth rate annotation
            if len(tech_predicted) > 0:
                current_value = tech_historical[tech_historical['Año'] == current_year]['Proyectos'].values[0]
                future_value = tech_predicted[tech_predicted['Año'] == current_year + 5]['Proyectos'].values[0]
                
                if current_value > 0:
                    growth_rate = ((future_value / current_value) ** (1/5) - 1) * 100
                    st.markdown(f"""
                    <div style='background-color:white; padding:15px; border-radius:10px; margin-bottom:20px;'>
                        <h4 style='color:{COLOR_AZUL_PRINCIPAL}; margin-bottom:10px;'>Análisis de Tendencia</h4>
                        <p>La tecnología <b>{selected_tech}</b> muestra una tasa de crecimiento anual compuesta (CAGR) 
                        estimada del <b>{growth_rate:.1f}%</b> para los próximos 5 años.</p>
                        <p>Proyectos actuales (estimados): <b>{current_value}</b></p>
                        <p>Proyectos estimados en {current_year + 5}: <b>{future_value}</b></p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.info(f"La tecnología {selected_tech} es emergente y no tiene suficientes datos históricos para un análisis de crecimiento preciso.")
    
    else:
        st.warning("No hay información de fecha disponible en los datos para realizar análisis predictivos.")

# ============================
# SECTION 8: SCENARIO SIMULATOR
# ============================
elif selected == "Simulador de Escenarios":
    st.markdown('<p class="main-header">Simulador de Escenarios</p>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style='background-color:white; padding:20px; border-radius:10px; margin-bottom:20px;'>
        <h3 style='color:#0D47A1;'>Simulador de Adopción de IA en el Sector Sanitario</h3>
        <p>Esta herramienta permite simular diferentes escenarios de adopción de tecnologías IA 
        en el sector sanitario, visualizando su impacto potencial en términos de implementación, 
        riesgos y ámbitos de aplicación.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Scenario parameters
    st.markdown('<p class="sub-header">Parámetros del Escenario</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        growth_rate = st.slider(
            "Tasa de crecimiento anual de proyectos (%)",
            min_value=-20,
            max_value=50,
            value=15,
            step=5
        )
        
        high_risk_ratio = st.slider(
            "Proporción de proyectos de alto riesgo (%)",
            min_value=0,
            max_value=100,
            value=int(filtered_df[filtered_df["Riesgo_IA"] == "Alto riesgo"].shape[0] / len(filtered_df) * 100) if len(filtered_df) > 0 else 40,
            step=5
        )
    
    with col2:
        years_to_simulate = st.slider(
            "Años a simular",
            min_value=1,
            max_value=10,
            value=5
        )
        
        primary_tech = st.selectbox(
            "Tecnología dominante",
            options=filtered_df["Tecnologia_IA"].value_counts().nlargest(10).index.tolist()
        )
    
    # Current year stats
    current_year = pd.to_datetime('today').year
    current_projects = len(filtered_df)
    
    # Simulate future growth
    scenario_data = []
    
    # Starting values
    yearly_projects = current_projects
    
    # Risk distribution (use current distribution or user-specified high risk)
    risk_distribution = filtered_df["Riesgo_IA"].value_counts(normalize=True)
    
    # Adjust high risk ratio based on user input
    current_high_risk = risk_distribution.get("Alto riesgo", 0) * 100
    adjustment_factor = high_risk_ratio / current_high_risk if current_high_risk > 0 else 0
    
    adjusted_risk = risk_distribution.copy()
    
    if adjustment_factor > 0:
        # Adjust high risk up or down
        adjusted_risk["Alto riesgo"] = high_risk_ratio / 100
        
        # Distribute remaining probability proportionally among other risk levels
        other_risks = [r for r in adjusted_risk.index if r != "Alto riesgo"]
        other_sum = sum([adjusted_risk[r] for r in other_risks])
        
        if other_sum > 0:  # Avoid division by zero
            remaining_prob = 1 - adjusted_risk["Alto riesgo"]
            for risk in other_risks:
                adjusted_risk[risk] = adjusted_risk[risk] / other_sum * remaining_prob
    
    # Technology adoption trend (sigmoid pattern)
    def sigmoid(x, k=0.5):
        return 1 / (1 + np.exp(-k * x))
    
    # Generate scenario data
    for year in range(1, years_to_simulate + 1):
        # Calculate growth for the year
        yearly_projects = int(yearly_projects * (1 + growth_rate / 100))
        
        # Simulate tech adoption (sigmoid curve)
        tech_adoption_factor = sigmoid(year / years_to_simulate * 4 - 2)
        
        # Current tech distribution
        tech_distribution = filtered_df["Tecnologia_IA"].value_counts(normalize=True)
        
        # Adjust distribution to favor primary technology over time
        primary_tech_current = tech_distribution.get(primary_tech, 0.1)
        primary_tech_target = min(0.6, primary_tech_current + 0.5 * tech_adoption_factor)
        
        # Risk distribution for each year (may change over time)
        yearly_high_risk = adjusted_risk.get("Alto riesgo", 0.4)
        
        scenario_data.append({
            "Año": current_year + year,
            "Proyectos": yearly_projects,
            "Adopción Tecnología Principal": primary_tech_target * 100,
            "Proyectos Alto Riesgo": int(yearly_projects * yearly_high_risk),
            "% Alto Riesgo": yearly_high_risk * 100
        })
    
    scenario_df = pd.DataFrame(scenario_data)
    
    # Show simulation results
    st.markdown('<p class="sub-header">Resultados de la Simulación</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Project growth chart
        fig_growth = px.line(
            scenario_df,
            x="Año",
            y="Proyectos",
            markers=True,
            title="Proyección de Crecimiento de Proyectos"
        )
        
        fig_growth.update_traces(line=dict(color=COLOR_AZUL_PRINCIPAL, width=3))
        
        fig_growth.update_layout(
            xaxis_title="Año",
            yaxis_title="Número de Proyectos",
            height=400,
            title_font=dict(size=16, color=COLOR_AZUL_PRINCIPAL),
            paper_bgcolor="white",
            plot_bgcolor="white"
        )
        
        st.plotly_chart(fig_growth, use_container_width=True)
    
    with col2:
        # Summary card
        st.markdown('<div style="background-color:white; padding:20px; border-radius:10px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05);">', unsafe_allow_html=True)
        st.markdown(f"<h3 style='color:{COLOR_AZUL_PRINCIPAL};'>Resumen del Escenario</h3>", unsafe_allow_html=True)
        
        final_year = scenario_df.iloc[-1]
        
        st.markdown(f"""
        <p><b>Proyectos actuales:</b> {current_projects}</p>
        <p><b>Proyectos en {final_year['Año']}:</b> {final_year['Proyectos']}</p>
        <p><b>Crecimiento total:</b> {((final_year['Proyectos'] / current_projects) - 1) * 100:.1f}%</p>
        <p><b>Penetración de {primary_tech}:</b> {final_year['Adopción Tecnología Principal']:.1f}%</p>
        <p><b>Proyectos de alto riesgo en {final_year['Año']}:</b> {final_year['Proyectos Alto Riesgo']} ({final_year['% Alto Riesgo']:.1f}%)</p>
        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Risk evolution
    st.markdown('<p class="sub-header">Evolución de Riesgos en el Escenario</p>', unsafe_allow_html=True)
    
    # Risk projection
    risk_projection = []
    
    # Copy risk distribution
    risk_levels = list(adjusted_risk.index)
    
    for i, row in scenario_df.iterrows():
        year = row['Año']
        total_projects = row['Proyectos']
        
        for risk in risk_levels:
            # Calculate number of projects for this risk level
            if risk == "Alto riesgo":
                risk_ratio = row['% Alto Riesgo'] / 100
            else:
                risk_ratio = adjusted_risk[risk]
            
            risk_projection.append({
                "Año": year,
                "Riesgo": risk,
                "Proyectos": int(total_projects * risk_ratio)
            })
    
    risk_projection_df = pd.DataFrame(risk_projection)
    
    # Stacked area chart for risk evolution
    fig_risk_evolution = px.area(
        risk_projection_df,
        x="Año",
        y="Proyectos",
        color="Riesgo",
        color_discrete_map={
            "Alto riesgo": COLOR_ACENTO,
            "Riesgo limitado": COLOR_AZUL_SECUNDARIO,
            "Bajo riesgo": COLOR_AZUL_CLARO,
            "No especificado": "#CCCCCC"
        },
        title="Evolución Proyectada de Niveles de Riesgo"
    )
    
    fig_risk_evolution.update_layout(
        xaxis_title="Año",
        yaxis_title="Número de Proyectos",
        height=450,
        title_font=dict(size=16, color=COLOR_AZUL_PRINCIPAL),
        paper_bgcolor="white",
        plot_bgcolor="white"
    )
    
    st.plotly_chart(fig_risk_evolution, use_container_width=True)
    
    # Technology adoption scenario
    st.markdown('<p class="sub-header">Escenario de Adopción Tecnológica</p>', unsafe_allow_html=True)
    
    # Technology distribution for the scenario
    tech_distribution = filtered_df["Tecnologia_IA"].value_counts(normalize=True)
    top_techs = tech_distribution.nlargest(5)
    
    # Adjust over time with primary technology gaining share
    tech_scenario = []
    
    for i, row in scenario_df.iterrows():
        year = row['Año']
        total_projects = row['Proyectos']
        primary_tech_share = row['Adopción Tecnología Principal'] / 100
        
        # Remaining share for other techs
        remaining_share = 1 - primary_tech_share
        other_techs_total = sum([v for k, v in top_techs.items() if k != primary_tech])
        
        for tech, current_share in top_techs.items():
            if tech == primary_tech:
                tech_projects = int(total_projects * primary_tech_share)
            else:
                # Distribute remaining share proportionally among other techs
                adjusted_share = current_share / other_techs_total * remaining_share if other_techs_total > 0 else 0
                tech_projects = int(total_projects * adjusted_share)
            
            tech_scenario.append({
                "Año": year,
                "Tecnología": tech,
                "Proyectos": tech_projects
            })
    
    tech_scenario_df = pd.DataFrame(tech_scenario)
    
    # Create area chart for technology adoption
    fig_tech_scenario = px.area(
        tech_scenario_df,
        x="Año",
        y="Proyectos",
        color="Tecnología",
        color_discrete_sequence=COLOR_PALETA,
        title="Escenario de Adopción Tecnológica"
    )
    
    fig_tech_scenario.update_layout(
        xaxis_title="Año",
        yaxis_title="Número de Proyectos",
        height=450,
        title_font=dict(size=16, color=COLOR_AZUL_PRINCIPAL),
        paper_bgcolor="white",
        plot_bgcolor="white"
    )
    
    st.plotly_chart(fig_tech_scenario, use_container_width=True)
    
    # Add impact assessment
    st.markdown('<p class="sub-header">Evaluación de Impacto</p>', unsafe_allow_html=True)
    
    # Calculate some impact metrics
    final_projects = scenario_df.iloc[-1]['Proyectos']
    high_risk_growth = (scenario_df.iloc[-1]['Proyectos Alto Riesgo'] / (current_projects * adjusted_risk.get("Alto riesgo", 0.4))) - 1
    
    # Create metric cards for impact assessment
    col1, col2, col3 = st.columns(3)
    
    with col1:
        growth_color = COLOR_AZUL_PRINCIPAL if growth_rate >= 0 else COLOR_ACENTO
        st.markdown(f"""
        <div style='background-color:white; padding:20px; border-radius:10px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05);'>
            <h4 style='color:{COLOR_AZUL_PRINCIPAL}; margin-bottom:10px;'>Impacto en Volumen</h4>
            <p style='font-size:2rem; font-weight:bold; color:{growth_color};'>{final_projects - current_projects}</p>
            <p>Nuevos proyectos estimados</p>
            <p>Tasa de crecimiento anual: <b>{growth_rate}%</b></p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        risk_color = COLOR_ACENTO if high_risk_ratio > 40 else (COLOR_AZUL_SECUNDARIO if high_risk_ratio > 20 else COLOR_AZUL_CLARO)
        st.markdown(f"""
        <div style='background-color:white; padding:20px; border-radius:10px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05);'>
            <h4 style='color:{COLOR_AZUL_PRINCIPAL}; margin-bottom:10px;'>Impacto en Riesgo</h4>
            <p style='font-size:2rem; font-weight:bold; color:{risk_color};'>{high_risk_ratio}%</p>
            <p>Proporción de alto riesgo</p>
            <p>Crecimiento de alto riesgo: <b>{high_risk_growth * 100:.1f}%</b></p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        tech_color = COLOR_AZUL_PRINCIPAL
        st.markdown(f"""
        <div style='background-color:white; padding:20px; border-radius:10px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05);'>
            <h4 style='color:{COLOR_AZUL_PRINCIPAL}; margin-bottom:10px;'>Impacto Tecnológico</h4>
            <p style='font-size:2rem; font-weight:bold; color:{tech_color};'>{primary_tech}</p>
            <p>Tecnología dominante</p>
            <p>Adopción final: <b>{scenario_df.iloc[-1]['Adopción Tecnología Principal']:.1f}%</b></p>
        </div>
        """, unsafe_allow_html=True)
    
    # Recommendations based on scenario
    st.markdown('<p class="sub-header">Recomendaciones Estratégicas</p>', unsafe_allow_html=True)
    
    # Generate recommendations based on scenario parameters
    recommendations = []
    
    if growth_rate > 30:
        recommendations.append("Establecer un **marco regulatorio robusto** para gestionar el rápido crecimiento de proyectos IA en sanidad.")
    elif growth_rate < 0:
        recommendations.append("Implementar **incentivos y programas de apoyo** para reactivar la adopción de IA en el sector sanitario.")
    else:
        recommendations.append("Mantener un **seguimiento continuo** del desarrollo de proyectos IA para garantizar un crecimiento sostenible.")
    
    if high_risk_ratio > 50:
        recommendations.append("Priorizar la **evaluación de riesgos y sistemas de supervisión** dado el alto porcentaje de proyectos de alto riesgo.")
    elif high_risk_ratio > 30:
        recommendations.append("Balancear la innovación con mecanismos de **auditoría de algoritmos** para gestionar proyectos de alto riesgo.")
    else:
        recommendations.append("Promover la **adopción de buenas prácticas** para mantener niveles de riesgo controlados.")
    
    if years_to_simulate <= 3:
        recommendations.append("Desarrollar un **plan estratégico a corto plazo** que permita adaptarse rápidamente a los cambios tecnológicos.")
    else:
        recommendations.append("Establecer una **visión estratégica a largo plazo** con hitos intermedios para evaluar el progreso.")
    
    # Display recommendations
    st.markdown('<div style="background-color:white; padding:20px; border-radius:10px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05);">', unsafe_allow_html=True)
    st.markdown(f"<h3 style='color:{COLOR_AZUL_PRINCIPAL};'>Recomendaciones basadas en el Escenario</h3>", unsafe_allow_html=True)
    
    for i, rec in enumerate(recommendations, 1):
        st.markdown(f"<p><b>{i}.</b> {rec}</p>", unsafe_allow_html=True)
    
        st.markdown('<p><i>Nota: Estas recomendaciones son generadas automáticamente en base a los parámetros del escenario y deben ser evaluadas por expertos.</i></p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
