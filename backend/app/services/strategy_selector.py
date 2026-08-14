

def select_strategy(regime: dict) -> str:
    regime_name = regime["regime"]  # Ensure the regime is classified before selecting a strategy

    if regime_name == "BULL_TREND":
        
        return "TREND_FOLLOWING"

    if regime_name  == "BEAR_TREND":
        return "TREND_FOLLOWING"

    if regime_name == "HIGH_VOLATILITY":
        return "BREAKOUT"

    if regime_name == "RANGE":
        return "MEAN_REVERSION"

    return "NO_STRATEGY"