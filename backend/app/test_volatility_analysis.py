from datetime import datetime

from models.candle import Candle
from services.analysis.volatility_analysis import calculate_volatility


candles = [
    Candle(
        timestamp=datetime(2026, 8, 12, 10, 0),
        open=100,
        high=105,
        low=95,
        close=103,
        volume=1000
    ),
    Candle(
        timestamp=datetime(2026, 8, 12, 11, 0),
        open=103,
        high=110,
        low=100,
        close=108,
        volume=1200
    ),
    Candle(
        timestamp=datetime(2026, 8, 12, 12, 0),
        open=108,
        high=112,
        low=104,
        close=110,
        volume=1300
    )
]

result = calculate_volatility(candles)

print("Volatility Analysis:")
print(result)