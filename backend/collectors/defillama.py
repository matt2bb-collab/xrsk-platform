"""
Collecteur de données DefiLlama
"""

import requests
from typing import List, Dict, Optional
from datetime import datetime

class DefiLlamaCollector:
    """Collecteur de données bridges depuis DefiLlama API"""
    
    BASE_URL = "https://bridges.llama.fi"
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'XRSK-Platform/1.0'
        })
    
    def get_all_bridges(self) -> Optional[List[Dict]]:
        """
        Récupère la liste complète des bridges
        
        Returns:
            Liste de dictionnaires avec données bridges
        """
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
        """
        Récupère les détails d'un bridge spécifique
        
        Args:
            bridge_id: ID du bridge
            
        Returns:
            Dictionnaire avec détails du bridge
        """
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
        """
        Récupère les volumes d'un bridge
        
        Args:
            bridge_id: ID du bridge
            
        Returns:
            Données de volume
        """
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
        """
        Formate les données brutes DefiLlama
        
        Args:
            raw_data: Données brutes de l'API
            
        Returns:
            Données formatées
        """
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
        """
        Récupère et formate tous les bridges
        
        Returns:
            Liste de bridges formatés
        """
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
