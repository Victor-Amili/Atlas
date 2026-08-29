MIN_STRATEGY_SCORE = 0.5
MIN_BREAKOUT_VOLATILITY = 10
MAX_MEAN_REVERSION_RETURN = 0.01
MIN_CANDLES_FOR_STRATEGY = 5


def make_strategy_decision(
    scores: dict,
    regime_analysis: dict,
    statistics: dict,
    volatility_analysis: dict,
    candle_count: int
) -> dict:
    
    if candle_count < MIN_CANDLES_FOR_STRATEGY:
        return {
            "strategy": "NO_STRATEGY",
            "score": 0.0,
            "confidence": 0.0,
            "reason": "Insufficient market data for strategy analysis",
            "conditions": {
                "minimum_score": False,
                "sufficient_data": False
            }
        }

    if not scores:
        return {
            "strategy": "NO_STRATEGY",
            "score": 0.0,
            "confidence": 0.0,
            "reason": "No strategy scores available",
            "conditions": {
                "minimum_score": False,
                "sufficient_data": True
            }
        }

    best_strategy = max(scores, key=scores.get)
    best_score = scores[best_strategy]

    confidence = regime_analysis.get("confidence", 0.0)
    average_return = statistics.get("average_return", 0.0)
    regime = regime_analysis.get("regime", "UNKNOWN")
    volatility = volatility_analysis.get("volatility", 0.0)

    if best_score < MIN_STRATEGY_SCORE:
        return {
            "strategy": "NO_STRATEGY",
            "score": best_score,
            "confidence": confidence,
            "reason": "Strategy confidence below minimum threshold", 
            "conditions": {
                 "minimum_score": False,
                "sufficient_data": candle_count >= MIN_CANDLES_FOR_STRATEGY
            }
        }

    if best_strategy == "TREND_FOLLOWING":

        return {
            "strategy": best_strategy,
            "score": best_score,
            "confidence": confidence,
            "reason": f"{regime} with strong confidence and sufficient average return",
            "conditions": {
                "minimum_score": True,
                "sufficient_data": candle_count >= MIN_CANDLES_FOR_STRATEGY,
                "average_return_valid": True
            }
        }

    if best_strategy == "BREAKOUT":

        if volatility < MIN_BREAKOUT_VOLATILITY:
            return {
                "strategy": "NO_STRATEGY",
                "score": best_score,
                "confidence": confidence,
                "reason": "Volatility is too weak for breakout strategy",
                "conditions": {
                    "minimum_score": True,
                    "sufficient_data": candle_count >= MIN_CANDLES_FOR_STRATEGY,
                    "volatility_valid": False
                }
            }

        return {
            "strategy": best_strategy,
            "score": best_score,
            "confidence": confidence,
            "reason": (
                f"{regime} with volatility {volatility:.2f} "
                f"and breakout score {best_score:.2f}"
            ),
            "conditions": {
                "minimum_score": True,
                "sufficient_data": candle_count >= MIN_CANDLES_FOR_STRATEGY,
                "volatility_valid": True
            }
        }

    if best_strategy == "MEAN_REVERSION":

        if abs(average_return) > MAX_MEAN_REVERSION_RETURN:
         return {
            "strategy": "NO_STRATEGY",
            "score": best_score,
            "confidence": confidence,
            "reason": "Average return is too strong for mean reversion",
            "conditions": {
                "minimum_score": True,
                "sufficient_data": candle_count >= MIN_CANDLES_FOR_STRATEGY,
                "average_return_valid": False
            }
        }

        return {
            "strategy": best_strategy,
            "score": best_score,
            "confidence": confidence,
            "reason": (
                f"{regime} with controlled average return "
                f"of {average_return:.4f}"
            ),
            "conditions": {
                "minimum_score": True,
                "sufficient_data": candle_count >= MIN_CANDLES_FOR_STRATEGY,
                "average_return_valid": True
            }
        }

    return {
        "strategy": "NO_STRATEGY",
        "score": best_score,
        "confidence": confidence,
        "reason": "No suitable strategy found",
        "conditions": {
            "minimum_score": False,
            "sufficient_data": False,
            "average_return_valid": False
        }
    }