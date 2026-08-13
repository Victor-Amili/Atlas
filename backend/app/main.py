from fastapi import FastAPI

from api.health import router as health_router
from api.market_data import router as market_data_router
from api.analysis import router as analysis_router

app = FastAPI(title="Atlas API")

app.include_router(health_router, prefix="/api")
app.include_router(market_data_router, prefix="/api")
app.include_router(analysis_router)