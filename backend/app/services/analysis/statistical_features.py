from models.candle import Candle


def calculate_return_statistics(candles: list[Candle]) -> dict:

    if len(candles) < 2:
        return {
            "average_return": 0.0,
            "maximum_return": 0.0,
            "minimum_return": 0.0
        }

    returns = []

    for i in range(1, len(candles)):

        previous_close = candles[i - 1].close
        current_close = candles[i].close

        price_return = (current_close - previous_close) / previous_close

        returns.append(price_return)

    return {
        "average_return": sum(returns) / len(returns),
        "maximum_return": max(returns),
        "minimum_return": min(returns)
    }