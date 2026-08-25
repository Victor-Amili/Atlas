from fastapi import APIRouter

from models.analysis_request import AnalysisRequest
from models.market_analysis import MarketAnalysis  
from models.account import AccountConfig


from services.analysis.return_analysis import analyze_returns
from services.market_data_service import get_market_data, get_sample_market_data
from services.analysis.volatility_analysis import calculate_volatility
from services.analysis.market_analysis import analyze_market
from services.analysis.market_summary import summarize_market


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
    account = AccountConfig(
        balance=100000,
        risk_percent=0.01
    )

    return analyze_market(request.candles, account)

@router.get("/market-summary")
def get_market_summary(
    symbol: str = "BTCUSDT",
    timeframe: str = "1h",
    limit: int = 100
):
    account = AccountConfig(
        balance=100000,
        risk_percent=0.01
    )

    market_data = get_market_data(
        symbol=symbol,
        timeframe=timeframe,
        limit=limit
    )

    return summarize_market(
        market_data.candles,
        account
    )

@router.get("/market-returns")
def get_market_returns(
    symbol: str = "BTCUSD",
    timeframe: str = "1h",
    limit: int = 100
):
    market_data = get_market_data(
        symbol,
        timeframe,
        limit
    )

    return analyze_returns(
        market_data.candles
    )

   