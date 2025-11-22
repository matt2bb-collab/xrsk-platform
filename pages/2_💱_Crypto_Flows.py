"""
XRSK Platform - Crypto Flows Analysis
Analyse des cryptomonnaies transitant par les bridges
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from backend.collectors.defillama import DefiLlamaCollector

st.set_page_config(page_title="Crypto Flows - XRSK", page_icon="💱", layout="wide")

st.title("💱 Crypto Flows Analysis")
st.markdown("Analyse des cryptomonnaies transitant par les bridges")
st.markdown("---")

# Note sur les données
st.info("""
📊 **Note sur les données**

Cette page affiche les cryptos qui transitent par chaque bridge. 
Les données sont agrégées par bridge et par token.

⚠️ DefiLlama API ne fournit pas les flux en temps réel par défaut. 
Cette fonctionnalité nécessite des appels API supplémentaires.
""")

# Chargement données
@st.cache_data(ttl=300)
def load_bridge_tokens():
    """
    Charge les données de tokens par bridge
    Note: Fonction placeholder - à enrichir avec API détails bridges
    """
    collector = DefiLlamaCollector()
    bridges = collector.get_formatted_bridges()
    
    if not bridges:
        return pd.DataFrame()
    
    # Placeholder: On simule les données de tokens les plus communs
    # En production, il faudrait appeler get_bridge_details() pour chaque bridge
    common_tokens = ['ETH', 'USDC', 'USDT', 'WBTC', 'DAI', 'MATIC', 'BNB', 'AVAX']
    
    data = []
    for bridge in bridges[:20]:  # Top 20 pour démo
        # Pour chaque bridge, on attribue quelques tokens principaux
        for token in common_tokens[:5]:  # 5 tokens principaux par bridge
            # Estimation basée sur le TVL
            estimated_amount = bridge['tvl'] * (0.1 + 0.3 * (common_tokens.index(token) / len(common_tokens)))
            
            data.append({
                'bridge_name': bridge['name'],
                'bridge_id': bridge['id'],
                'token_symbol': token,
                'estimated_tvl': estimated_amount,
                'chains': ', '.join(bridge['chains'][:3]) if bridge['chains'] else 'N/A'
            })
    
    return pd.DataFrame(data)

with st.spinner("🔄 Analyse des flux crypto..."):
    df_flows = load_bridge_tokens()

if df_flows.empty:
    st.error("❌ Données indisponibles")
    st.stop()

# Statistiques globales
st.subheader("📊 Vue d'ensemble")

col1, col2, col3 = st.columns(3)

with col1:
    unique_tokens = df_flows['token_symbol'].nunique()
    st.metric("Tokens Uniques", unique_tokens)

with col2:
    unique_bridges = df_flows['bridge_name'].nunique()
    st.metric("Bridges Analysés", unique_bridges)

with col3:
    total_tvl = df_flows['estimated_tvl'].sum()
    st.metric("TVL Total Estimé", f"${total_tvl/1e9:.2f}B")

st.markdown("---")

# Filtres
st.sidebar.header("🔍 Filtres")

# Filtre par token
selected_tokens = st.sidebar.multiselect(
    "Tokens",
    options=sorted(df_flows['token_symbol'].unique()),
    default=None
)

# Filtre par bridge
selected_bridges = st.sidebar.multiselect(
    "Bridges",
    options=sorted(df_flows['bridge_name'].unique()),
    default=None
)

# Application des filtres
df_filtered = df_flows.copy()
if selected_tokens:
    df_filtered = df_filtered[df_filtered['token_symbol'].isin(selected_tokens)]
if selected_bridges:
    df_filtered = df_filtered[df_filtered['bridge_name'].isin(selected_bridges)]

# Tabs pour différentes vues
tab1, tab2, tab3 = st.tabs(["Par Token", "Par Bridge", "Tableau Détaillé"])

with tab1:
    st.subheader("💰 Distribution par Token")
    
    token_agg = df_filtered.groupby('token_symbol')['estimated_tvl'].sum().sort_values(ascending=False)
    
    fig1 = px.bar(
        x=token_agg.index,
        y=token_agg.values,
        title="TVL par Token (Top Tokens)",
        labels={'x': 'Token', 'y': 'TVL Estimé (USD)'},
        color=token_agg.values,
        color_continuous_scale='Viridis'
    )
    st.plotly_chart(fig1, use_container_width=True)
    
    # Pie chart
    fig2 = px.pie(
        values=token_agg.values[:10],
        names=token_agg.index[:10],
        title="Répartition Top 10 Tokens"
    )
    st.plotly_chart(fig2, use_container_width=True)

with tab2:
    st.subheader("🔗 Distribution par Bridge")
    
    bridge_agg = df_filtered.groupby('bridge_name')['estimated_tvl'].sum().sort_values(ascending=False)
    
    fig3 = px.bar(
        x=bridge_agg.index[:15],
        y=bridge_agg.values[:15],
        title="TVL par Bridge (Top 15)",
        labels={'x': 'Bridge', 'y': 'TVL Estimé (USD)'},
        color=bridge_agg.values[:15],
        color_continuous_scale='Blues'
    )
    fig3.update_xaxes(tickangle=-45)
    st.plotly_chart(fig3, use_container_width=True)
    
    # Heatmap Token x Bridge
    st.subheader("🔥 Heatmap Token × Bridge")
    
    pivot = df_filtered.pivot_table(
        values='estimated_tvl',
        index='token_symbol',
        columns='bridge_name',
        aggfunc='sum',
        fill_value=0
    )
    
    # Limiter pour lisibilité
    pivot_limited = pivot.iloc[:10, :10]
    
    fig4 = px.imshow(
        pivot_limited,
        title="TVL: Token × Bridge (Top 10×10)",
        labels=dict(x="Bridge", y="Token", color="TVL"),
        color_continuous_scale="YlOrRd"
    )
    st.plotly_chart(fig4, use_container_width=True)

with tab3:
    st.subheader("📋 Détails complets")
    
    # Formatage
    df_display = df_filtered.copy()
    df_display['estimated_tvl'] = df_display['estimated_tvl'].apply(lambda x: f"${x/1e6:.2f}M")
    df_display = df_display[['bridge_name', 'token_symbol', 'estimated_tvl', 'chains']]
    df_display.columns = ['Bridge', 'Token', 'TVL Estimé', 'Chains']
    
    st.dataframe(df_display, use_container_width=True, height=500)
    
    # Export
    csv = df_filtered.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Télécharger données CSV",
        data=csv,
        file_name="xrsk_crypto_flows.csv",
        mime="text/csv"
    )

# Avertissement
st.markdown("---")
st.warning("""
⚠️ **Données estimées**

Les montants affichés sont des **estimations** basées sur le TVL global des bridges.
Pour des données précises par token, il faudrait :
1. Interroger l'API DefiLlama pour chaque bridge individuellement
2. Agréger les données de chaînes spécifiques
3. Potentiellement utiliser d'autres sources (Dune Analytics, The Graph)

**Hook préparé** : La structure permet facilement d'ajouter ces sources de données.
""")

# ============================================
# HOOK: Enhanced Token Data
# ============================================
# Pour améliorer avec données réelles :
# 1. Créer backend/collectors/token_flows.py
# 2. Implémenter get_bridge_token_details()
# 3. Remplacer la fonction load_bridge_tokens()
# 4. Possibilité d'intégrer Dune Analytics, The Graph
# ============================================
