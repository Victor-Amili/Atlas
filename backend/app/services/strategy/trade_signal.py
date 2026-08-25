# from models.candle import Candle


# def generate_trade_signal(
#     strategy_decision: dict,
#     regime_analysis: dict,
#     candles: list[Candle]
# ) -> dict:

#     strategy = strategy_decision.get("strategy", "NO_STRATEGY")
#     regime = regime_analysis.get("regime", "UNKNOWN")
#     confidence = strategy_decision.get("confidence", 0.0)

#     if len(candles) < 2:
#         return {
#             "action": "HOLD",
#             "direction": "NONE",
#             "confidence": confidence,
#             "reason": "Insufficient candles for entry confirmation"
#         }

#     previous_close = candles[-2].close
#     latest_close = candles[-1].close

#     latest_return = (
#         (latest_close - previous_close) / previous_close
#     )

#     if strategy == "NO_STRATEGY":
#         return {
#             "action": "HOLD",
#             "direction": "NONE",
#             "confidence": confidence,
#             "reason": "No valid strategy available"
#         }

#     if strategy == "TREND_FOLLOWING":

#         if regime == "BULL_TREND":

#             if latest_close > previous_close:
#                 return {
#                     "action": "BUY",
#                     "direction": "LONG",
#                     "confidence": confidence,
#                     "latest_return": latest_return,
#                     "entry_confirmed": True,
#                     "reason": "Bullish trend confirmed by latest upward price movement"
#                 }

#             return {
#                 "action": "HOLD",
#                 "direction": "NONE",
#                 "confidence": confidence,
#                 "latest_return": latest_return,
#                 "entry_confirmed": False,
#                 "reason": "Bullish trend exists but latest price movement does not confirm entry"
#             }

#         if regime == "BEAR_TREND":

#             if latest_close < previous_close:
#                 return {
#                     "action": "SELL",
#                     "direction": "SHORT",
#                     "confidence": confidence,
#                     "latest_return": latest_return,
#                     "entry_confirmed": True,
#                     "reason": "Bearish trend confirmed by latest downward price movement"
#                 }

#             return {
#                 "action": "HOLD",
#                 "direction": "NONE",
#                 "confidence": confidence,
#                 "latest_return": latest_return,
#                 "entry_confirmed": False,
#                 "reason": "Bearish trend exists but latest price movement does not confirm entry"
#             }

#     if strategy == "BREAKOUT":
#         return {
#             "action": "HOLD",
#             "direction": "PENDING",
#             "confidence": confidence,
#             "latest_return": latest_return,
#             "entry_confirmed": False,
#             "reason": "Breakout strategy selected; breakout confirmation required"
#         }

#     if strategy == "MEAN_REVERSION":
#         return {
#             "action": "HOLD",
#             "direction": "PENDING",
#             "confidence": confidence,
#             "latest_return": latest_return,
#             "entry_confirmed": False,
#             "reason": "Mean-reversion strategy selected; reversal confirmation required"
#         }

#     return {
#         "action": "HOLD",
#         "direction": "NONE",
#         "confidence": confidence,
#         "latest_return": latest_return,
#         "entry_confirmed": False,
#         "reason": "No actionable trade signal"
#     }

from models.candle import Candle


