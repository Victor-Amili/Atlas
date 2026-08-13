from datetime import datetime, timedelta

from models.candle import Candle
from models.market_data import MarketData


def get_sample_market_data() -> MarketData:
    candles = []

    start_time = datetime(2026, 8, 12, 10, 0, 0)

    for i in range(5):
        candle = Candle(
            timestamp=start_time + timedelta(hours=i),
            open=100 + i,
            high=105 + i,
            low=95 + i,
            close=103 + i,
            volume=1000 + (i * 100)
        )

        candles.append(candle)

    return MarketData(
        symbol="BTCUSD",
        timeframe="1h",
        candles=candles
    )