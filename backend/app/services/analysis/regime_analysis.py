from models.candle import Candle


def determine_market_regime(candles: list[Candle]) -> str:
    if len(candles) < 2:
        return "NEUTRAL"

    first_close = candles[0].close
    last_close = candles[-1].close

    if last_close > first_close:
        return "BULLISH"

    if last_close < first_close:
        return "BEARISH"

    return "NEUTRAL"