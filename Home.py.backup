"""
XRSK Platform - Dashboard principal
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

# CSS Custom pour style XRSK
st.markdown("""
<style>
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* XRSK Custom styling */
    .stApp {
        background-color: #FAFAFA;
    }
    h1, h2, h3 {
        font-family: 'Georgia', serif;
        color: #1F4E78;
    }
    .metric-card {
        background: white;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Header
st.title("🔗 XRSK Platform")
st.markdown("**Cross-Chain Risk Intelligence** - Real-time bridge analytics & DeFi compliance research")
st.markdown("---")

# Fonction de cache pour les données (5 min)
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

# Métriques clés
col1, col2, col3, col4 = st.columns(4)

with col1:
    total_tvl = df_bridges['tvl'].sum()
    st.metric(
        label="📊 TVL Total",
        value=f"${total_tvl/1e9:.2f}B",
        delta="Temps réel"
    )

with col2:
    total_volume = df_bridges['volume_24h'].sum()
    st.metric(
        label="💱 Volume 24h",
        value=f"${total_volume/1e6:.1f}M",
        delta="Dernières 24h"
    )

with col3:
    nb_bridges = len(df_bridges)
    st.metric(
        label="🔗 Bridges Actifs",
        value=f"{nb_bridges}",
        delta="Surveillés"
    )

with col4:
    total_chains = df_bridges['chains_count'].sum()
    st.metric(
        label="⛓️ Blockchains",
        value=f"{total_chains}",
        delta="Connectées"
    )

st.markdown("---")

# Top 10 Bridges par TVL
st.subheader("🏆 Top 10 Bridges par TVL")

top10 = df_bridges.nlargest(10, 'tvl')

fig_tvl = px.bar(
    top10,
    x='name',
    y='tvl',
    title='Total Value Locked (TVL)',
    labels={'tvl': 'TVL (USD)', 'name': 'Bridge'},
    color='tvl',
    color_continuous_scale='Blues'
)
fig_tvl.update_layout(
    showlegend=False,
    height=400,
    xaxis_tickangle=-45
)
st.plotly_chart(fig_tvl, use_container_width=True)

# Répartition TVL vs Volume
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
        title='TVL vs Volume (Top 20)',
        labels={'tvl': 'TVL', 'volume_24h': 'Volume 24h', 'chains_count': 'Nb Chains'},
        color='chains_count',
        color_continuous_scale='Viridis'
    )
    fig_scatter.update_xaxes(type="log")
    fig_scatter.update_yaxes(type="log")
    st.plotly_chart(fig_scatter, use_container_width=True)

with col2:
    # Pie chart répartition TVL
    fig_pie = px.pie(
        top10,
        values='tvl',
        names='name',
        title='Répartition TVL (Top 10)'
    )
    st.plotly_chart(fig_pie, use_container_width=True)

# Tableau des bridges
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

# Footer
st.markdown("---")
st.markdown("**XRSK Platform** - Données actualisées toutes les 5 minutes | Source: DefiLlama")
st.caption(f"Dernière mise à jour: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
