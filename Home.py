"""
XRSK Platform - Dashboard principal
Style ASXN - Clean & Professional
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
from backend.collectors.defillama import DefiLlamaCollector

# Configuration de la page
st.set_page_config(
    page_title="XRSK Platform - Cross-Chain Risk Intelligence",
    page_icon="🔗",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================
# STYLES CSS AVANCÉS - ASXN-INSPIRED
# ============================================

XRSK_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Inter:wght@300;400;500;600&display=swap');
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    [data-testid="stSidebar"] {display: none;}
    
    .stApp {background-color: #FAFAFA;}
    
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1400px;
        margin: 0 auto;
    }
    
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
    }
    
    p, .stMarkdown {
        font-family: 'Inter', sans-serif !important;
        font-size: 1rem !important;
        line-height: 1.7 !important;
        color: #444 !important;
    }
    
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
    
    [data-testid="metric-container"] {
        background: white;
        padding: 1.5rem;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        border: 1px solid #F0F0F0;
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
    
    hr {
        margin: 2.5rem 0 !important;
        border: none !important;
        border-top: 1px solid #E8E8E8 !important;
    }
    
    .xrsk-baseline {
        font-family: 'Inter', sans-serif;
        font-size: 1.1rem;
        color: #666;
        font-weight: 300;
        margin-bottom: 2rem;
    }
</style>
"""

st.markdown(XRSK_CSS, unsafe_allow_html=True)

# ============================================
# HEADER
# ============================================

st.title("🔗 XRSK Platform")
st.markdown('<p class="xrsk-baseline"><strong>Cross-Chain Risk Intelligence</strong> — Real-time bridge analytics & DeFi compliance research</p>', unsafe_allow_html=True)
st.markdown("---")

# ============================================
# CHARGEMENT DONNÉES
# ============================================

@st.cache_data(ttl=300)
def load_bridge_data():
    """Charge les données des bridges depuis DefiLlama"""
    collector = DefiLlamaCollector()
    bridges = collector.get_formatted_bridges()
    
    if not bridges:
        return pd.DataFrame()
    
    df = pd.DataFrame(bridges)
    return df

# Chargement des données
with st.spinner("🔄 Chargement des données bridges..."):
    df_bridges = load_bridge_data()

if df_bridges.empty:
    st.error("❌ Impossible de charger les données. Vérifiez votre connexion.")
    st.stop()

# ============================================
# MÉTRIQUES CLÉS
# ============================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    total_tvl = df_bridges['tvl'].sum()
    st.metric(
        label="TVL Total",
        value=f"${total_tvl/1e9:.2f}B",
        delta="Temps réel"
    )

with col2:
    total_volume = df_bridges['volume_24h'].sum()
    st.metric(
        label="Volume 24h",
        value=f"${total_volume/1e6:.1f}M",
        delta="Dernières 24h"
    )

with col3:
    nb_bridges = len(df_bridges)
    st.metric(
        label="Bridges Actifs",
        value=f"{nb_bridges}",
        delta="Surveillés"
    )

with col4:
    total_chains = df_bridges['chains_count'].sum()
    st.metric(
        label="Blockchains",
        value=f"{total_chains}",
        delta="Connectées"
    )

st.markdown("---")

# ============================================
# TOP 10 BRIDGES PAR TVL
# ============================================

st.subheader("🏆 Top 10 Bridges par TVL")

top10 = df_bridges.nlargest(10, 'tvl')

# Graphique avec palette XRSK
fig_tvl = px.bar(
    top10,
    x='name',
    y='tvl',
    title='',
    labels={'tvl': 'TVL (USD)', 'name': 'Bridge'},
    color='tvl',
    color_continuous_scale=['#1F4E78', '#FF6B35']
)
fig_tvl.update_layout(
    showlegend=False,
    height=400,
    xaxis_tickangle=-45,
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(family="Inter, sans-serif", color="#2C3E50"),
    xaxis=dict(showgrid=False),
    yaxis=dict(showgrid=True, gridcolor='#F0F0F0')
)
st.plotly_chart(fig_tvl, use_container_width=True)

# ============================================
# ANALYSE TVL VS VOLUME
# ============================================

st.subheader("📊 Analyse TVL vs Volume 24h")

col1, col2 = st.columns(2)

with col1:
    # Scatter plot TVL vs Volume
    fig_scatter = px.scatter(
        df_bridges.head(20),
        x='tvl',
        y='volume_24h',
        size='chains_count',
        hover_data=['name'],
        title='',
        labels={'tvl': 'TVL', 'volume_24h': 'Volume 24h', 'chains_count': 'Nb Chains'},
        color='chains_count',
        color_continuous_scale='Viridis'
    )
    fig_scatter.update_xaxes(type="log")
    fig_scatter.update_yaxes(type="log")
    fig_scatter.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Inter, sans-serif", color="#2C3E50")
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

with col2:
    # Pie chart répartition TVL
    fig_pie = px.pie(
        top10,
        values='tvl',
        names='name',
        title='',
        color_discrete_sequence=px.colors.sequential.Blues_r
    )
    fig_pie.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Inter, sans-serif", color="#2C3E50")
    )
    st.plotly_chart(fig_pie, use_container_width=True)

# ============================================
# TABLEAU DES BRIDGES
# ============================================

st.subheader("📋 Liste complète des bridges")

# Formatage du dataframe pour affichage
df_display = df_bridges[['name', 'tvl', 'volume_24h', 'chains_count']].copy()
df_display['tvl'] = df_display['tvl'].apply(lambda x: f"${x/1e6:.2f}M")
df_display['volume_24h'] = df_display['volume_24h'].apply(lambda x: f"${x/1e6:.2f}M")
df_display.columns = ['Bridge', 'TVL', 'Volume 24h', 'Chains']

st.dataframe(
    df_display,
    use_container_width=True,
    height=400
)

# ============================================
# FOOTER
# ============================================

st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; font-family: 'Inter', sans-serif; font-size: 0.85rem; color: #999; margin-top: 2rem;">
        <strong>XRSK Platform</strong> — Données actualisées toutes les 5 minutes | Source: DefiLlama<br>
        Dernière mise à jour: """ + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + """
    </div>
    """,
    unsafe_allow_html=True
)
