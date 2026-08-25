import httpx

from models.candle import Candle
from models.market_data import MarketData


COINGECKO_URL = "https://api.coingecko.com/api/v3"


COIN_MAP = {
    "BTCUSDT": "bitcoin",
    "ETHUSDT": "ethereum",
    "SOLUSDT": "solana",
    "BNBUSDT": "binancecoin",
    "ADAUSDT": "cardano",
    "XRPUSDT": "ripple",
    "DOGEUSDT": "dogecoin",
    "AVAXUSDT": "avalanche-2",
    "DOTUSDT": "polkadot",
    "LINKUSDT": "chainlink",
}


TIMEFRAME_MAP = {
    "1h": 1,
    "4h": 4,
    "1d": 24,
}


def get_market_data(
    symbol: str,
    timeframe: str,
    limit: int = 100
) -> MarketData:

    symbol = symbol.upper()
    timeframe = timeframe.lower()

    if symbol not in COIN_MAP:
        raise ValueError(
            f"Unsupported crypto symbol: {symbol}"
        )

    if timeframe not in TIMEFRAME_MAP:
        raise ValueError(
            f"Unsupported timeframe: {timeframe}. "
            f"Supported: {list(TIMEFRAME_MAP.keys())}"
        )

    coin_id = COIN_MAP[symbol]

    response = httpx.get(
        f"{COINGECKO_URL}/coins/{coin_id}/ohlc",
        params={
            "vs_currency": "usd",
            "days": "7"
        },
        timeout=15.0
    )

    response.raise_for_status()

    data = response.json()

    if not data:
        raise ValueError(
            f"No market data found for {symbol}"
        )

    candles = []

    for item in data:

        timestamp = item[0] / 1000

        candles.append(
            Candle(
                timestamp=timestamp,
                open=float(item[1]),
                high=float(item[2]),
                low=float(item[3]),
                close=float(item[4]),
                volume=0.0
            )
        )

    # Keep the requested number of candles.
    candles = candles[-limit:]

    return MarketData(
        symbol=symbol,
        timeframe=timeframe,
        candles=candles
    )