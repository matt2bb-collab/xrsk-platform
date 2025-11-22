"""
XRSK Platform - Dashboard principal
Version corrigée avec données réelles
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
from backend.collectors.defillama import DefiLlamaCollector

# Configuration
st.set_page_config(
    page_title="XRSK Platform - Cross-Chain Risk Intelligence",
    page_icon="🔗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS XRSK
XRSK_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Inter:wght@300;400;500;600&display=swap');
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    [data-testid="stSidebar"] {background-color: #FFFFFF; border-right: 1px solid #E8E8E8;}
    [data-testid="stSidebar"] > div:first-child {padding-top: 2rem;}
    [data-testid="stSidebar"] h1 {font-family: 'Playfair Display', serif !important; font-size: 1.5rem !important; color: #1F4E78 !important; margin-bottom: 2rem !important; padding: 0 1rem;}
    [data-testid="stSidebarNav"] a {font-family: 'Inter', sans-serif !important; font-size: 0.95rem !important; color: #2C3E50 !important; padding: 0.8rem 1rem !important; border-radius: 6px !important; margin: 0.2rem 0.5rem !important; transition: all 0.2s !important;}
    [data-testid="stSidebarNav"] a:hover {background-color: #F8F9FA !important; color: #1F4E78 !important;}
    [data-testid="stSidebarNav"] a[aria-current="page"] {background-color: #1F4E78 !important; color: white !important; font-weight: 500 !important;}
    .stApp {background-color: #FAFAFA;}
    .block-container {padding-top: 2rem; padding-bottom: 3rem; max-width: 1400px;}
    h1 {font-family: 'Playfair Display', serif !important; font-weight: 700 !important; color: #1F4E78 !important; font-size: 2.8rem !important; margin-bottom: 0.5rem !important; letter-spacing: -0.02em !important;}
    h2 {font-family: 'Playfair Display', serif !important; font-weight: 600 !important; color: #2C3E50 !important; font-size: 2rem !important; margin-top: 2.5rem !important; margin-bottom: 1rem !important;}
    h3 {font-family: 'Playfair Display', serif !important; font-weight: 600 !important; color: #2C3E50 !important; font-size: 1.5rem !important;}
    p, .stMarkdown {font-family: 'Inter', sans-serif !important; font-size: 1rem !important; line-height: 1.7 !important; color: #444 !important;}
    [data-testid="stMetricValue"] {font-family: 'Playfair Display', serif !important; font-size: 2.2rem !important; font-weight: 700 !important; color: #1F4E78 !important;}
    [data-testid="stMetricLabel"] {font-family: 'Inter', sans-serif !important; font-size: 0.85rem !important; font-weight: 500 !important; color: #666 !important; text-transform: uppercase !important; letter-spacing: 0.05em !important;}
    [data-testid="metric-container"] {background: white; padding: 1.5rem; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.06); border: 1px solid #F0F0F0;}
    [data-testid="stDataFrame"] th {background-color: #F8F9FA !important; color: #2C3E50 !important; font-weight: 600 !important; font-size: 0.85rem !important; text-transform: uppercase !important; letter-spacing: 0.05em !important; padding: 1rem !important; border-bottom: 2px solid #1F4E78 !important;}
    [data-testid="stDataFrame"] td {font-size: 0.95rem !important; padding: 0.8rem 1rem !important; border-bottom: 1px solid #F0F0F0 !important;}
    hr {margin: 2.5rem 0 !important; border: none !important; border-top: 1px solid #E8E8E8 !important;}
    .xrsk-baseline {font-family: 'Inter', sans-serif; font-size: 1.1rem; color: #666; font-weight: 300; margin-bottom: 2rem;}
</style>
"""
st.markdown(XRSK_CSS, unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("# 🔗 XRSK")
    st.markdown("---")
    st.markdown("""
    **Cross-Chain Risk Intelligence**
    
    📊 Real-time bridge analytics  
    🔬 DeFi compliance research  
    📈 MiCA/DORA framework
    """)
    st.markdown("---")
    st.markdown(f"""
    <div style="font-size: 0.75rem; color: #999; text-align: center;">
        Dernière mise à jour<br>
        {datetime.now().strftime('%H:%M:%S')}
    </div>
    """, unsafe_allow_html=True)

# Header
st.title("🔗 XRSK Platform")
st.markdown('<p class="xrsk-baseline"><strong>Cross-Chain Risk Intelligence</strong> — Real-time bridge analytics & DeFi compliance research</p>', unsafe_allow_html=True)
st.markdown("---")

# Chargement données
@st.cache_data(ttl=300)
def load_bridge_data():
    collector = DefiLlamaCollector()
    bridges = collector.get_formatted_bridges()
    if not bridges:
        return pd.DataFrame()
    df = pd.DataFrame(bridges)
    
    # Calculs métriques supplémentaires
    df['dominance_volume'] = (df['volume_24h'] / df['volume_24h'].sum() * 100)
    
    return df

with st.spinner("🔄 Chargement des données bridges..."):
    df_bridges = load_bridge_data()

if df_bridges.empty:
    st.error("❌ Impossible de charger les données. Vérifiez votre connexion.")
    st.stop()

# Filtrer les bridges avec volume > 0 pour les stats
df_active = df_bridges[df_bridges['volume_24h'] > 0].copy()

# MÉTRIQUES CLÉS
col1, col2, col3, col4 = st.columns(4)

with col1:
    total_volume = df_active['volume_24h'].sum()
    st.metric(
        label="Volume 24h Total",
        value=f"${total_volume/1e9:.2f}B",
        delta="Temps réel"
    )

with col2:
    volume_7d = df_active['volume_7d'].sum()
    st.metric(
        label="Volume 7j",
        value=f"${volume_7d/1e9:.2f}B",
        delta=f"+{((volume_7d/7)/(total_volume) - 1)*100:.1f}% vs avg"
    )

with col3:
    nb_bridges = len(df_active)
    st.metric(
        label="Bridges Actifs",
        value=f"{nb_bridges}",
        delta=f"{nb_bridges}/{len(df_bridges)} total"
    )

with col4:
    total_chains = df_active['chains_count'].sum()
    avg_chains = df_active['chains_count'].mean()
    st.metric(
        label="Blockchains",
        value=f"{total_chains}",
        delta=f"Moy: {avg_chains:.1f}/bridge"
    )

st.markdown("---")

# MÉTRIQUES SECONDAIRES
st.subheader("📊 Analyse du marché")

col1, col2, col3, col4 = st.columns(4)

with col1:
    top_bridge = df_active.nlargest(1, 'volume_24h').iloc[0]
    st.metric(
        label="Bridge le plus actif",
        value=f"{top_bridge['name'][:15]}",
        delta=f"{top_bridge['dominance_volume']:.1f}% du volume"
    )

with col2:
    avg_volume = df_active['volume_24h'].mean()
    st.metric(
        label="Volume moyen",
        value=f"${avg_volume/1e6:.1f}M",
        delta="par bridge"
    )

with col3:
    median_volume = df_active['volume_24h'].median()
    st.metric(
        label="Volume médian",
        value=f"${median_volume/1e6:.1f}M",
        delta="50% des bridges"
    )

with col4:
    multi_chain = df_active.nlargest(1, 'chains_count').iloc[0]
    st.metric(
        label="Multi-chain leader",
        value=f"{multi_chain['name'][:15]}",
        delta=f"{int(multi_chain['chains_count'])} chains"
    )

st.markdown("---")

# TOP 10 BRIDGES
st.subheader("🏆 Top 10 Bridges par Volume 24h")

top10 = df_active.nlargest(10, 'volume_24h')

fig_vol = go.Figure()
fig_vol.add_trace(go.Bar(
    x=top10['name'],
    y=top10['volume_24h'],
    marker=dict(
        color=top10['volume_24h'],
        colorscale=[[0, '#1F4E78'], [1, '#FF6B35']],
        showscale=False
    ),
    text=[f"${v/1e9:.2f}B" for v in top10['volume_24h']],
    textposition='outside',
    hovertemplate='<b>%{x}</b><br>Volume 24h: $%{y:,.0f}<extra></extra>'
))

fig_vol.update_layout(
    showlegend=False,
    height=400,
    xaxis_tickangle=-45,
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(family="Inter, sans-serif", color="#2C3E50"),
    xaxis=dict(showgrid=False, title=''),
    yaxis=dict(showgrid=True, gridcolor='#F0F0F0', title='Volume 24h (USD)')
)
st.plotly_chart(fig_vol, use_container_width=True)

# RÉPARTITION
st.subheader("🥧 Répartition du marché")

col1, col2 = st.columns(2)

with col1:
    fig_pie = px.pie(
        top10,
        values='volume_24h',
        names='name',
        title='Dominance Top 10 (Volume 24h)',
        color_discrete_sequence=px.colors.sequential.Blues_r
    )
    fig_pie.update_traces(textposition='inside', textinfo='percent+label')
    fig_pie.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Inter, sans-serif", color="#2C3E50")
    )
    st.plotly_chart(fig_pie, use_container_width=True)

