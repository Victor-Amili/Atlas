from pydantic import BaseModel


class CandleFeatures(BaseModel):
    candle_range: float
    body_size: float
    upper_wick: float
    lower_wick: float