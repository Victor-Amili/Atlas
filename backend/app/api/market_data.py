from fastapi import APIRouter

from services.market_data_service import get_market_data


router = APIRouter()


@router.get("/market-data")
def get_market_data_endpoint():
    return get_market_data()