import httpx

from models.candle import Candle
from models.market_data import MarketData


BITGET_URL = "https://api.bitget.com/api/v2/mix/market/history-candles"

TIMEFRAME_MAP = {
    "1h": "1H",
    "4h": "4H",
    "1d": "1D",
}


def get_bitget_market_data(
    symbol: str,
    timeframe: str,
    limit: int = 100
) -> MarketData:

    symbol = symbol.upper()
    timeframe = timeframe.lower()

    if timeframe not in TIMEFRAME_MAP:
        raise ValueError(
            f"Unsupported timeframe: {timeframe}. "
            f"Supported: {list(TIMEFRAME_MAP.keys())}"
        )

    if limit <= 0:
        raise ValueError("Limit must be greater than zero")

    if limit > 200:
        raise ValueError(
            "Bitget historical candle endpoint supports "
            "a maximum of 200 candles per request"
        )

    response = httpx.get(
        BITGET_URL,
        params={
            "symbol": symbol,
            "productType": "USDT-FUTURES",
            "granularity": TIMEFRAME_MAP[timeframe],
            "limit": limit,
        },
        timeout=15.0
    )

    response.raise_for_status()

    result = response.json()

    if result.get("code") != "00000":
        raise ValueError(
            f"Bitget API error: {result.get('msg')}"
        )

    data = result.get("data", [])

    if not data:
        raise ValueError(
            f"No market data found for {symbol}"
        )

    candles = []

    for item in data:

        if len(item) < 6:
            continue

        candles.append(
            Candle(
                timestamp=int(item[0]) / 1000,
                open=float(item[1]),
                high=float(item[2]),
                low=float(item[3]),
                close=float(item[4]),
                volume=float(item[5]),
            )
        )

    if not candles:
        raise ValueError(
            f"No valid candles returned for {symbol}"
        )

    # Make absolutely sure candles are chronological.
    candles.sort(key=lambda candle: candle.timestamp)

    return MarketData(
        symbol=symbol,
        timeframe=timeframe,
        candles=candles
    )