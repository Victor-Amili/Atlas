from models.candle import Candle

from services.analysis.volatility_analysis import calculate_volatility


# ---------------------------------------------------------
# REGIME THRESHOLDS
# ---------------------------------------------------------

MIN_TREND_STRENGTH = 0.20
HIGH_VOLATILITY_PERCENT = 1.00

LOOKBACK = 20


def classify_regime(candles: list[Candle]) -> dict:

    if len(candles) < LOOKBACK + 1:
        return {
            "regime": "INSUFFICIENT_DATA",
            "confidence": 0.0,
            "trend_strength": 0.0,
            "rising_moves": 0,
            "falling_moves": 0
        }

    # -----------------------------------------------------
    # VOLATILITY
    # -----------------------------------------------------

    volatility_analysis = calculate_volatility(candles)

    volatility_percent = volatility_analysis.get(
        "volatility_percent",
        0.0
    )

    # -----------------------------------------------------
    # USE RECENT MARKET DATA
    # -----------------------------------------------------

    recent_candles = candles[-(LOOKBACK + 1):]

    rising_moves = 0
    falling_moves = 0

    for i in range(1, len(recent_candles)):

        previous_close = recent_candles[i - 1].close
        current_close = recent_candles[i].close

        if current_close > previous_close:
            rising_moves += 1

        elif current_close < previous_close:
            falling_moves += 1

    total_moves = rising_moves + falling_moves

    # -----------------------------------------------------
    # DIRECTIONAL CONSISTENCY
    # -----------------------------------------------------

    if total_moves > 0:

        directional_consistency = (
            abs(rising_moves - falling_moves)
            / total_moves
        )

    else:

        directional_consistency = 0.0

    # -----------------------------------------------------
    # PRICE DISPLACEMENT
    # -----------------------------------------------------

    start_price = recent_candles[0].close
    latest_price = recent_candles[-1].close

    if start_price > 0:

        price_change_percent = (
            (latest_price - start_price)
            / start_price
        ) * 100

    else:

        price_change_percent = 0.0

    # -----------------------------------------------------
    # PRICE RANGE
    # -----------------------------------------------------

    highest_price = max(
        candle.high for candle in recent_candles
    )

    lowest_price = min(
        candle.low for candle in recent_candles
    )

    if lowest_price > 0:

        total_range_percent = (
            (highest_price - lowest_price)
            / lowest_price
        ) * 100

    else:

        total_range_percent = 0.0

    # -----------------------------------------------------
    # NORMALIZED PRICE DISPLACEMENT
    #
    # Measures how much of the total range the market
    # actually travelled in one direction.
    # -----------------------------------------------------

    if total_range_percent > 0:

        displacement_strength = min(
            abs(price_change_percent)
            / total_range_percent,
            1.0
        )

    else:

        displacement_strength = 0.0

    # -----------------------------------------------------
    # COMBINED TREND STRENGTH
    # -----------------------------------------------------

    trend_strength = (
        directional_consistency * 0.40
        +
        displacement_strength * 0.60
    )

    trend_strength = min(
        trend_strength,
        1.0
    )

    # -----------------------------------------------------
    # DETERMINE DIRECTION
    # -----------------------------------------------------

    if price_change_percent > 0:

        direction = "BULLISH"

    elif price_change_percent < 0:

        direction = "BEARISH"

    else:

        direction = "NEUTRAL"

    # -----------------------------------------------------
    # TREND
    # -----------------------------------------------------

    if trend_strength >= MIN_TREND_STRENGTH:

        if direction == "BULLISH":

            return {
                "regime": "BULL_TREND",
                "confidence": round(
                    trend_strength,
                    4
                ),
                "trend_strength": round(
                    trend_strength,
                    4
                ),
                "volatility_percent": round(
                    volatility_percent,
                    4
                ),
                "price_change_percent": round(
                    price_change_percent,
                    4
                ),
                "rising_moves": rising_moves,
                "falling_moves": falling_moves
            }

        if direction == "BEARISH":

            return {
                "regime": "BEAR_TREND",
                "confidence": round(
                    trend_strength,
                    4
                ),
                "trend_strength": round(
                    trend_strength,
                    4
                ),
                "volatility_percent": round(
                    volatility_percent,
                    4
                ),
                "price_change_percent": round(
                    price_change_percent,
                    4
                ),
                "rising_moves": rising_moves,
                "falling_moves": falling_moves
            }

    # -----------------------------------------------------
    # HIGH VOLATILITY
    # -----------------------------------------------------

    if volatility_percent >= HIGH_VOLATILITY_PERCENT:

        return {
            "regime": "HIGH_VOLATILITY",
            "confidence": round(
                trend_strength,
                4
            ),
            "trend_strength": round(
                trend_strength,
                4
            ),
            "volatility_percent": round(
                volatility_percent,
                4
            ),
            "price_change_percent": round(
                price_change_percent,
                4
            ),
            "rising_moves": rising_moves,
            "falling_moves": falling_moves
        }

    # -----------------------------------------------------
    # RANGE
    # -----------------------------------------------------

    return {
        "regime": "RANGE",
        "confidence": round(
            trend_strength,
            4
        ),
        "trend_strength": round(
            trend_strength,
            4
        ),
        "volatility_percent": round(
            volatility_percent,
            4
        ),
        "price_change_percent": round(
            price_change_percent,
            4
        ),
        "rising_moves": rising_moves,
        "falling_moves": falling_moves
    }