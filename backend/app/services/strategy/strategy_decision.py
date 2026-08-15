MIN_STRATEGY_SCORE = 0.5
MIN_AVERAGE_RETURN = 0.01


def make_strategy_decision(
    scores: dict,
    regime_analysis: dict,
    statistics: dict
) -> dict:

    if not scores:
        return {
            "strategy": "NO_STRATEGY",
            "score": 0.0,
            "confidence": 0.0,
            "reason": "No strategy scores available"
        }

    best_strategy = max(scores, key=scores.get)
    best_score = scores[best_strategy]

    confidence = regime_analysis.get("confidence", 0.0)
    average_return = statistics.get("average_return", 0.0)

    if best_score < MIN_STRATEGY_SCORE:
        return {
            "strategy": "NO_STRATEGY",
            "score": best_score,
            "confidence": confidence,
            "reason": "Strategy confidence below minimum threshold"
        }

    if best_strategy == "TREND_FOLLOWING":
        if average_return < MIN_AVERAGE_RETURN:
            return {
                "strategy": "NO_STRATEGY",
                "score": best_score,
                "confidence": confidence,
                "reason": "Average return is too weak for trend following"
            }

    return {
        "strategy": best_strategy,
        "score": best_score,
        "confidence": confidence,
        "reason": "Strategy passed statistical validation"
    }