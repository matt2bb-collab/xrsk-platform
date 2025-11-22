#!/usr/bin/env python3
"""
XRSK Platform - Script d'installation automatisé
Crée l'arborescence complète et génère tous les fichiers
Usage: python setup_xrsk.py
"""

import os
from pathlib import Path

# Configuration
PROJECT_NAME = "."  # Création dans le dossier courant
GITHUB_USER = "matt2bb-collab"

def create_directory_structure():
    """Crée l'arborescence complète du projet"""
    
    dirs = [
        "pages",
        "backend",
        "backend/collectors",
        "hooks",
        ".streamlit",
        "data",
    ]
    
    print("📁 Création des dossiers...")
    for d in dirs:
        Path(d).mkdir(parents=True, exist_ok=True)
        print(f"   ✓ {d}")
    
    return PROJECT_NAME

def create_config_toml(project_dir):
    """Crée le fichier de configuration Streamlit"""
    
    content = """[theme]
primaryColor = "#1F4E78"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F5F5F5"
textColor = "#2C3E50"
font = "serif"

[server]
headless = true
port = 8501
"""
    
    filepath = ".streamlit/config.toml"
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"   ✓ {filepath}")

def create_requirements(project_dir):
    """Crée requirements.txt"""
    
    content = """streamlit==1.29.0
requests==2.31.0
pandas==2.1.3
plotly==5.18.0
"""
    
    filepath = "requirements.txt"
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"   ✓ {filepath}")

def create_gitignore(project_dir):
    """Crée .gitignore"""
    
    content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/

# Streamlit
.streamlit/secrets.toml

