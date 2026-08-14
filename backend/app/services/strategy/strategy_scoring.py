def score_strategies(regime_analysis: dict) -> dict:

    regime = regime_analysis["regime"]
    confidence = regime_analysis["confidence"]

    scores = {
        "TREND_FOLLOWING": 0.0,
        "BREAKOUT": 0.0,
        "MEAN_REVERSION": 0.0
    }

    if regime == "BULL_TREND":
        scores["TREND_FOLLOWING"] = confidence

    elif regime == "BEAR_TREND":
        scores["TREND_FOLLOWING"] = confidence

    elif regime == "HIGH_VOLATILITY":
        scores["BREAKOUT"] = confidence

    elif regime == "RANGE":
        scores["MEAN_REVERSION"] = confidence

    return scores


MIN_STRATEGY_SCORE = 0.5


def select_best_strategy(scores: dict) -> str:

    if not scores:
        return "NO_STRATEGY"

    best_strategy = max(scores, key=scores.get)

    if scores[best_strategy] < MIN_STRATEGY_SCORE:
        return "NO_STRATEGY"

    return best_strategy