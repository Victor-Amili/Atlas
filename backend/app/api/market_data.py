from fastapi import APIRouter

from services.market_data_service import get_sample_market_data

router = APIRouter()


@router.get("/market-data")
def get_market_data():
    return get_sample_market_data()