import time
from datetime import datetime, timezone

import httpx

from models.candle import Candle
from models.market_data import MarketData


BITGET_URL = (
    "https://api.bitget.com/api/v2/mix/market/history-candles"
)


PRODUCT_TYPE = "USDT-FUTURES"


SUPPORTED_TIMEFRAMES = {
    "1h": "1H",
    "4h": "4H",
    "1d": "1D",
}


def get_market_data(
    symbol: str,
    timeframe: str,
    limit: int = 100
) -> MarketData:

    symbol = symbol.upper()
    timeframe = timeframe.lower()

    if timeframe not in SUPPORTED_TIMEFRAMES:
        raise ValueError(
            f"Unsupported timeframe: {timeframe}. "
            f"Supported: {list(SUPPORTED_TIMEFRAMES.keys())}"
        )

    if limit <= 0:
        raise ValueError(
            "Limit must be greater than zero"
        )

    candles = []

    remaining = limit

    end_time = None

    while remaining > 0:

        batch_size = min(100, remaining)

        params = {
            "symbol": symbol,
            "productType": PRODUCT_TYPE,
            "granularity": SUPPORTED_TIMEFRAMES[timeframe],
            "limit": batch_size,
        }

        if end_time is not None:
            params["endTime"] = end_time

        response = httpx.get(
            BITGET_URL,
            params=params,
            timeout=15.0
        )

        response.raise_for_status()

        payload = response.json()

        if payload.get("code") != "00000":
            raise ValueError(
                f"Bitget API error: {payload}"
            )

        data = payload.get("data", [])

        if not data:
            break

        for item in data:

            candles.append(
                Candle(
                    timestamp=datetime.fromtimestamp(
                        int(item[0]) / 1000,
                        tz=timezone.utc
                    ),
                    open=float(item[1]),
                    high=float(item[2]),
                    low=float(item[3]),
                    close=float(item[4]),
                    volume=float(item[5])
                )
            )

        oldest_timestamp = min(
            int(item[0])
            for item in data
        )

        end_time = str(
            oldest_timestamp - 1
        )

        remaining -= len(data)

        if len(data) < batch_size:
            break

        time.sleep(0.1)

    # Remove duplicate timestamps
    unique_candles = {
        candle.timestamp: candle
        for candle in candles
    }

    candles = list(
        unique_candles.values()
    )

    # Chronological order
    candles.sort(
        key=lambda candle: candle.timestamp
    )

    # Keep exactly the requested amount
    candles = candles[-limit:]

    return MarketData(
        symbol=symbol,
        timeframe=timeframe,
        candles=candles
    )