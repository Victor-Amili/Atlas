from services.providers.bitget_provider import get_bitget_market_data


def get_market_data(
    symbol: str,
    timeframe: str,
    limit: int = 100
):
    return get_bitget_market_data(
        symbol=symbol,
        timeframe=timeframe,
        limit=limit
    )