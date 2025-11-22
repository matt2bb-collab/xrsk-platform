"""
XRSK Platform - Bridge Analytics
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from backend.collectors.defillama import DefiLlamaCollector

st.set_page_config(page_title="Bridge Analytics - XRSK", page_icon="📊", layout="wide")

st.title("📊 Bridge Analytics")
st.markdown("Analyse détaillée des bridges cross-chain")
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

# Filtres
st.sidebar.header("🔍 Filtres")

# Filtre TVL
tvl_min = st.sidebar.slider(
    "TVL Minimum (M$)",
    min_value=0,
    max_value=int(df['tvl'].max() / 1e6),
    value=0
)

# Filtre Volume
vol_min = st.sidebar.slider(
    "Volume 24h Minimum (M$)",
    min_value=0,
    max_value=int(df['volume_24h'].max() / 1e6),
    value=0
)

# Filtre Chains
chains_min = st.sidebar.slider(
    "Nombre de chains minimum",
    min_value=1,
    max_value=int(df['chains_count'].max()),
    value=1
)

# Application des filtres
df_filtered = df[
    (df['tvl'] >= tvl_min * 1e6) &
    (df['volume_24h'] >= vol_min * 1e6) &
    (df['chains_count'] >= chains_min)
]

st.success(f"✅ {len(df_filtered)} bridges correspondent aux filtres")

# Métriques filtrées
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("TVL Filtré", f"${df_filtered['tvl'].sum()/1e9:.2f}B")

with col2:
    st.metric("Volume 24h Filtré", f"${df_filtered['volume_24h'].sum()/1e6:.1f}M")

with col3:
    st.metric("Bridges", len(df_filtered))

# Graphiques
st.subheader("📈 Visualisations")

tab1, tab2, tab3 = st.tabs(["Comparaison", "Distribution", "Évolution"])

with tab1:
    fig1 = px.bar(
        df_filtered.nlargest(15, 'tvl'),
        x='name',
        y=['tvl', 'volume_24h'],
        title="TVL vs Volume (Top 15)",
        barmode='group'
    )
    st.plotly_chart(fig1, use_container_width=True)

with tab2:
    fig2 = px.histogram(
        df_filtered,
        x='chains_count',
        title="Distribution du nombre de chains",
        nbins=20
    )
    st.plotly_chart(fig2, use_container_width=True)

with tab3:
    st.info("📊 Graphique d'évolution temporelle - Disponible prochainement (nécessite historique)")

# Tableau détaillé
st.subheader("📋 Tableau comparatif")

df_table = df_filtered[['name', 'tvl', 'volume_24h', 'chains_count']].copy()
df_table['tvl'] = df_table['tvl'].apply(lambda x: f"${x/1e6:.2f}M")
df_table['volume_24h'] = df_table['volume_24h'].apply(lambda x: f"${x/1e6:.2f}M")
df_table.columns = ['Bridge', 'TVL', 'Volume 24h', 'Chains']

st.dataframe(df_table, use_container_width=True, height=500)

# Export (hook préparé)
st.markdown("---")
col1, col2 = st.columns(2)

with col1:
    csv = df_filtered.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Télécharger CSV",
        data=csv,
        file_name="xrsk_bridges.csv",
        mime="text/csv"
    )

with col2:
    st.info("📊 Export PDF/Excel - Disponible prochainement (Hook préparé)")

# ============================================
# HOOK: Export Formats
# ============================================
# Pour ajouter PDF/Excel :
# 1. Créer hooks/exporters.py avec fonctions export
# 2. Importer ici et ajouter boutons download
# ============================================
