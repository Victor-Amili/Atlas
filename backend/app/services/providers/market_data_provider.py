
# import httpx

# from models.candle import Candle
# from models.market_data import MarketData


# BINANCE_URL = "https://api.binance.com/api/v3/kline"


# def get_market_data(
#     symbol: str,
#     timeframe: str,
#     limit: int = 100
# ) -> MarketData:

#     params = {
#         "symbol": symbol.upper(),
#         "interval": timeframe,
#         "limit": limit
#     }

#     response = httpx.get(
#         BINANCE_URL,
#         params=params,
#         timeout=10.0
#     )

#     response.raise_for_status()

#     data = response.json()

#     candles = []

#     for item in data:
#         candle = Candle(
#             timestamp=item[0] / 1000,
#             open=float(item[1]),
#             high=float(item[2]),
#             low=float(item[3]),
#             close=float(item[4]),
#             volume=float(item[5])
#         )

#         candles.append(candle)

#     return MarketData(
#         symbol=symbol.upper(),
#         timeframe=timeframe,
#         candles=candles
#     )
import yfinance as yf

from models.candle import Candle
from models.market_data import MarketData


TIMEFRAME_MAP = {
    "1m": "1m",
    "2m": "2m",
    "5m": "5m",
    "15m": "15m",
    "30m": "30m",
    "1h": "1h",
    "4h": "1h",
    "1d": "1d",
}


def get_market_data(
    symbol: str,
    timeframe: str,
    limit: int = 100
) -> MarketData:

    symbol = symbol.upper()
    timeframe = timeframe.lower()

    # Convert our symbol format to Yahoo Finance format
    if symbol.endswith("USDT"):
        ticker_symbol = symbol.replace("USDT", "-USD")
    elif symbol.endswith("USD"):
        ticker_symbol = symbol.replace("USD", "-USD")
    else:
        ticker_symbol = symbol

    # Validate timeframe
    if timeframe not in TIMEFRAME_MAP:
        raise ValueError(
            f"Unsupported timeframe: {timeframe}"
        )

    interval = TIMEFRAME_MAP[timeframe]

    ticker = yf.Ticker(ticker_symbol)

    df = ticker.history(
        period="5d",
        interval=interval
    )

    if df.empty:
        raise ValueError(
            f"No market data found for {ticker_symbol}"
        )

    # Keep only the requested number of candles
    recent_df = df.tail(limit)

    candles = []

    for timestamp, row in recent_df.iterrows():

        candle = Candle(
            timestamp=timestamp.to_pydatetime(),
            open=float(row["Open"]),
            high=float(row["High"]),
            low=float(row["Low"]),
            close=float(row["Close"]),
            volume=float(row["Volume"])
        )

        candles.append(candle)

    return MarketData(
        symbol=symbol,
        timeframe=timeframe,
        candles=candles
    )