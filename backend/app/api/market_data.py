# from fastapi import APIRouter

# from services.market_data_service import get_market_data


# router = APIRouter()


# @router.get("/market-data")
# def get_market_data_endpoint(
#     symbol: str = "BTCUSD",
#     timeframe: str = "1h"
# ):
#     return get_market_data(symbol, timeframe)

from fastapi import APIRouter

from services.market_data_service import get_market_data


router = APIRouter()


@router.get("/market-data")
def get_market_data_endpoint(
    symbol: str = "BTCUSD",
    timeframe: str = "1h",
    limit: int = 100
):
    return get_market_data(
        symbol,
        timeframe,
        limit
    )