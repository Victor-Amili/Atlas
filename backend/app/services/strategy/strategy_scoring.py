MIN_STRATEGY_SCORE = 0.5

# Volatility percentage ranges
LOW_VOLATILITY_PERCENT = 0.50
HIGH_VOLATILITY_PERCENT = 1.00


def score_strategies(
    regime_analysis: dict,
    volatility_analysis: dict
) -> dict:

    regime = regime_analysis.get("regime", "UNKNOWN")
    confidence = regime_analysis.get("confidence", 0.0)

    volatility_percent = volatility_analysis.get(
        "volatility_percent",
        0.0
    )

    scores = {
        "TREND_FOLLOWING": 0.0,
        "BREAKOUT": 0.0,
        "MEAN_REVERSION": 0.0
    }

    # ---------------------------------------------------------
    # TREND FOLLOWING
    # ---------------------------------------------------------

    if regime == "BULL_TREND":
        scores["TREND_FOLLOWING"] = confidence

    elif regime == "BEAR_TREND":
        scores["TREND_FOLLOWING"] = confidence

    # ---------------------------------------------------------
    # HIGH VOLATILITY / BREAKOUT
    # ---------------------------------------------------------

    elif regime == "HIGH_VOLATILITY":

        if volatility_percent <= LOW_VOLATILITY_PERCENT:

            breakout_score = 0.0

        elif volatility_percent >= HIGH_VOLATILITY_PERCENT:

            breakout_score = 1.0

        else:

            breakout_score = (
                (volatility_percent - LOW_VOLATILITY_PERCENT)
                /
                (HIGH_VOLATILITY_PERCENT - LOW_VOLATILITY_PERCENT)
            )

        scores["BREAKOUT"] = breakout_score

    # ---------------------------------------------------------
    # RANGE / MEAN REVERSION
    # ---------------------------------------------------------

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