from pydantic import BaseModel


class MarketAnalysis(BaseModel):
    returns: dict
    volatility: dict
    trend: dict
    regime: dict
    strategy: str