from pydantic import BaseModel


class MarketAnalysis(BaseModel):
    returns: dict
    volatility: dict
    trend: dict
    regime: dict
    strategy_scores: dict
    strategy: str