def generate_trade_signal(
    strategy_decision: dict,
    regime_analysis: dict
) -> dict:

    strategy = strategy_decision.get("strategy", "NO_STRATEGY")
    regime = regime_analysis.get("regime", "UNKNOWN")
    confidence = strategy_decision.get("confidence", 0.0)

    if strategy == "NO_STRATEGY":
        return {
            "action": "HOLD",
            "direction": "NONE",
            "confidence": confidence,
            "reason": "No valid strategy available"
        }

    if strategy == "TREND_FOLLOWING":

        if regime == "BULL_TREND":
            return {
                "action": "BUY",
                "direction": "LONG",
                "confidence": confidence,
                "reason": "Bullish trend supports trend-following long position"
            }

        if regime == "BEAR_TREND":
            return {
                "action": "SELL",
                "direction": "SHORT",
                "confidence": confidence,
                "reason": "Bearish trend supports trend-following short position"
            }

    if strategy == "BREAKOUT":
        return {
            "action": "HOLD",
            "direction": "PENDING",
            "confidence": confidence,
            "reason": "Breakout strategy selected; waiting for breakout confirmation"
        }

    if strategy == "MEAN_REVERSION":
        return {
            "action": "HOLD",
            "direction": "PENDING",
            "confidence": confidence,
            "reason": "Mean-reversion strategy selected; waiting for reversal confirmation"
        }

    return {
        "action": "HOLD",
        "direction": "NONE",
        "confidence": confidence,
        "reason": "No actionable trade signal"
    }