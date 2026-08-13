from models.candle import Candle
from models.market_analysis import MarketAnalysis

from services.analysis.return_analysis import analyze_returns
from services.analysis.volatility_analysis import calculate_volatility
from services.analysis.trend_analysis import analyze_trend


def analyze_market(candles: list[Candle]) -> MarketAnalysis:
    return_analysis = analyze_returns(candles)
    trend_analysis = analyze_trend(candles)
    volatility_analysis = calculate_volatility(candles)

    return MarketAnalysis(
        returns=return_analysis,
        volatility=volatility_analysis,
        trend=trend_analysis
    )