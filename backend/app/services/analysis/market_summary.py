from models.candle import Candle

from services.analysis.trend_analysis import analyze_trend
from services.analysis.regime_analysis import classify_regime
from services.analysis.volatility_analysis import calculate_volatility
from services.analysis.statistical_features import calculate_return_statistics


def summarize_market(candles: list[Candle]) -> dict:

    trend = analyze_trend(candles)
    regime = classify_regime(candles)
    volatility = calculate_volatility(candles)
    statistics = calculate_return_statistics(candles)

    return {
        "trend": trend,
        "regime": regime,
        "volatility": volatility,
        "statistics": statistics
    }