MIN_SIGNAL_CONFIDENCE = 0.50
BREAKOUT_LOOKBACK = 20


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
            "entry_confirmed": False,
            "reason": "Insufficient candles for entry confirmation"
        }

    previous_close = candles[-2].close
    latest_candle = candles[-1]
    latest_close = latest_candle.close

    latest_return = (
        (latest_close - previous_close) / previous_close
    )

    if strategy == "NO_STRATEGY":
        return {
            "action": "HOLD",
            "direction": "NONE",
            "confidence": confidence,
            "latest_return": latest_return,
            "entry_confirmed": False,
            "reason": "No valid strategy available"
        }

    # ---------------------------------------------------------
    # CONFIDENCE FILTER
    # ---------------------------------------------------------

    if confidence < MIN_SIGNAL_CONFIDENCE:
        return {
            "action": "HOLD",
            "direction": "NONE",
            "confidence": confidence,
            "latest_return": latest_return,
            "entry_confirmed": False,
            "reason": (
                f"Signal confidence {confidence:.2f} is below "
                f"minimum required confidence {MIN_SIGNAL_CONFIDENCE:.2f}"
            )
        }

    # ---------------------------------------------------------
    # TREND FOLLOWING
    # ---------------------------------------------------------

    if strategy == "TREND_FOLLOWING":

        if regime == "BULL_TREND":

            if latest_close > previous_close:
                return {
                    "action": "BUY",
                    "direction": "LONG",
                    "confidence": confidence,
                    "latest_return": latest_return,
                    "entry_confirmed": True,
                    "reason": (
                        "Bullish trend confirmed by latest upward "
                        "price movement"
                    )
                }

            return {
                "action": "HOLD",
                "direction": "NONE",
                "confidence": confidence,
                "latest_return": latest_return,
                "entry_confirmed": False,
                "reason": (
                    "Bullish trend exists but latest price movement "
                    "does not confirm entry"
                )
            }

        if regime == "BEAR_TREND":

            if latest_close < previous_close:
                return {
                    "action": "SELL",
                    "direction": "SHORT",
                    "confidence": confidence,
                    "latest_return": latest_return,
                    "entry_confirmed": True,
                    "reason": (
                        "Bearish trend confirmed by latest downward "
                        "price movement"
                    )
                }

            return {
                "action": "HOLD",
                "direction": "NONE",
                "confidence": confidence,
                "latest_return": latest_return,
                "entry_confirmed": False,
                "reason": (
                    "Bearish trend exists but latest price movement "
                    "does not confirm entry"
                )
            }

    # ---------------------------------------------------------
    # BREAKOUT
    # ---------------------------------------------------------

    if strategy == "BREAKOUT":

        if len(candles) < BREAKOUT_LOOKBACK + 1:
            return {
                "action": "HOLD",
                "direction": "PENDING",
                "confidence": confidence,
                "latest_return": latest_return,
                "entry_confirmed": False,
                "reason": (
                    f"Breakout requires at least "
                    f"{BREAKOUT_LOOKBACK + 1} candles"
                )
            }

        # Exclude the current candle when calculating
        # previous resistance/support.
        lookback_candles = candles[-(BREAKOUT_LOOKBACK + 1):-1]

        resistance = max(
            candle.high for candle in lookback_candles
        )

        support = min(
            candle.low for candle in lookback_candles
        )

        # Bullish breakout
        if latest_close > resistance:

            return {
                "action": "BUY",
                "direction": "LONG",
                "confidence": confidence,
                "latest_return": latest_return,
                "entry_confirmed": True,
                "breakout_level": resistance,
                "reason": (
                    f"Bullish breakout confirmed: "
                    f"close {latest_close:.2f} broke above "
                    f"resistance {resistance:.2f}"
                )
            }

        # Bearish breakout
        if latest_close < support:

            return {
                "action": "SELL",
                "direction": "SHORT",
                "confidence": confidence,
                "latest_return": latest_return,
                "entry_confirmed": True,
                "breakout_level": support,
                "reason": (
                    f"Bearish breakout confirmed: "
                    f"close {latest_close:.2f} broke below "
                    f"support {support:.2f}"
                )
            }

        return {
            "action": "HOLD",
            "direction": "PENDING",
            "confidence": confidence,
            "latest_return": latest_return,
            "entry_confirmed": False,
            "resistance": resistance,
            "support": support,
            "reason": (
                "No confirmed breakout: price remains "
                "inside the recent support/resistance range"
            )
        }

    # ---------------------------------------------------------
    # MEAN REVERSION
    # ---------------------------------------------------------

    if strategy == "MEAN_REVERSION":
        return {
            "action": "HOLD",
            "direction": "PENDING",
            "confidence": confidence,
            "latest_return": latest_return,
            "entry_confirmed": False,
            "reason": (
                "Mean-reversion strategy selected; "
                "reversal confirmation required"
            )
        }

    return {
        "action": "HOLD",
        "direction": "NONE",
        "confidence": confidence,
        "latest_return": latest_return,
        "entry_confirmed": False,
        "reason": "No actionable trade signal"
    }