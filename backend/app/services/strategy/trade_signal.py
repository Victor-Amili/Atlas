from models.candle import Candle


def generate_trade_signal(
    strategy_decision: dict,
    regime_analysis: dict,
    candles: list[Candle]
) -> dict:

    strategy = strategy_decision.get("strategy", "NO_STRATEGY")
    regime = regime_analysis.get("regime", "UNKNOWN")
    confidence = strategy_decision.get("confidence", 0.0)

    if len(candles) < 2:
        return {
            "action": "HOLD",
            "direction": "NONE",
            "confidence": confidence,
            "reason": "Insufficient candles for entry confirmation"
        }

    previous_close = candles[-2].close
    latest_close = candles[-1].close

    latest_return = (
        (latest_close - previous_close) / previous_close
    )

    if strategy == "NO_STRATEGY":
        return {
            "action": "HOLD",
            "direction": "NONE",
            "confidence": confidence,
            "reason": "No valid strategy available"
        }

    if strategy == "TREND_FOLLOWING":

        if regime == "BULL_TREND":

            if latest_close > previous_close:
                return {
                    "action": "BUY",
                    "direction": "LONG",
                    "confidence": confidence,
                    "latest_return": latest_return,
                    "entry_confirmed": True,
                    "reason": "Bullish trend confirmed by latest upward price movement"
                }

            return {
                "action": "HOLD",
                "direction": "NONE",
                "confidence": confidence,
                "latest_return": latest_return,
                "entry_confirmed": False,
                "reason": "Bullish trend exists but latest price movement does not confirm entry"
            }

        if regime == "BEAR_TREND":

            if latest_close < previous_close:
                return {
                    "action": "SELL",
                    "direction": "SHORT",
                    "confidence": confidence,
                    "latest_return": latest_return,
                    "entry_confirmed": True,
                    "reason": "Bearish trend confirmed by latest downward price movement"
                }

            return {
                "action": "HOLD",
                "direction": "NONE",
                "confidence": confidence,
                "latest_return": latest_return,
                "entry_confirmed": False,
                "reason": "Bearish trend exists but latest price movement does not confirm entry"
            }

    if strategy == "BREAKOUT":
        return {
            "action": "HOLD",
            "direction": "PENDING",
            "confidence": confidence,
            "latest_return": latest_return,
            "entry_confirmed": False,
            "reason": "Breakout strategy selected; breakout confirmation required"
        }

    if strategy == "MEAN_REVERSION":
        return {
            "action": "HOLD",
            "direction": "PENDING",
            "confidence": confidence,
            "latest_return": latest_return,
            "entry_confirmed": False,
            "reason": "Mean-reversion strategy selected; reversal confirmation required"
        }

    return {
        "action": "HOLD",
        "direction": "NONE",
        "confidence": confidence,
        "latest_return": latest_return,
        "entry_confirmed": False,
        "reason": "No actionable trade signal"
    }