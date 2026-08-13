from models.candle import Candle
from services.analysis.volatility_analysis import calculate_volatility


HIGH_VOLATILITY_THRESHOLD = 10


def classify_regime(candles: list[Candle]) -> str:
    if len(candles) < 2:
        return "INSUFFICIENT_DATA"

    volatility_analysis = calculate_volatility(candles)
    volatility = volatility_analysis["volatility"]

    if volatility > HIGH_VOLATILITY_THRESHOLD:
        return "HIGH_VOLATILITY"

    rising_moves = 0
    falling_moves = 0

    for i in range(1, len(candles)):
        previous_close = candles[i - 1].close
        current_close = candles[i].close

        if current_close > previous_close:
            rising_moves += 1
        elif current_close < previous_close:
            falling_moves += 1

    if rising_moves > falling_moves:
        return "BULL_TREND"

    if falling_moves > rising_moves:
        return "BEAR_TREND"

    return "RANGE"