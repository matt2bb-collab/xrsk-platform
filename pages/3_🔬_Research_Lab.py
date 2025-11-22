"""
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
