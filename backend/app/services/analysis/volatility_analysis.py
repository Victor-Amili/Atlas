from models.candle import Candle


def calculate_volatility(candles: list[Candle]) -> dict:
    if len(candles) < 2:
        return {
            "volatility": 0.0,
            "average_range": 0.0,
            "volatility_percent": 0.0
        }

    ranges = []

    for candle in candles:
        candle_range = candle.high - candle.low
        ranges.append(candle_range)

    average_range = sum(ranges) / len(ranges)

    average_price = sum(
        candle.close for candle in candles
    ) / len(candles)

    if average_price == 0:
        volatility_percent = 0.0
    else:
        volatility_percent = (
            average_range / average_price
        ) * 100

    return {
        "volatility": average_range,
        "average_range": average_range,
        "volatility_percent": volatility_percent
    }