from datetime import datetime, timedelta

from models.candle import Candle
from services.analysis.regime_analysis import classify_regime


start_time = datetime(2026, 8, 13, 10, 0, 0)

candles = []

prices = [100, 102, 104, 106, 108]

for i, price in enumerate(prices):
    candles.append(
        Candle(
            timestamp=start_time + timedelta(hours=i),
            open=price,
            high=price + 10,
            low=price - 10,
            close=price,
            volume=1000
        )
    )


result = classify_regime(candles)

print(result)