
from models.candle import Candle

from services.analysis.volatility_analysis import calculate_volatility
from services.analysis.trend_analysis import analyze_trend


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
            "volatility_percent": 0.0,
            "price_change_percent": 0.0,
            "rising_moves": 0,
            "falling_moves": 0,
            "reason": "Insufficient candles for regime analysis"
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
    # TREND ANALYSIS
    # -----------------------------------------------------

    trend_analysis = analyze_trend(candles)

    trend = trend_analysis.get(
        "trend",
        "neutral"
    )

    trend_strength = trend_analysis.get(
        "strength",
        0.0
    )

    price_change_percent = trend_analysis.get(
        "price_change_percent",
        0.0
    )

    rising_moves = trend_analysis.get(
        "rising_moves",
        0
    )

    falling_moves = trend_analysis.get(
        "falling_moves",
        0
    )

    directional_strength = trend_analysis.get(
        "directional_strength",
        0.0
    )

    magnitude_strength = trend_analysis.get(
        "magnitude_strength",
        0.0
    )

    price_momentum = trend_analysis.get(
        "price_momentum",
        0.0
    )

    recent_momentum = trend_analysis.get(
        "recent_momentum",
        0.0
    )

    # -----------------------------------------------------
    # BULL TREND
    # -----------------------------------------------------

    if (
        trend == "bullish"
        and trend_strength >= MIN_TREND_STRENGTH
    ):
        return {
            "regime": "BULL_TREND",
            "confidence": round(trend_strength, 4),
            "trend_strength": round(trend_strength, 4),
            "volatility_percent": round(
                volatility_percent,
                4
            ),
            "price_change_percent": round(
                price_change_percent,
                4
            ),
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
            "rising_moves": rising_moves,
            "falling_moves": falling_moves,
            "reason": (
                "Bullish trend confirmed by price displacement "
                "and trend strength"
            )
        }

    # -----------------------------------------------------
    # BEAR TREND
    # -----------------------------------------------------

    if (
        trend == "bearish"
        and trend_strength >= MIN_TREND_STRENGTH
    ):
        return {
            "regime": "BEAR_TREND",
            "confidence": round(trend_strength, 4),
            "trend_strength": round(trend_strength, 4),
            "volatility_percent": round(
                volatility_percent,
                4
            ),
            "price_change_percent": round(
                price_change_percent,
                4
            ),
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
            "rising_moves": rising_moves,
            "falling_moves": falling_moves,
            "reason": (
                "Bearish trend confirmed by price displacement "
                "and trend strength"
            )
        }

    # -----------------------------------------------------
    # HIGH VOLATILITY
    # -----------------------------------------------------

    if volatility_percent >= HIGH_VOLATILITY_PERCENT:
        return {
            "regime": "HIGH_VOLATILITY",
            "confidence": round(trend_strength, 4),
            "trend_strength": round(trend_strength, 4),
            "volatility_percent": round(
                volatility_percent,
                4
            ),
            "price_change_percent": round(
                price_change_percent,
                4
            ),
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
            "rising_moves": rising_moves,
            "falling_moves": falling_moves,
            "reason": (
                "Volatility is high but directional trend "
                "strength is insufficient for trend regime"
            )
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
        "rising_moves": rising_moves,
        "falling_moves": falling_moves,
        "reason": (
            "No sufficiently strong directional trend "
            "detected"
        )
    }

