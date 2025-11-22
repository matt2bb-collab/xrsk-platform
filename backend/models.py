"""
Modèles de données pour XRSK Platform
"""

from dataclasses import dataclass
from typing import Optional, Dict, List
from datetime import datetime

@dataclass
class BridgeData:
    """Données d'un bridge cross-chain"""
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
        """Score total pondéré"""
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
    """Flux crypto d'un bridge"""
    bridge_id: str
    bridge_name: str
    token_symbol: str
    amount: float
    usd_value: float
    from_chain: str
    to_chain: str
    timestamp: datetime
