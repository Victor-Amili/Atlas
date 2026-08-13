from fastapi import APIRouter

from models.analysis_request import AnalysisRequest
from models.market_analysis import MarketAnalysis  


from services.analysis.return_analysis import analyze_returns
from services.market_data_service import get_sample_market_data
from services.analysis.volatility_analysis import calculate_volatility
from services.analysis.market_analysis import analyze_market


router = APIRouter(
    prefix="/api/analysis",
    tags=["Analysis"]
)


@router.post("/returns")
def get_return_analysis(request: AnalysisRequest):
    return analyze_returns(request.candles)


@router.post("/volatility")
def get_volatility_analysis(request: AnalysisRequest):
    return calculate_volatility(request.candles)

@router.post("/market-analysis")
def get_market_analysis(request: AnalysisRequest) -> MarketAnalysis:
    return analyze_market(request.candles)

@router.get("/market-returns")
def get_market_returns():
    market_data = get_sample_market_data()

    return analyze_returns(market_data.candles)


   