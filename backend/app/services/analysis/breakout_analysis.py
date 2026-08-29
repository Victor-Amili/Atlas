from models.candle import Candle


BREAKOUT_LOOKBACK = 20


def analyze_breakout(candles: list[Candle]) -> dict:

    if len(candles) < BREAKOUT_LOOKBACK + 1:
        return {
            "breakout": "NONE",
            "score": 0.0,
            "confidence": 0.0,
            "resistance": None,
            "support": None,
            "latest_close": None,
            "reason": (
                f"Insufficient candles for breakout analysis. "
                f"Need at least {BREAKOUT_LOOKBACK + 1}"
            )
        }

    latest_candle = candles[-1]
    latest_close = latest_candle.close

    lookback_candles = candles[-(BREAKOUT_LOOKBACK + 1):-1]

    resistance = max(
        candle.high for candle in lookback_candles
    )

    support = min(
        candle.low for candle in lookback_candles
    )

    price_range = resistance - support

    if price_range <= 0:
        return {
            "breakout": "NONE",
            "score": 0.0,
            "confidence": 0.0,
            "resistance": resistance,
            "support": support,
            "latest_close": latest_close,
            "reason": "Invalid support/resistance range"
        }

    # ---------------------------------------------------------
    # CONFIRMED BULLISH BREAKOUT
    # ---------------------------------------------------------

    if latest_close > resistance:

        return {
            "breakout": "BULLISH",
            "score": 1.0,
            "confidence": 1.0,
            "resistance": resistance,
            "support": support,
            "latest_close": latest_close,
            "reason": (
                f"Price closed above resistance "
                f"{resistance:.2f}"
            )
        }

    # ---------------------------------------------------------
    # CONFIRMED BEARISH BREAKOUT
    # ---------------------------------------------------------

    if latest_close < support:

        return {
            "breakout": "BEARISH",
            "score": 1.0,
            "confidence": 1.0,
            "resistance": resistance,
            "support": support,
            "latest_close": latest_close,
            "reason": (
                f"Price closed below support "
                f"{support:.2f}"
            )
        }

    # ---------------------------------------------------------
    # DISTANCE FROM RESISTANCE / SUPPORT
    # ---------------------------------------------------------

    distance_to_resistance = (
        resistance - latest_close
    ) / price_range

    distance_to_support = (
        latest_close - support
    ) / price_range

    proximity = max(
        0.0,
        1.0 - min(
            distance_to_resistance,
            distance_to_support
        )
    )

    return {
        "breakout": "NONE",
        "score": round(proximity * 0.5, 4),
        "confidence": 0.0,
        "resistance": resistance,
        "support": support,
        "latest_close": latest_close,
        "reason": (
            "No confirmed breakout; price remains "
            "inside the recent support/resistance range"
        )
    }