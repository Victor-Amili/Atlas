from models.candle import Candle


MIN_SIGNAL_CONFIDENCE = 0.50
BREAKOUT_LOOKBACK = 20

MIN_BREAKOUT_PERCENT = 0.20
MIN_BODY_PERCENT = 0.50

MEAN_REVERSION_LOOKBACK = 20

MEAN_REVERSION_ZONE_PERCENT = 0.25

MIN_REVERSION_BODY_RATIO = 0.30


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
    # TREND FOLLOWING
    # ---------------------------------------------------------

    if strategy == "TREND_FOLLOWING":

        if confidence + 1e-9 < MIN_SIGNAL_CONFIDENCE:
            return {
                "action": "HOLD",
                "direction": "NONE",
                "confidence": confidence,
                "latest_return": latest_return,
                "entry_confirmed": False,
                "reason": (
                    f"Trend signal confidence {confidence:.4f} "
                    f"is below minimum required confidence "
                    f"{MIN_SIGNAL_CONFIDENCE:.4f}"
                )
            }

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
                "entry_confirmed": False,
                "reason": (
                    f"Breakout requires at least "
                    f"{BREAKOUT_LOOKBACK + 1} candles"
                )
            }

        lookback_candles = candles[
            -(BREAKOUT_LOOKBACK + 1):-1
        ]

        resistance = max(
            candle.high for candle in lookback_candles
        )

        support = min(
            candle.low for candle in lookback_candles
        )

        # -----------------------------------------------------
        # CURRENT CANDLE
        # -----------------------------------------------------

        candle_open = latest_candle.open
        candle_high = latest_candle.high
        candle_low = latest_candle.low
        candle_close = latest_candle.close

        candle_range = candle_high - candle_low

        if candle_range <= 0:
            return {
                "action": "HOLD",
                "direction": "PENDING",
                "confidence": confidence,
                "entry_confirmed": False,
                "resistance": resistance,
                "support": support,
                "reason": "Invalid latest candle range"
            }

        candle_body = abs(candle_close - candle_open)

        body_ratio = candle_body / candle_range

        # -----------------------------------------------------
        # VOLUME ANALYSIS
        # -----------------------------------------------------

        average_volume = (
            sum(candle.volume for candle in lookback_candles)
            / len(lookback_candles)
        )

        latest_volume = latest_candle.volume

        if average_volume > 0:
            volume_ratio = latest_volume / average_volume
        else:
            volume_ratio = 0.0

        # Volume score capped between 0 and 1.
        volume_score = min(volume_ratio / 2.0, 1.0)

        # -----------------------------------------------------
        # MOMENTUM
        # -----------------------------------------------------

        average_body = (
            sum(
                abs(candle.close - candle.open)
                for candle in lookback_candles
            )
            / len(lookback_candles)
        )

        if average_body > 0:
            momentum_ratio = candle_body / average_body
        else:
            momentum_ratio = 0.0

        momentum_score = min(momentum_ratio / 2.0, 1.0)

        # -----------------------------------------------------
        # BREAKOUT DISTANCE
        # -----------------------------------------------------

        bullish_breakout_percent = (
            (candle_close - resistance) / resistance
        ) * 100

        bearish_breakout_percent = (
            (support - candle_close) / support
        ) * 100

        # -----------------------------------------------------
        # BULLISH BREAKOUT
        # -----------------------------------------------------

        if candle_close > resistance:

            body_score = min(
                body_ratio / MIN_BODY_PERCENT,
                1.0
            )

            distance_score = min(
                bullish_breakout_percent
                / MIN_BREAKOUT_PERCENT,
                1.0
            )

            breakout_confidence = (
                distance_score * 0.25
                + body_score * 0.25
                + volume_score * 0.25
                + momentum_score * 0.25
            )

            body_confirmed = (
                body_ratio >= MIN_BODY_PERCENT
            )
            
            effective_confidence = min(
                confidence,
              breakout_confidence
            )

            distance_confirmed = (
                bullish_breakout_percent
                >= MIN_BREAKOUT_PERCENT
            )

            if body_confirmed and distance_confirmed and effective_confidence >= MIN_SIGNAL_CONFIDENCE:

                return {
                    "action": "BUY",
                    "direction": "LONG",
                    "confidence": confidence,
                    "breakout_confidence": breakout_confidence,
                    "latest_return": latest_return,
                    "entry_confirmed": True,
                    "breakout_level": resistance,
                    "breakout_percent": bullish_breakout_percent,
                    "body_ratio": body_ratio,
                    "volume_ratio": volume_ratio,
                    "momentum_ratio": momentum_ratio,
                    "reason": (
                        f"Bullish breakout confirmed: "
                        f"close {candle_close:.2f} broke above "
                        f"resistance {resistance:.2f} by "
                        f"{bullish_breakout_percent:.2f}%. "
                        f"Breakout confidence: "
                        f"{breakout_confidence:.2f}"
                    )
                }

            return {
                "action": "HOLD",
                "direction": "PENDING",
                "confidence": confidence,
                "breakout_confidence": breakout_confidence,
                "latest_return": latest_return,
                "entry_confirmed": False,
                "resistance": resistance,
                "support": support,
                "breakout_percent": bullish_breakout_percent,
                "body_ratio": body_ratio,
                "volume_ratio": volume_ratio,
                "momentum_ratio": momentum_ratio,
                "reason": (
                    "Price broke resistance but breakout "
                    "confirmation conditions were not satisfied"
                )
            }

        # -----------------------------------------------------
        # BEARISH BREAKOUT
        # -----------------------------------------------------

        if candle_close < support:

            body_score = min(
                body_ratio / MIN_BODY_PERCENT,
                1.0
            )

            distance_score = min(
                bearish_breakout_percent
                / MIN_BREAKOUT_PERCENT,
                1.0
            )

            breakout_confidence = (
                distance_score * 0.25
                + body_score * 0.25
                + volume_score * 0.25
                + momentum_score * 0.25
            )

            body_confirmed = (
                body_ratio >= MIN_BODY_PERCENT
            )
            
            effective_confidence = min(
                confidence,
                breakout_confidence
            )

            distance_confirmed = (
                bearish_breakout_percent
                >= MIN_BREAKOUT_PERCENT
            )

            if body_confirmed and distance_confirmed and effective_confidence >= MIN_SIGNAL_CONFIDENCE:

                return {
                    "action": "SELL",
                    "direction": "SHORT",
                    "confidence": confidence,
                    "breakout_confidence": breakout_confidence,
                    "latest_return": latest_return,
                    "entry_confirmed": True,
                    "breakout_level": support,
                    "breakout_percent": bearish_breakout_percent,
                    "body_ratio": body_ratio,
                    "volume_ratio": volume_ratio,
                    "momentum_ratio": momentum_ratio,
                    "reason": (
                        f"Bearish breakout confirmed: "
                        f"close {candle_close:.2f} broke below "
                        f"support {support:.2f} by "
                        f"{bearish_breakout_percent:.2f}%. "
                        f"Breakout confidence: "
                        f"{breakout_confidence:.2f}"
                    )
                }

            return {
                "action": "HOLD",
                "direction": "PENDING",
                "confidence": confidence,
                "breakout_confidence": breakout_confidence,
                "latest_return": latest_return,
                "entry_confirmed": False,
                "resistance": resistance,
                "support": support,
                "breakout_percent": bearish_breakout_percent,
                "body_ratio": body_ratio,
                "volume_ratio": volume_ratio,
                "momentum_ratio": momentum_ratio,
                "reason": (
                    "Price broke support but breakdown "
                    "confirmation conditions were not satisfied"
                )
            }

        # -----------------------------------------------------
        # NO BREAKOUT
        # -----------------------------------------------------

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

        if regime != "RANGE":
            return {
                "action": "HOLD",
                "direction": "NONE",
                "confidence": confidence,
                "latest_return": latest_return,
                "entry_confirmed": False,
                "reason": "Mean-reversion requires a RANGE regime"
            }

        if len(candles) < MEAN_REVERSION_LOOKBACK + 1:
            return {
                "action": "HOLD",
                "direction": "PENDING",
                "confidence": confidence,
                "latest_return": latest_return,
                "entry_confirmed": False,
                "reason": (
                    f"Mean reversion requires at least "
                    f"{MEAN_REVERSION_LOOKBACK + 1} candles"
                )
            }

        # -----------------------------------------------------
        # RECENT RANGE
        # -----------------------------------------------------

        lookback_candles = candles[
            -(MEAN_REVERSION_LOOKBACK + 1):-1
        ]

        resistance = max(
            candle.high for candle in lookback_candles
        )

        support = min(
            candle.low for candle in lookback_candles
        )

        range_size = resistance - support

        if range_size <= 0:
            return {
                "action": "HOLD",
                "direction": "PENDING",
                "confidence": confidence,
                "latest_return": latest_return,
                "entry_confirmed": False,
                "reason": "Invalid range for mean reversion"
            }

        # -----------------------------------------------------
        # CURRENT CANDLE
        # -----------------------------------------------------

        candle_open = latest_candle.open
        candle_high = latest_candle.high
        candle_low = latest_candle.low
        candle_close = latest_candle.close

        candle_range = candle_high - candle_low

        if candle_range <= 0:
            return {
                "action": "HOLD",
                "direction": "PENDING",
                "confidence": confidence,
                "latest_return": latest_return,
                "entry_confirmed": False,
                "reason": "Invalid latest candle range"
            }

        candle_body = abs(
            candle_close - candle_open
        )

        body_ratio = candle_body / candle_range

        # -----------------------------------------------------
        # DISTANCE FROM SUPPORT / RESISTANCE
        # -----------------------------------------------------

        support_distance_percent = (
            (candle_close - support) / support
        ) * 100

        resistance_distance_percent = (
            (resistance - candle_close) / resistance
        ) * 100

        # -----------------------------------------------------
        # REVERSAL ZONES
        # -----------------------------------------------------

        near_support = (
            candle_close <=
            support * (
                1 + MEAN_REVERSION_ZONE_PERCENT / 100
            )
        )

        near_resistance = (
            candle_close >=
            resistance * (
                1 - MEAN_REVERSION_ZONE_PERCENT / 100
            )
        )

        # -----------------------------------------------------
        # BULLISH REVERSAL
        # -----------------------------------------------------

        bullish_candle = (
            candle_close > candle_open
        )

        if near_support and bullish_candle:

            if body_ratio >= MIN_REVERSION_BODY_RATIO:

                return {
                    "action": "BUY",
                    "direction": "LONG",
                    "confidence": confidence,
                    "latest_return": latest_return,
                    "entry_confirmed": True,
                    "support": support,
                    "resistance": resistance,
                    "body_ratio": body_ratio,
                    "reason": (
                        f"Mean-reversion BUY confirmed: "
                        f"price is near support {support:.2f} "
                        f"and latest candle shows bullish reversal"
                    )
                }

        # -----------------------------------------------------
        # BEARISH REVERSAL
        # -----------------------------------------------------

        bearish_candle = (
            candle_close < candle_open
        )

        if near_resistance and bearish_candle:

            if body_ratio >= MIN_REVERSION_BODY_RATIO:

                return {
                    "action": "SELL",
                    "direction": "SHORT",
                    "confidence": confidence,
                    "latest_return": latest_return,
                    "entry_confirmed": True,
                    "support": support,
                    "resistance": resistance,
                    "body_ratio": body_ratio,
                    "reason": (
                        f"Mean-reversion SELL confirmed: "
                        f"price is near resistance {resistance:.2f} "
                        f"and latest candle shows bearish reversal"
                    )
                }

        # -----------------------------------------------------
        # NO REVERSAL
        # -----------------------------------------------------

        return {
            "action": "HOLD",
            "direction": "PENDING",
            "confidence": confidence,
            "latest_return": latest_return,
            "entry_confirmed": False,
            "support": support,
            "resistance": resistance,
            "body_ratio": body_ratio,
            "support_distance_percent": support_distance_percent,
            "resistance_distance_percent": resistance_distance_percent,
            "reason": (
                "Mean-reversion selected but price has not "
                "confirmed a reversal near support or resistance"
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