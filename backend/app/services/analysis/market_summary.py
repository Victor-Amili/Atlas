from models.candle import Candle
from models.account import AccountConfig

from services.analysis.market_analysis import analyze_market


def summarize_market(
    candles: list[Candle],
    account: AccountConfig
) -> dict:

    analysis = analyze_market(candles, account)

    return {
        "trend": analysis.trend,
        "regime": analysis.regime,
        "volatility": analysis.volatility,
        "statistics": analysis.statistics,
        "strategy": analysis.strategy,
        "strategy_decision": analysis.strategy_decision,
        "trade_signal": analysis.trade_signal,
        "risk": analysis.risk,
        "position_size": analysis.position_size,
        "trade_decision": analysis.trade_decision
    }