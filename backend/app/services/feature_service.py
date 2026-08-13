from models.candle import Candle
from models.candle_features import CandleFeatures


def calculate_candle_features(candle: Candle) -> CandleFeatures:
    candle_range = candle.high - candle.low

    body_size = abs(candle.close - candle.open)

    upper_wick = candle.high - max(candle.open, candle.close)

    lower_wick = min(candle.open, candle.close) - candle.low

    return CandleFeatures(
        candle_range=candle_range,
        body_size=body_size,
        upper_wick=upper_wick,
        lower_wick=lower_wick
    )