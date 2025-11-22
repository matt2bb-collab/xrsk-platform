"""
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
