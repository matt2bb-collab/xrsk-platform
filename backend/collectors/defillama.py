"""
DefiLlama Collector - Récupération données bridges
"""

import requests
from datetime import datetime
from typing import List, Dict, Optional

class DefiLlamaCollector:
    """
    Collecteur de données depuis l'API DefiLlama
    """
    
    BASE_URL = "https://bridges.llama.fi"
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'XRSK-Platform/1.0'
        })
    
    def get_all_bridges(self) -> Optional[List[Dict]]:
        """
        Récupère la liste complète des bridges depuis DefiLlama
        """
        try:
            response = self.session.get(
                f"{self.BASE_URL}/bridges",
                timeout=10
            )
            response.raise_for_status()
            
            data = response.json()
            bridges = data.get('bridges', [])
            
            print(f"✓ {len(bridges)} bridges récupérés depuis DefiLlama")
            return bridges
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Erreur DefiLlama API: {e}")
            return None
        except Exception as e:
            print(f"❌ Erreur inattendue: {e}")
            return None
    
    def get_formatted_bridges(self) -> List[Dict]:
        """
        Retourne les bridges formatés pour l'affichage
        Mapping correct des champs API DefiLlama
        """
        bridges = self.get_all_bridges()
        
        if not bridges:
            return []
        
        formatted = []
        for bridge in bridges:
            # Mapping correct des champs
            formatted_bridge = {
                'id': bridge.get('id', 0),
                'name': bridge.get('displayName', bridge.get('name', 'Unknown')),
                'tvl': bridge.get('tvl', 0),  # Peut être 0 si non dispo
                'volume_24h': bridge.get('last24hVolume', bridge.get('lastDailyVolume', 0)),  # Corrigé
                'volume_7d': bridge.get('weeklyVolume', 0),
                'volume_30d': bridge.get('monthlyVolume', 0),
                'chains': bridge.get('chains', []),
                'chains_count': len(bridge.get('chains', [])),
                'last_updated': datetime.now()
            }
            formatted.append(formatted_bridge)
        
        return formatted
    
    def get_bridge_details(self, bridge_id: int) -> Optional[Dict]:
        """
        Récupère les détails d'un bridge spécifique
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
