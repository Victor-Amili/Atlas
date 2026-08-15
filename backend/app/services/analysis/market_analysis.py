from models.candle import Candle
from models.market_analysis import MarketAnalysis

from services.analysis.return_analysis import analyze_returns
from services.analysis.volatility_analysis import calculate_volatility
from services.analysis.trend_analysis import analyze_trend
from services.analysis.regime_analysis import classify_regime
from services.strategy.strategy_decision import make_strategy_decision
from services.analysis.statistical_features import calculate_return_statistics

from services.strategy.strategy_scoring import score_strategies

def analyze_market(candles: list[Candle]) -> MarketAnalysis:
    return_analysis = analyze_returns(candles)

    trend_analysis = analyze_trend(candles)

    regime = classify_regime(candles)

    volatility_analysis = calculate_volatility(candles)
    
    statistics = calculate_return_statistics(candles)

    strategy_scores = score_strategies(regime, volatility_analysis)

   
    strategy_decision = make_strategy_decision(strategy_scores, regime, 
                                               statistics, volatility_analysis, len(candles))

    return MarketAnalysis(
        returns=return_analysis,
        volatility=volatility_analysis,
        trend=trend_analysis,
        regime=regime,
        strategy_scores=strategy_scores,
        statistics=statistics,
        strategy = strategy_decision["strategy"],    
        strategy_decision=strategy_decision
    )