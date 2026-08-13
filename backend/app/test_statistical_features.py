from datetime import datetime, timedelta

from models.candle import Candle
from services.analysis.statistical_features import calculate_return_statistics


candles = []

start_time = datetime(2026, 8, 13, 10, 0, 0)

prices = [100, 105, 102, 108, 110]

for i, price in enumerate(prices):

    candle = Candle(
        timestamp=start_time + timedelta(hours=i),
        open=price,
        high=price + 5,
        low=price - 5,
        close=price,
        volume=1000
    )

    candles.append(candle)


result = calculate_return_statistics(candles)

print(result)