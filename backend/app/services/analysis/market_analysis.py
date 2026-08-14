from models.candle import Candle
from models.market_analysis import MarketAnalysis

from services.analysis.return_analysis import analyze_returns
from services.analysis.volatility_analysis import calculate_volatility
from services.analysis.trend_analysis import analyze_trend
from services.analysis.regime_analysis import classify_regime

from services.strategy.strategy_scoring import (
    score_strategies,
    select_best_strategy
)


def analyze_market(candles: list[Candle]) -> MarketAnalysis:
    return_analysis = analyze_returns(candles)

    trend_analysis = analyze_trend(candles)

    regime = classify_regime(candles)

    volatility_analysis = calculate_volatility(candles)

    strategy_scores = score_strategies(regime)

    strategy = select_best_strategy(strategy_scores)

    return MarketAnalysis(
        returns=return_analysis,
        volatility=volatility_analysis,
        trend=trend_analysis,
        regime=regime,
        strategy_scores=strategy_scores,
        strategy=strategy
    )