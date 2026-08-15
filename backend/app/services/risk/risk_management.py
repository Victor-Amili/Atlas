from models.candle import Candle


MIN_RISK_REWARD_RATIO = 2.0


def calculate_risk(
    trade_signal: dict,
    candles: list[Candle]
) -> dict:

    if len(candles) < 2:
        return {
            "valid": False,
            "reason": "Insufficient candles for risk calculation"
        }

    action = trade_signal.get("action", "HOLD")

    if action not in ["BUY", "SELL"]:
        return {
            "valid": False,
            "reason": "No active trade signal"
        }

    latest_candle = candles[-1]

    entry_price = latest_candle.close

    if action == "BUY":

        stop_loss = latest_candle.low

        risk = entry_price - stop_loss

        if risk <= 0:
            return {
                "valid": False,
                "reason": "Invalid stop-loss for long position"
            }

        take_profit = entry_price + (risk * MIN_RISK_REWARD_RATIO)

    else:

        stop_loss = latest_candle.high

        risk = stop_loss - entry_price

        if risk <= 0:
            return {
                "valid": False,
                "reason": "Invalid stop-loss for short position"
            }

        take_profit = entry_price - (risk * MIN_RISK_REWARD_RATIO)

    reward = abs(take_profit - entry_price)

    risk_reward_ratio = reward / risk

    return {
        "valid": risk_reward_ratio >= MIN_RISK_REWARD_RATIO,
        "entry_price": entry_price,
        "stop_loss": stop_loss,
        "take_profit": take_profit,
        "risk": risk,
        "reward": reward,
        "risk_reward_ratio": risk_reward_ratio,
        "minimum_required_ratio": MIN_RISK_REWARD_RATIO
    }