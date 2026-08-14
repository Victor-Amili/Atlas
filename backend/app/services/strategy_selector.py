def select_strategy(regime_analysis: dict) -> str:

    regime = regime_analysis["regime"]
    confidence = regime_analysis["confidence"]

    MIN_CONFIDENCE = 0.6

    if confidence < MIN_CONFIDENCE:
        return "NO_STRATEGY"

    if regime == "BULL_TREND":
        return "TREND_FOLLOWING"

    if regime == "BEAR_TREND":
        return "TREND_FOLLOWING"

    if regime == "HIGH_VOLATILITY":
        return "BREAKOUT"

    if regime == "RANGE":
        return "MEAN_REVERSION"

    return "NO_STRATEGY"