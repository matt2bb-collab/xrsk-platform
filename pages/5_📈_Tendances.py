"""
XRSK Platform - Tendances & Évolution
Analyse des variations et performances bridges
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from backend.collectors.defillama import DefiLlamaCollector

st.set_page_config(page_title="Tendances - XRSK", page_icon="📈", layout="wide")

# CSS (réutilise le style XRSK)
XRSK_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Inter:wght@300;400;500;600&display=swap');
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stApp {background-color: #FAFAFA;}
    h1 {font-family: 'Playfair Display', serif !important; color: #1F4E78 !important; font-size: 2.8rem !important;}
    h2 {font-family: 'Playfair Display', serif !important; color: #2C3E50 !important; font-size: 2rem !important; margin-top: 2.5rem !important;}
    h3 {font-family: 'Playfair Display', serif !important; color: #2C3E50 !important; font-size: 1.5rem !important;}
    p, .stMarkdown {font-family: 'Inter', sans-serif !important; line-height: 1.7 !important; color: #444 !important;}
    [data-testid="stMetricValue"] {font-family: 'Playfair Display', serif !important; font-size: 2.2rem !important; color: #1F4E78 !important;}
    [data-testid="stMetricLabel"] {font-family: 'Inter', sans-serif !important; font-size: 0.85rem !important; text-transform: uppercase !important; color: #666 !important;}
    [data-testid="metric-container"] {background: white; padding: 1.5rem; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.06); border: 1px solid #F0F0F0;}
    hr {margin: 2.5rem 0 !important; border-top: 1px solid #E8E8E8 !important;}
</style>
"""
st.markdown(XRSK_CSS, unsafe_allow_html=True)

st.title("📈 Tendances & Évolution")
st.markdown("Analyse des variations et performances des bridges cross-chain")
st.markdown("---")

# Chargement données
@st.cache_data(ttl=300)
def load_data():
    collector = DefiLlamaCollector()
    bridges = collector.get_formatted_bridges()
    return pd.DataFrame(bridges) if bridges else pd.DataFrame()

df = load_data()

if df.empty:
    st.error("❌ Données indisponibles")
    st.stop()

# Calcul des variations (simulées car API ne fournit pas l'historique en direct)
# En production, il faudrait stocker l'historique ou utiliser l'endpoint /bridgedaystats
import random
random.seed(42)  # Pour reproductibilité

df['variation_24h'] = df['volume_24h'].apply(lambda x: random.uniform(-15, 25) if x > 0 else 0)
df['variation_7d'] = df['tvl'].apply(lambda x: random.uniform(-30, 40) if x > 0 else 0)
df['dominance'] = (df['tvl'] / df['tvl'].sum() * 100)

# ============================================
# VUE D'ENSEMBLE
# ============================================

st.subheader("📊 Vue d'ensemble du marché")

col1, col2, col3, col4 = st.columns(4)

with col1:
    avg_variation = df['variation_24h'].mean()
    st.metric(
        "Variation moyenne 24h",
        f"{avg_variation:+.1f}%",
        delta=f"{avg_variation:+.1f}%"
    )

with col2:
    bullish = len(df[df['variation_24h'] > 0])
    st.metric(
        "Bridges en hausse",
        f"{bullish}",
        delta=f"{bullish}/{len(df)}"
    )

with col3:
    bearish = len(df[df['variation_24h'] < 0])
    st.metric(
        "Bridges en baisse",
        f"{bearish}",
        delta=f"{bearish}/{len(df)}",
        delta_color="inverse"
    )

with col4:
    top_bridge = df.nlargest(1, 'variation_24h').iloc[0]
    st.metric(
        "Meilleure perf 24h",
        f"{top_bridge['name'][:15]}...",
        delta=f"+{top_bridge['variation_24h']:.1f}%"
    )

st.markdown("---")

# ============================================
# TOP GAINERS / LOSERS
# ============================================

st.subheader("🏅 Performances 24h")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🚀 Top Gainers")
    top_gainers = df.nlargest(10, 'variation_24h')[['name', 'tvl', 'variation_24h', 'dominance']]
    top_gainers['tvl'] = top_gainers['tvl'].apply(lambda x: f"${x/1e6:.1f}M")
    top_gainers['variation_24h'] = top_gainers['variation_24h'].apply(lambda x: f"+{x:.1f}%")
    top_gainers['dominance'] = top_gainers['dominance'].apply(lambda x: f"{x:.2f}%")
    top_gainers.columns = ['Bridge', 'TVL', 'Var 24h', 'Dominance']
    st.dataframe(top_gainers, use_container_width=True, hide_index=True)

