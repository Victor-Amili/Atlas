from models.candle import Candle
from models.market_analysis import MarketAnalysis

from services.analysis.return_analysis import analyze_returns
from services.analysis.volatility_analysis import calculate_volatility


def analyze_market(candles: list[Candle]) -> MarketAnalysis:
    return_analysis = analyze_returns(candles)

    volatility_analysis = calculate_volatility(candles)

    return MarketAnalysis(
        returns=return_analysis,
        volatility=volatility_analysis
    )