# Data
data/*.db
data/*.csv

# IDE
.vscode/
.idea/
*.swp
*.swo
"""
    
    filepath = ".gitignore"
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"   ✓ {filepath}")

def create_readme(project_dir):
    """Crée README.md"""
    
    content = """# 🔗 XRSK Platform

**Cross-Chain Risk Intelligence - Real-time bridge analytics & DeFi compliance research**

## 🎯 Mission

Quantifier les risques cross-chain pour une DeFi plus sûre et conforme aux régulations MiCA/DORA.

## 🚀 Features

- 📊 **Bridge Analytics** - Surveillance temps réel de 50+ bridges DeFi
- 💱 **Crypto Flows** - Analyse des flux de cryptos par bridge
- 🔬 **Research Lab** - Publications et méthodologie de scoring
- 📈 **Risk Scoring** - Framework à 5 piliers (Security, Liquidity, Governance, Operational, Regulatory)

## 🛠️ Tech Stack

- **Frontend**: Streamlit 1.29
- **Data**: DefiLlama API
- **Charts**: Plotly
- **Deployment**: Streamlit Cloud

## 📦 Installation locale

```bash
pip install -r requirements.txt
streamlit run Home.py
```

## 🌐 Live Demo

[https://matt2bb-collab-xrsk-platform.streamlit.app](https://matt2bb-collab-xrsk-platform.streamlit.app)

## 📄 License

Personal research project - Non-commercial use

## 👤 Author

Expert conformité crypto MiCA/DORA | Certifié AMF
"""
    
    filepath = "README.md"
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"   ✓ {filepath}")

def create_backend_models(project_dir):
    """Crée backend/models.py"""
    
    content = """\"\"\"
Modèles de données pour XRSK Platform
\"\"\"

from dataclasses import dataclass
from typing import Optional, Dict, List
from datetime import datetime

@dataclass
class BridgeData:
    \"\"\"Données d'un bridge cross-chain\"\"\"
    id: str
    name: str
    tvl: float
    volume_24h: float
    chains: List[str]
    last_updated: datetime
    
    # Données additionnelles
    txs_24h: Optional[int] = None
    chains_count: Optional[int] = None
    
    # Scores (à implémenter)
    security_score: Optional[float] = None
    liquidity_score: Optional[float] = None
    governance_score: Optional[float] = None
    operational_score: Optional[float] = None
    regulatory_score: Optional[float] = None
    
    @property
    def total_score(self) -> Optional[float]:
        \"\"\"Score total pondéré\"\"\"
        if all([self.security_score, self.liquidity_score]):
            return (
                self.security_score * 0.35 +
                self.liquidity_score * 0.25 +
                (self.governance_score or 0) * 0.20 +
                (self.operational_score or 0) * 0.15 +
                (self.regulatory_score or 0) * 0.05
            )
        return None

@dataclass
class CryptoFlow:
    \"\"\"Flux crypto d'un bridge\"\"\"
    bridge_id: str
    bridge_name: str
    token_symbol: str
    amount: float
    usd_value: float
    from_chain: str
    to_chain: str
    timestamp: datetime
"""
    
    filepath = "backend/models.py"
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"   ✓ {filepath}")

def create_defillama_collector(project_dir):
    """Crée backend/collectors/defillama.py"""
    
    content = """\"\"\"
Collecteur de données DefiLlama
\"\"\"

import requests
from typing import List, Dict, Optional
from datetime import datetime

class DefiLlamaCollector:
    \"\"\"Collecteur de données bridges depuis DefiLlama API\"\"\"
    
    BASE_URL = "https://bridges.llama.fi"
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'XRSK-Platform/1.0'
        })
    
    def get_all_bridges(self) -> Optional[List[Dict]]:
        \"\"\"
        Récupère la liste complète des bridges
        
        Returns:
            Liste de dictionnaires avec données bridges
        \"\"\"
        try:
            response = self.session.get(f"{self.BASE_URL}/bridges", timeout=10)
            response.raise_for_status()
            data = response.json()
            
            bridges = data.get('bridges', [])
            print(f"✓ {len(bridges)} bridges récupérés depuis DefiLlama")
            return bridges
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Erreur DefiLlama API: {e}")
            return None
    
    def get_bridge_details(self, bridge_id: str) -> Optional[Dict]:
        \"\"\"
        Récupère les détails d'un bridge spécifique
        
        Args:
            bridge_id: ID du bridge
            
        Returns:
            Dictionnaire avec détails du bridge
        \"\"\"
        try:
            response = self.session.get(
                f"{self.BASE_URL}/bridge/{bridge_id}",
                timeout=10
            )
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Erreur récupération bridge {bridge_id}: {e}")
            return None
    
    def get_bridge_volume(self, bridge_id: str) -> Optional[Dict]:
        \"\"\"
        Récupère les volumes d'un bridge
        
        Args:
            bridge_id: ID du bridge
            
        Returns:
            Données de volume
        \"\"\"
        try:
            response = self.session.get(
                f"{self.BASE_URL}/bridgevolume/{bridge_id}",
                timeout=10
            )
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Erreur volume bridge {bridge_id}: {e}")
            return None
    
    def format_bridge_data(self, raw_data: Dict) -> Dict:
        \"\"\"
        Formate les données brutes DefiLlama
        
        Args:
            raw_data: Données brutes de l'API
            
        Returns:
            Données formatées
        \"\"\"
        return {
            'id': raw_data.get('id', ''),
            'name': raw_data.get('displayName', raw_data.get('name', '')),
            'tvl': raw_data.get('tvl', 0),
            'volume_24h': raw_data.get('volume24h', 0),
            'chains': raw_data.get('chains', []),
            'chains_count': len(raw_data.get('chains', [])),
            'last_updated': datetime.now(),
        }
    
    def get_formatted_bridges(self) -> List[Dict]:
        \"\"\"
        Récupère et formate tous les bridges
        
        Returns:
            Liste de bridges formatés
        \"\"\"
        raw_bridges = self.get_all_bridges()
        
        if not raw_bridges:
            return []
        
        formatted = []
        for bridge in raw_bridges:
            try:
                formatted.append(self.format_bridge_data(bridge))
            except Exception as e:
                print(f"⚠️  Erreur formatage bridge {bridge.get('name')}: {e}")
                continue
        
        return formatted

# ============================================
# HOOK: Data Sources Extension Point
# ============================================
# Pour ajouter d'autres sources de données :
# 1. Créer une classe similaire (ex: CoinGeckoCollector)
# 2. Implémenter les mêmes méthodes (get_all_bridges, format_bridge_data)
# 3. Enregistrer dans hooks/data_sources.py
# ============================================
"""
    
    filepath = "backend/collectors/defillama.py"
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"   ✓ {filepath}")

def create_backend_init(project_dir):
    """Crée les fichiers __init__.py"""
    
    files = [
        "backend/__init__.py",
        "backend/collectors/__init__.py",
    ]
    
    for filepath in files:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("")
        print(f"   ✓ {filepath}")

def create_hooks_data_sources(project_dir):
    """Crée hooks/data_sources.py"""
    
    content = """\"\"\"
============================================
HOOK: Data Sources Extension Point
============================================

Configuration des sources de données pour XRSK Platform.

Ajouter de nouvelles sources :
1. Créer un collecteur dans backend/collectors/
2. L'importer ici
3. L'ajouter au dictionnaire AVAILABLE_COLLECTORS

Exemple :
    from backend.collectors.coingecko import CoinGeckoCollector
    AVAILABLE_COLLECTORS['coingecko'] = CoinGeckoCollector

============================================
\"\"\"

from backend.collectors.defillama import DefiLlamaCollector

# Collecteurs disponibles
AVAILABLE_COLLECTORS = {
    'defillama': DefiLlamaCollector,
    # HOOK: Ajouter ici
    # 'coingecko': CoinGeckoCollector,
    # 'l2beat': L2BeatCollector,
    # 'dune': DuneCollector,
}

def get_collector(source='defillama'):
    \"\"\"
    Récupère un collecteur par son nom
    
    Args:
        source: Nom de la source ('defillama', 'coingecko', etc.)
        
    Returns:
        Instance du collecteur
    \"\"\"
    collector_class = AVAILABLE_COLLECTORS.get(source)
    
    if not collector_class:
        raise ValueError(f"Source inconnue: {source}. Disponibles: {list(AVAILABLE_COLLECTORS.keys())}")
    
    return collector_class()
"""
    
    filepath = "hooks/data_sources.py"
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"   ✓ {filepath}")

def create_home_page(project_dir):
    """Crée Home.py (page principale)"""
    
    content = """\"\"\"
XRSK Platform - Dashboard principal
\"\"\"

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
st.markdown(\"\"\"
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
\"\"\", unsafe_allow_html=True)

# Header
st.title("🔗 XRSK Platform")
st.markdown("**Cross-Chain Risk Intelligence** - Real-time bridge analytics & DeFi compliance research")
st.markdown("---")

# Fonction de cache pour les données (5 min)
@st.cache_data(ttl=300)
def load_bridge_data():
    \"\"\"Charge les données des bridges depuis DefiLlama\"\"\"
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
"""
    
    filepath = "Home.py"
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"   ✓ {filepath}")

def create_analytics_page(project_dir):
    """Crée pages/1_📊_Analytics.py"""
    
    content = """\"\"\"
XRSK Platform - Bridge Analytics
\"\"\"

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
"""
    
    filepath = "pages/1_📊_Analytics.py"
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"   ✓ {filepath}")

def create_crypto_flows_page(project_dir):
    """Crée pages/2_💱_Crypto_Flows.py - Page des flux cryptos"""
    
    content = """\"\"\"
XRSK Platform - Crypto Flows Analysis
Analyse des cryptomonnaies transitant par les bridges
\"\"\"

import streamlit as st
import pandas as pd
import plotly.express as px
from backend.collectors.defillama import DefiLlamaCollector

st.set_page_config(page_title="Crypto Flows - XRSK", page_icon="💱", layout="wide")

st.title("💱 Crypto Flows Analysis")
st.markdown("Analyse des cryptomonnaies transitant par les bridges")
st.markdown("---")

# Note sur les données
st.info(\"\"\"
📊 **Note sur les données**

Cette page affiche les cryptos qui transitent par chaque bridge. 
Les données sont agrégées par bridge et par token.

⚠️ DefiLlama API ne fournit pas les flux en temps réel par défaut. 
Cette fonctionnalité nécessite des appels API supplémentaires.
\"\"\")

# Chargement données
@st.cache_data(ttl=300)
def load_bridge_tokens():
    \"\"\"
    Charge les données de tokens par bridge
    Note: Fonction placeholder - à enrichir avec API détails bridges
    \"\"\"
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
st.warning(\"\"\"
⚠️ **Données estimées**

Les montants affichés sont des **estimations** basées sur le TVL global des bridges.
Pour des données précises par token, il faudrait :
1. Interroger l'API DefiLlama pour chaque bridge individuellement
2. Agréger les données de chaînes spécifiques
3. Potentiellement utiliser d'autres sources (Dune Analytics, The Graph)

**Hook préparé** : La structure permet facilement d'ajouter ces sources de données.
\"\"\")

# ============================================
# HOOK: Enhanced Token Data
# ============================================
# Pour améliorer avec données réelles :
# 1. Créer backend/collectors/token_flows.py
# 2. Implémenter get_bridge_token_details()
# 3. Remplacer la fonction load_bridge_tokens()
# 4. Possibilité d'intégrer Dune Analytics, The Graph
# ============================================
"""
    
    filepath = "pages/2_💱_Crypto_Flows.py"
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"   ✓ {filepath}")

def create_research_lab_page(project_dir):
    """Crée pages/3_🔬_Research_Lab.py"""
    
    content = '''"""
XRSK Platform - Research Lab
Publications et méthodologie
"""

import streamlit as st

st.set_page_config(page_title="Research Lab - XRSK", page_icon="🔬", layout="wide")

st.title("🔬 Research Lab")
st.markdown("Publications scientifiques et méthodologie de scoring")
st.markdown("---")

# Section Publications
st.header("📄 Publications")

with st.container():
    st.subheader("Framework for Cross-Chain Bridge Risk Assessment under MiCA & DORA")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown("""
        **Statut** : 🟡 En préparation - Soumission ArXiv prévue décembre 2025
        
        **Résumé**
        
        Ce papier présente un framework systématique d'évaluation des risques pour les bridges cross-chain, 
        conçu pour répondre aux exigences des régulations européennes MiCA (Markets in Crypto-Assets) 
        et DORA (Digital Operational Resilience Act).
        
        **Approche méthodologique**
        
        Le framework repose sur 5 piliers pondérés évaluant 32 métriques quantifiables :
        
        1. **Sécurité** (35%) - Audits, incidents historiques, type de validation
        2. **Liquidité** (25%) - TVL, volumes, profondeur de marché
        3. **Gouvernance** (20%) - Décentralisation, transparence, processus décisionnels
        4. **Opérationnel** (15%) - Performance technique, disponibilité, latence
        5. **Réglementaire** (5%) - Conformité, KYC/AML, juridiction
        
        **Contributions clés**
        
        - Premier framework académique aligné MiCA/DORA pour bridges DeFi
        - Méthodologie de scoring reproductible et vérifiable
        - Dataset public de 50+ bridges analysés
        - Recommandations pour régulateurs et acteurs du marché
        """)
    
    with col2:
        st.info("""
        **Auteur**
        
        Expert conformité crypto
        - Certifié AMF
        - CIF en cours
        - Spécialité : MiCA/DORA
        
        **Cible**
        
        ArXiv.org (Section: Quantitative Finance - Risk Management)
        """)

st.markdown("---")

# Section Méthodologie (simplifié pour éviter erreurs)
st.header("📊 Méthodologie de Scoring")

st.write("""
Le framework XRSK évalue les bridges cross-chain selon 5 piliers :

**1. Sécurité (35%)** - Audits, historique incidents, validation
**2. Liquidité (25%)** - TVL, volumes, profondeur marché  
**3. Gouvernance (20%)** - Décentralisation, transparence
**4. Opérationnel (15%)** - Performance, uptime, frais
**5. Réglementaire (5%)** - Conformité MiCA/DORA

Détails complets disponibles dans la publication ArXiv.
""")

st.markdown("---")
st.caption("XRSK Platform Research Lab - Contribution à une DeFi plus sûre et conforme")
'''
    
    filepath = "pages/3_🔬_Research_Lab.py"
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"   ✓ {filepath}")

def create_about_page(project_dir):
    """Crée pages/4_ℹ️_About.py"""
    
    content = '''"""
XRSK Platform - About
"""

import streamlit as st

st.set_page_config(page_title="About - XRSK", page_icon="ℹ️", layout="wide")

st.title("ℹ️ À propos de XRSK Platform")
st.markdown("---")

# Mission
st.header("🎯 Mission")

st.markdown("""
**XRSK Platform** est un projet de recherche visant à **quantifier les risques cross-chain** 
pour construire un écosystème DeFi plus sûr et conforme aux régulations européennes.

Notre objectif est de fournir aux utilisateurs, développeurs, et régulateurs des outils 
d'analyse objectifs basés sur des données vérifiables et une méthodologie scientifique rigoureuse.
""")

st.markdown("---")

# Contributeur
st.header("👤 Contributeur")

st.markdown("""
### Expert Conformité Crypto

**Fonctionnaire territorial français** - Service Finance Publique

**Certifications & Expertise**
- 🎓 Certifié AMF (Autorité des Marchés Financiers)
- 📚 CIF en cours (Conseiller en Investissement Financier)
- 🇪🇺 Expert régulations crypto : MiCA, DORA, TFR
- 💼 Spécialiste finance publique locale

**Domaines de recherche**
- Conformité réglementaire DeFi
- Évaluation des risques cross-chain
- Interopérabilité blockchain
- Finance décentralisée et régulation
""")

st.markdown("---")

# Technologies
st.header("🛠️ Stack Technique")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    **Frontend**
    - Streamlit 1.29
    - Plotly charts
    - Pandas analytics
    """)

with col2:
    st.markdown("""
    **Data Sources**
    - DefiLlama API
    - On-chain data
    - Public audits
    """)

with col3:
    st.markdown("""
    **Deployment**
    - GitHub
    - Streamlit Cloud
    - 100% gratuit
    """)

st.markdown("---")

# Contact
st.header("📬 Contact")

st.markdown("""
**GitHub**
💻 [github.com/matt2bb-collab](https://github.com/matt2bb-collab)

**LinkedIn**
💼 Connectez-vous pour échanger sur DeFi et conformité
""")

st.markdown("---")
st.caption("""
XRSK Platform v1.0 | Novembre 2025 | 
Projet de recherche personnel - Données à titre informatif uniquement
""")
'''
    
    filepath = "pages/4_ℹ️_About.py"
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"   ✓ {filepath}")

def main():
    """Fonction principale d'installation"""
    
    print("=" * 60)
    print("🚀 XRSK PLATFORM - Installation automatisée")
    print("=" * 60)
    print()
    
    # Création de l'arborescence
    project_dir = create_directory_structure()
    print()
    
    # Génération des fichiers
    print("📝 Génération des fichiers...")
    
    create_config_toml(project_dir)
    create_requirements(project_dir)
    create_gitignore(project_dir)
    create_readme(project_dir)
    
    create_backend_models(project_dir)
    create_defillama_collector(project_dir)
    create_backend_init(project_dir)
    
    create_hooks_data_sources(project_dir)
    
    create_home_page(project_dir)
    create_analytics_page(project_dir)
    create_crypto_flows_page(project_dir)
    create_research_lab_page(project_dir)
    create_about_page(project_dir)
    
    print()
    print("=" * 60)
    print("✅ Installation terminée !")
    print("=" * 60)
    print()
    print("📁 Tous les fichiers ont été créés dans le dossier actuel")
    print()
    print("🔧 Prochaines étapes :")
    print()
    print("1. Tester localement :")
    print("   pip install -r requirements.txt")
    print("   streamlit run Home.py")
    print()
    print("2. Push sur GitHub :")
    print("   git add .")
    print('   git commit -m "Initial commit XRSK Platform"')
    print("   git push origin main")
    print()
    print("3. Déployer sur Streamlit Cloud :")
    print("   - Aller sur https://streamlit.io/cloud")
    print("   - New app → Sélectionner repo xrsk-platform")
    print("   - Main file: Home.py")
    print("   - Deploy!")
    print()
    print("=" * 60)

if __name__ == "__main__":
    main()