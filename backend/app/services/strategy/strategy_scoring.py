MIN_STRATEGY_SCORE = 0.5


def score_strategies(
    regime_analysis: dict,
    volatility_analysis: dict
) -> dict:

    regime = regime_analysis["regime"]
    confidence = regime_analysis["confidence"]
    volatility = volatility_analysis.get("volatility", 0.0)

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

        # Higher volatility = stronger breakout suitability
        if volatility >= 10:
            breakout_score = min(volatility / 20, 1.0)
            scores["BREAKOUT"] = breakout_score

    elif regime == "RANGE":
        scores["MEAN_REVERSION"] = 1.0 - confidence

    return scores


def select_best_strategy(scores: dict) -> str:

    if not scores:
        return "NO_STRATEGY"

    best_strategy = max(scores, key=scores.get)

    if scores[best_strategy] < MIN_STRATEGY_SCORE:
        return "NO_STRATEGY"

    return best_strategy