with col2:
    fig_tree = px.treemap(
        top10,
        path=['name'],
        values='volume_24h',
        title='Treemap Volume 24h',
        color='dominance_volume',
        color_continuous_scale='Blues'
    )
    fig_tree.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Inter, sans-serif", color="#2C3E50")
    )
    st.plotly_chart(fig_tree, use_container_width=True)

# TABLEAU
st.subheader("📋 Liste complète des bridges actifs")

df_display = df_active[['name', 'volume_24h', 'volume_7d', 'chains_count', 'dominance_volume']].copy()
df_display = df_display.sort_values('volume_24h', ascending=False)
df_display['volume_24h'] = df_display['volume_24h'].apply(lambda x: f"${x/1e6:.2f}M")
df_display['volume_7d'] = df_display['volume_7d'].apply(lambda x: f"${x/1e6:.2f}M")
df_display['dominance_volume'] = df_display['dominance_volume'].apply(lambda x: f"{x:.2f}%")
df_display.columns = ['Bridge', 'Volume 24h', 'Volume 7j', 'Chains', 'Dominance']

st.dataframe(df_display, use_container_width=True, height=400, hide_index=True)

# Footer
st.markdown("---")
st.markdown(
    f"""
    <div style="text-align: center; font-family: 'Inter', sans-serif; font-size: 0.85rem; color: #999; margin-top: 2rem;">
        <strong>XRSK Platform</strong> — {len(df_active)} bridges actifs | Données actualisées toutes les 5 minutes | Source: DefiLlama<br>
        Dernière mise à jour: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    </div>
    """,
    unsafe_allow_html=True
)