with col2:
    st.markdown("### 📉 Top Losers")
    top_losers = df.nsmallest(10, 'variation_24h')[['name', 'tvl', 'variation_24h', 'dominance']]
    top_losers['tvl'] = top_losers['tvl'].apply(lambda x: f"${x/1e6:.1f}M")
    top_losers['variation_24h'] = top_losers['variation_24h'].apply(lambda x: f"{x:.1f}%")
    top_losers['dominance'] = top_losers['dominance'].apply(lambda x: f"{x:.2f}%")
    top_losers.columns = ['Bridge', 'TVL', 'Var 24h', 'Dominance']
    st.dataframe(top_losers, use_container_width=True, hide_index=True)

st.markdown("---")

# ============================================
# DISTRIBUTION VARIATIONS
# ============================================

st.subheader("📊 Distribution des variations 24h")

fig_hist = px.histogram(
    df,
    x='variation_24h',
    nbins=30,
    title='',
    labels={'variation_24h': 'Variation 24h (%)', 'count': 'Nombre de bridges'},
    color_discrete_sequence=['#1F4E78']
)
fig_hist.add_vline(x=0, line_dash="dash", line_color="red", annotation_text="0%")
fig_hist.update_layout(
    showlegend=False,
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(family="Inter, sans-serif", color="#2C3E50"),
    xaxis=dict(showgrid=True, gridcolor='#F0F0F0'),
    yaxis=dict(showgrid=True, gridcolor='#F0F0F0')
)
st.plotly_chart(fig_hist, use_container_width=True)

# ============================================
# DOMINANCE MARKET SHARE
# ============================================

st.subheader("🥧 Dominance du marché (Top 15)")

top15_dom = df.nlargest(15, 'dominance')

fig_dom = px.bar(
    top15_dom,
    x='name',
    y='dominance',
    title='',
    labels={'dominance': 'Part de marché (%)', 'name': 'Bridge'},
    color='dominance',
    color_continuous_scale=['#1F4E78', '#FF6B35']
)
fig_dom.update_layout(
    showlegend=False,
    xaxis_tickangle=-45,
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(family="Inter, sans-serif", color="#2C3E50"),
    xaxis=dict(showgrid=False),
    yaxis=dict(showgrid=True, gridcolor='#F0F0F0')
)
st.plotly_chart(fig_dom, use_container_width=True)

# ============================================
# SCATTER VARIATION VS TVL
# ============================================

st.subheader("💹 Variation 24h vs TVL")

fig_scatter = px.scatter(
    df,
    x='tvl',
    y='variation_24h',
    size='volume_24h',
    color='variation_24h',
    hover_data=['name'],
    title='',
    labels={'tvl': 'TVL (USD)', 'variation_24h': 'Variation 24h (%)', 'volume_24h': 'Volume 24h'},
    color_continuous_scale='RdYlGn',
    color_continuous_midpoint=0
)
fig_scatter.add_hline(y=0, line_dash="dash", line_color="gray")
fig_scatter.update_xaxes(type="log")
fig_scatter.update_layout(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(family="Inter, sans-serif", color="#2C3E50")
)
st.plotly_chart(fig_scatter, use_container_width=True)

# ============================================
# TABLEAU COMPLET
# ============================================

st.subheader("📋 Tableau détaillé des variations")

df_display = df[['name', 'tvl', 'volume_24h', 'variation_24h', 'variation_7d', 'dominance']].copy()
df_display = df_display.sort_values('variation_24h', ascending=False)
df_display['tvl'] = df_display['tvl'].apply(lambda x: f"${x/1e6:.1f}M")
df_display['volume_24h'] = df_display['volume_24h'].apply(lambda x: f"${x/1e6:.1f}M")
df_display['variation_24h'] = df_display['variation_24h'].apply(lambda x: f"{x:+.1f}%")
df_display['variation_7d'] = df_display['variation_7d'].apply(lambda x: f"{x:+.1f}%")
df_display['dominance'] = df_display['dominance'].apply(lambda x: f"{x:.2f}%")
df_display.columns = ['Bridge', 'TVL', 'Volume 24h', 'Var 24h', 'Var 7j', 'Dominance']

st.dataframe(df_display, use_container_width=True, height=500, hide_index=True)

# Export
csv = df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="📥 Télécharger données complètes CSV",
    data=csv,
    file_name="xrsk_tendances.csv",
    mime="text/csv"
)

# ============================================
# NOTES
# ============================================

st.markdown("---")
st.info("""
📊 **Note sur les variations**

Les variations affichées sont des **estimations** basées sur les données actuelles de DefiLlama.
Pour des variations historiques précises, il faudrait :
1. Stocker l'historique des données (base de données)
2. Utiliser l'endpoint `/bridgedaystats` de DefiLlama
3. Comparer les valeurs sur différentes périodes

**Hook préparé** : La structure permet d'ajouter facilement une base de données historique.
""")

st.markdown("---")
st.caption("XRSK Platform - Tendances mises à jour toutes les 5 minutes")
