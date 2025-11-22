"""
XRSK Platform - Styles CSS avancés
Style inspiré ASXN - Clean, serif, professional
"""

XRSK_CSS = """
<style>
    /* ============================================
       FONTS - Import Google Fonts
       ============================================ */
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Inter:wght@300;400;500;600&display=swap');

    /* ============================================
       GLOBAL - Reset Streamlit
       ============================================ */
    
    /* Cache menu Streamlit et footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Cache sidebar pour navigation horizontale */
    [data-testid="stSidebar"] {
        display: none;
    }
    
    /* Background général */
    .stApp {
        background-color: #FAFAFA;
    }
    
    /* Container principal */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1400px;
        margin: 0 auto;
    }
    
    /* ============================================
       NAVIGATION - Horizontal navbar style ASXN
       ============================================ */
    
    .xrsk-navbar {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        background: white;
        border-bottom: 1px solid #E8E8E8;
        padding: 1.2rem 2rem;
        z-index: 999;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }
    
    .xrsk-navbar h1 {
        font-family: 'Playfair Display', serif;
        font-size: 1.8rem;
        font-weight: 700;
        color: #1F4E78;
        margin: 0;
        display: inline-block;
    }
    
    .xrsk-navbar-links {
        float: right;
        margin-top: 0.5rem;
    }
    
    .xrsk-navbar-links a {
        font-family: 'Inter', sans-serif;
        font-size: 0.95rem;
        color: #2C3E50;
        text-decoration: none;
        margin-left: 2rem;
        transition: color 0.2s;
    }
    
    .xrsk-navbar-links a:hover {
        color: #1F4E78;
    }
    
    /* ============================================
       TYPOGRAPHY - Style ASXN serif
       ============================================ */
    
    /* Titres principaux */
    h1 {
        font-family: 'Playfair Display', serif !important;
        font-weight: 700 !important;
        color: #1F4E78 !important;
        font-size: 2.8rem !important;
        margin-bottom: 0.5rem !important;
        letter-spacing: -0.02em !important;
    }
    
    h2 {
        font-family: 'Playfair Display', serif !important;
        font-weight: 600 !important;
        color: #2C3E50 !important;
        font-size: 2rem !important;
        margin-top: 2.5rem !important;
        margin-bottom: 1rem !important;
    }
    
    h3 {
        font-family: 'Playfair Display', serif !important;
        font-weight: 600 !important;
        color: #2C3E50 !important;
        font-size: 1.5rem !important;
        margin-top: 2rem !important;
    }
    
    /* Corps de texte */
    p, .stMarkdown {
        font-family: 'Inter', sans-serif !important;
        font-size: 1rem !important;
        line-height: 1.7 !important;
        color: #444 !important;
    }
    
    /* Baseline sous titre principal */
    .xrsk-baseline {
        font-family: 'Inter', sans-serif;
        font-size: 1.1rem;
        color: #666;
        font-weight: 300;
        margin-bottom: 2rem;
    }
    
    /* ============================================
       METRICS - Style ASXN clean
       ============================================ */
    
    [data-testid="stMetricValue"] {
        font-family: 'Playfair Display', serif !important;
        font-size: 2.2rem !important;
        font-weight: 700 !important;
        color: #1F4E78 !important;
    }
    
    [data-testid="stMetricLabel"] {
        font-family: 'Inter', sans-serif !important;
        font-size: 0.85rem !important;
        font-weight: 500 !important;
        color: #666 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
    }
    
    [data-testid="stMetricDelta"] {
        font-family: 'Inter', sans-serif !important;
        font-size: 0.8rem !important;
    }
    
    /* Cartes métriques */
    [data-testid="metric-container"] {
        background: white;
        padding: 1.5rem;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        border: 1px solid #F0F0F0;
    }
    
    /* ============================================
       BUTTONS - Style subtil
       ============================================ */
    
    .stButton > button {
        font-family: 'Inter', sans-serif !important;
        font-weight: 500 !important;
        border-radius: 6px !important;
        border: 1px solid #1F4E78 !important;
        background-color: white !important;
        color: #1F4E78 !important;
        padding: 0.5rem 1.5rem !important;
        transition: all 0.2s !important;
    }
    
    .stButton > button:hover {
        background-color: #1F4E78 !important;
        color: white !important;
    }
    
    .stDownloadButton > button {
        font-family: 'Inter', sans-serif !important;
        background-color: #1F4E78 !important;
        color: white !important;
        border: none !important;
        border-radius: 6px !important;
        padding: 0.5rem 1.5rem !important;
    }
    
    /* ============================================
       DATAFRAMES - Tables propres
       ============================================ */
    
    [data-testid="stDataFrame"] {
        font-family: 'Inter', sans-serif !important;
    }
    
    [data-testid="stDataFrame"] th {
        background-color: #F8F9FA !important;
        color: #2C3E50 !important;
        font-weight: 600 !important;
        font-size: 0.85rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
        padding: 1rem !important;
        border-bottom: 2px solid #1F4E78 !important;
    }
    
    [data-testid="stDataFrame"] td {
        font-size: 0.95rem !important;
        padding: 0.8rem 1rem !important;
        border-bottom: 1px solid #F0F0F0 !important;
    }
    
    /* ============================================
       TABS - Style clean
       ============================================ */
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
        border-bottom: 1px solid #E8E8E8;
    }
    
    .stTabs [data-baseweb="tab"] {
        font-family: 'Inter', sans-serif !important;
        font-weight: 500 !important;
        font-size: 1rem !important;
        color: #666 !important;
        padding: 0.8rem 0 !important;
        background-color: transparent !important;
        border: none !important;
    }
    
    .stTabs [aria-selected="true"] {
        color: #1F4E78 !important;
        border-bottom: 2px solid #1F4E78 !important;
    }
    
    /* ============================================
       DIVIDERS - Séparateurs subtils
       ============================================ */
    
    hr {
        margin: 2.5rem 0 !important;
        border: none !important;
        border-top: 1px solid #E8E8E8 !important;
    }
    
    /* ============================================
       ALERTS - Messages stylisés
       ============================================ */
    
    .stAlert {
        font-family: 'Inter', sans-serif !important;
        border-radius: 8px !important;
        border-left: 4px solid #1F4E78 !important;
        padding: 1rem 1.2rem !important;
    }
    
    [data-testid="stMarkdownContainer"] > .stAlert {
        background-color: #F8F9FA !important;
    }
    
    /* ============================================
       EXPANDERS - Accordéons propres
       ============================================ */
    
    .streamlit-expanderHeader {
        font-family: 'Inter', sans-serif !important;
        font-weight: 500 !important;
        color: #2C3E50 !important;
        background-color: #F8F9FA !important;
        border-radius: 6px !important;
    }
    
    /* ============================================
       CHARTS - Plotly customization
       ============================================ */
    
    .js-plotly-plot {
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    }
    
    /* ============================================
       SPACING - Espacement ASXN-like
       ============================================ */
    
    .element-container {
        margin-bottom: 1.5rem;
    }
    
    /* Colonnes avec espacement */
    [data-testid="column"] {
        padding: 0 1rem;
    }
    
    /* ============================================
       CARDS - Conteneurs stylisés
       ============================================ */
    
    .xrsk-card {
        background: white;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.08);
        border: 1px solid #F0F0F0;
        margin-bottom: 2rem;
    }
    
    /* ============================================
       FOOTER - Pied de page discret
       ============================================ */
    
    .xrsk-footer {
        margin-top: 4rem;
        padding: 2rem 0;
        border-top: 1px solid #E8E8E8;
        text-align: center;
        font-family: 'Inter', sans-serif;
        font-size: 0.85rem;
        color: #999;
    }
    
    /* ============================================
       RESPONSIVE - Mobile friendly
       ============================================ */
    
    @media (max-width: 768px) {
        .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }
        
        h1 {
            font-size: 2rem !important;
        }
        
        .xrsk-navbar h1 {
            font-size: 1.3rem;
        }
        
        .xrsk-navbar-links {
            display: none;
        }
    }
</style>
"""

# Fonction helper pour appliquer le CSS
def apply_xrsk_styles():
    """Applique les styles XRSK à la page Streamlit"""
    import streamlit as st
    st.markdown(XRSK_CSS, unsafe_allow_html=True)
