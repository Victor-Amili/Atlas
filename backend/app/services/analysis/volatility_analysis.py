from models.candle import Candle


def calculate_volatility(candles: list[Candle]) -> dict:
    if len(candles) < 2:
        return {
            "volatility": 0.0,
            "average_range": 0.0
        }

    ranges = []

    for candle in candles:
        candle_range = candle.high - candle.low
        ranges.append(candle_range)

    average_range = sum(ranges) / len(ranges)

    return {
        "volatility": average_range,
        "average_range": average_range
    }