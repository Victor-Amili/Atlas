from services.trading.trade_decision import make_trade_decision


trade_signal = {
    "action": "BUY",
    "direction": "LONG",
    "confidence": 1.0,
    "entry_confirmed": True
}


strategy_decision = {
    "strategy": "TREND_FOLLOWING",
    "score": 1.0,
    "confidence": 1.0
}


risk_analysis = {
    "valid": True,
    "entry_price": 105,
    "stop_loss": 103,
    "take_profit": 109,
    "risk": 2,
    "reward": 4,
    "risk_reward_ratio": 2.0
}


position_size = {
    "valid": True,
    "account_balance": 100000,
    "risk_percent": 0.01,
    "maximum_loss": 1000,
    "risk_per_unit": 2,
    "position_size": 500,
    "position_value": 52500
}


result = make_trade_decision(
    trade_signal,
    strategy_decision,
    risk_analysis,
    position_size
)


print(result)