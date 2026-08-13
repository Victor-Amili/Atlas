from pydantic import BaseModel

from models.candle import Candle


class MarketData(BaseModel):
    symbol: str
    timeframe: str
    candles: list[Candle]