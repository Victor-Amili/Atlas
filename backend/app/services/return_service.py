from models.candle import Candle


def calculate_return(previous_close: float, current_close: float) -> float:
    return (current_close - previous_close) / previous_close


def calculate_returns(candles: list[Candle]) -> list[float]:
    returns = []

    for i in range(1, len(candles)):
        previous_close = candles[i - 1].close
        current_close = candles[i].close

        result = calculate_return(previous_close, current_close)

        returns.append(result)

    return returns