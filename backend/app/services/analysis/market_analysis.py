from models.candle import Candle
from models.market_analysis import MarketAnalysis
from models.account import AccountConfig

from services.analysis.return_analysis import analyze_returns
from services.analysis.volatility_analysis import calculate_volatility
from services.analysis.trend_analysis import analyze_trend
from services.analysis.regime_analysis import classify_regime
from services.strategy.strategy_decision import make_strategy_decision
from services.analysis.statistical_features import calculate_return_statistics
from services.risk.position_sizing import calculate_position_size

from services.strategy.strategy_scoring import score_strategies
from services.strategy.trade_signal import generate_trade_signal
from services.risk.risk_management import calculate_risk
from services.trading.trade_decision import make_trade_decision
def analyze_market(candles: list[Candle],account: AccountConfig) -> MarketAnalysis:

    return_analysis = analyze_returns(candles)

    trend_analysis = analyze_trend(candles)

    regime = classify_regime(candles)

    volatility_analysis = calculate_volatility(candles)

    statistics = calculate_return_statistics(candles)

    strategy_scores = score_strategies(
        regime,
        volatility_analysis
    )

    strategy_decision = make_strategy_decision(
        strategy_scores,
        regime,
        statistics,
        volatility_analysis,
        len(candles)
    )

    trade_signal = generate_trade_signal(
        strategy_decision,
        regime,
        candles
    )

    risk = calculate_risk(
        trade_signal,
        candles
    )

        # UPDATE THIS BLOCK IN MARKET_ANALYSIS.PY
    position_size = calculate_position_size(
        account_balance=account.balance,
        risk_percent=account.risk_percent,
        risk_analysis=risk
    )


    trade_decision = make_trade_decision(
        strategy_decision,
        trade_signal,
        risk,
        position_size
    )

    return MarketAnalysis(
        returns=return_analysis,
        volatility=volatility_analysis,
        trend=trend_analysis,
        regime=regime,
        strategy_scores=strategy_scores,
        statistics=statistics,
        strategy=strategy_decision["strategy"],
        strategy_decision=strategy_decision,
        trade_signal=trade_signal,
        risk=risk,
        trade_decision=trade_decision
    )