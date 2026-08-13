from models.candle import Candle
from services.analysis.volatility_analysis import calculate_volatility


HIGH_VOLATILITY_THRESHOLD = 10


def classify_regime(candles: list[Candle]) -> dict:

    if len(candles) < 2:
        return {
            "regime": "INSUFFICIENT_DATA",
            "confidence": 0.0,
            "rising_moves": 0,
            "falling_moves": 0
        }

    volatility_analysis = calculate_volatility(candles)
    volatility = volatility_analysis["volatility"]

    rising_moves = 0
    falling_moves = 0

    for i in range(1, len(candles)):

        previous_close = candles[i - 1].close
        current_close = candles[i].close

        if current_close > previous_close:
            rising_moves += 1

        elif current_close < previous_close:
            falling_moves += 1

    total_moves = rising_moves + falling_moves

    if total_moves == 0:
        confidence = 0.0
    else:
        confidence = abs(rising_moves - falling_moves) / total_moves

    if volatility > HIGH_VOLATILITY_THRESHOLD:

        return {
            "regime": "HIGH_VOLATILITY",
            "confidence": confidence,
            "rising_moves": rising_moves,
            "falling_moves": falling_moves
        }

    if rising_moves > falling_moves:

        return {
            "regime": "BULL_TREND",
            "confidence": confidence,
            "rising_moves": rising_moves,
            "falling_moves": falling_moves
        }

    if falling_moves > rising_moves:

        return {
            "regime": "BEAR_TREND",
            "confidence": confidence,
            "rising_moves": rising_moves,
            "falling_moves": falling_moves
        }

    return {
        "regime": "RANGE",
        "confidence": confidence,
        "rising_moves": rising_moves,
        "falling_moves": falling_moves
    }