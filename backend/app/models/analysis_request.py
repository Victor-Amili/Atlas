from pydantic import BaseModel
from models.candle import Candle


class AnalysisRequest(BaseModel):
    candles: list[Candle]