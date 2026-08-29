def make_trade_decision(
    strategy_decision: dict,
    trade_signal: dict,
    risk: dict,
    position_size: dict,
) -> dict:

    strategy = strategy_decision.get("strategy", "NO_STRATEGY")

    if strategy == "NO_STRATEGY":
        return {
            "decision": "HOLD",
            "action": "NONE",
            "reason": "No valid strategy available"
        }

    if not trade_signal.get("entry_confirmed", False):
        return {
            "decision": "HOLD",
            "action": "NONE",
            "reason": "Trade entry has not been confirmed"
        }

    if not risk.get("valid", False):
        return {
            "decision": "HOLD",
            "action": "NONE",
            "reason": "Risk analysis failed"
        }

    if not position_size.get("valid", False):
        return {
            "decision": "HOLD",
            "action": "NONE",
            "reason": "Position sizing failed"
        }

    return {
        "decision": "ENTER",
        "action": trade_signal.get("action", "NONE"),
        "direction": trade_signal.get("direction", "NONE"),
        "strategy": strategy,
        "entry_price": risk.get("entry_price"),
        "stop_loss": risk.get("stop_loss"),
        "take_profit": risk.get("take_profit"),
        "position_size": position_size.get("position_size"),
        "position_value": position_size.get("position_value"),
        "risk": risk.get("risk"),
        "reward": risk.get("reward"),
        "risk_reward_ratio": risk.get("risk_reward_ratio"),
        "confidence": strategy_decision.get("confidence", 0.0),
        "reason": (
            "Strategy, entry confirmation, risk management "
            "and position sizing all passed"
        )
    }