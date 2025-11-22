"""
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
"""

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
    """
    Récupère un collecteur par son nom
    
    Args:
        source: Nom de la source ('defillama', 'coingecko', etc.)
        
    Returns:
        Instance du collecteur
    """
    collector_class = AVAILABLE_COLLECTORS.get(source)
    
    if not collector_class:
        raise ValueError(f"Source inconnue: {source}. Disponibles: {list(AVAILABLE_COLLECTORS.keys())}")
    
    return collector_class()
