from models.candle import Candle
from services.return_service import calculate_returns


def analyze_returns(candles: list[Candle]) -> dict:
    returns = calculate_returns(candles)

    if not returns:
        return {
            "returns": [],
            "average_return": 0.0,
            "positive_returns": 0,
            "negative_returns": 0
        }

    positive_returns = 0
    negative_returns = 0

    for result in returns:
        if result > 0:
            positive_returns += 1
        elif result < 0:
            negative_returns += 1

    average_return = sum(returns) / len(returns)

    return {
        "returns": returns,
        "average_return": average_return,
        "positive_returns": positive_returns,
        "negative_returns": negative_returns
    }