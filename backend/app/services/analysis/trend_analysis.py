from models.candle import Candle


def analyze_trend(candles: list[Candle]) -> dict:
    if len(candles) < 2:
        return {
            "trend": "neutral",
            "strength": 0.0
        }

    rising = 0
    falling = 0

    for i in range(1, len(candles)):
        previous_close = candles[i - 1].close
        current_close = candles[i].close

        if current_close > previous_close:
            rising += 1

        elif current_close < previous_close:
            falling += 1

    total_moves = rising + falling

    if total_moves == 0:
        return {
            "trend": "neutral",
            "strength": 0.0
        }

    if rising > falling:
        trend = "bullish"
    elif falling > rising:
        trend = "bearish"
    else:
        trend = "neutral"

    strength = abs(rising - falling) / total_moves

    return {
        "trend": trend,
        "strength": strength,
        "rising_moves": rising,
        "falling_moves": falling
    }