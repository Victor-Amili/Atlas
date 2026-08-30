
from models.candle import Candle


MIN_TREND_CANDLES = 5
TREND_LOOKBACK = 50


def clamp(value: float) -> float:
    return max(0.0, min(value, 1.0))


def analyze_trend(candles: list[Candle]) -> dict:
    if len(candles) < MIN_TREND_CANDLES:
        return {
            "trend": "neutral",
            "strength": 0.0,
            "directional_strength": 0.0,
            "price_momentum": 0.0,
            "recent_momentum": 0.0,
            "rising_moves": 0,
            "falling_moves": 0,
            "reason": "Insufficient candles for trend analysis"
        }
        
    analysis_candles = candles[-TREND_LOOKBACK:]   

    rising = 0
    falling = 0

    total_up_magnitude = 0.0
    total_down_magnitude = 0.0

    for i in range(1, len(analysis_candles)):
        previous_close = analysis_candles[i - 1].close
        current_close = analysis_candles[i].close

        if previous_close <= 0:
            continue

        price_change = (
            (current_close - previous_close)
            / previous_close
        )

        if price_change > 0:
            rising += 1
            total_up_magnitude += price_change

        elif price_change < 0:
            falling += 1
            total_down_magnitude += abs(price_change)

    total_moves = rising + falling

    if total_moves == 0:
        return {
            "trend": "neutral",
            "strength": 0.0,
            "directional_strength": 0.0,
            "price_momentum": 0.0,
            "recent_momentum": 0.0,
            "rising_moves": 0,
            "falling_moves": 0,
            "reason": "No directional price movement detected"
        }

    # ---------------------------------------------------------
    # DIRECTION
    # ---------------------------------------------------------

    first_close = analysis_candles[0].close
    latest_close = analysis_candles[-1].close

    if first_close > 0:
        total_price_change = (
            (latest_close - first_close)
            / first_close
        )
    else:
        total_price_change = 0.0

    if total_price_change > 0:
        trend = "bullish"

    elif total_price_change < 0:
        trend = "bearish"

    else:
        trend = "neutral"


    # ---------------------------------------------------------
    # DIRECTIONAL CONSISTENCY
    # ---------------------------------------------------------

    directional_strength = (
        abs(rising - falling)
        / total_moves
    )


    # ---------------------------------------------------------
    # PRICE MOMENTUM
    # ---------------------------------------------------------

    price_momentum = clamp(
        abs(total_price_change) / 0.02
    )

    # ---------------------------------------------------------
    # MAGNITUDE BALANCE
    # ---------------------------------------------------------

    total_magnitude = (
        total_up_magnitude
        + total_down_magnitude
    )

    if total_magnitude > 0:

        if trend == "bullish":
            magnitude_strength = (
                total_up_magnitude
                / total_magnitude
            )

        elif trend == "bearish":
            magnitude_strength = (
                total_down_magnitude
                / total_magnitude
            )

        else:
            magnitude_strength = 0.0

    else:
        magnitude_strength = 0.0

    # ---------------------------------------------------------
    # RECENT MOMENTUM
    # ---------------------------------------------------------

    recent_window = min(5, len(analysis_candles) - 1)

    recent_rising = 0
    recent_falling = 0

    for i in range(
        len(analysis_candles) - recent_window,
        len(analysis_candles)
    ):
        previous_close = analysis_candles[i - 1].close
        current_close = analysis_candles[i].close

        if current_close > previous_close:
            recent_rising += 1

        elif current_close < previous_close:
            recent_falling += 1

    recent_total = (
        recent_rising
        + recent_falling
    )

    if recent_total > 0:
        recent_momentum = (
            abs(recent_rising - recent_falling)
            / recent_total
        )
    else:
        recent_momentum = 0.0

    # ---------------------------------------------------------
    # COMBINED TREND STRENGTH
    # ---------------------------------------------------------

    strength = (
        directional_strength * 0.30
        + magnitude_strength * 0.30
        + price_momentum * 0.25
        + recent_momentum * 0.15
    )

    strength = clamp(strength)

    return {
        "trend": trend,
        "strength": round(strength, 4),
        "directional_strength": round(
            directional_strength,
            4
        ),
        "magnitude_strength": round(
            magnitude_strength,
            4
        ),
        "price_momentum": round(
            price_momentum,
            4
        ),
        "recent_momentum": round(
            recent_momentum,
            4
        ),
        "price_change_percent": round(
            total_price_change * 100,
            4
        ),
        "rising_moves": rising,
        "falling_moves": falling
    }