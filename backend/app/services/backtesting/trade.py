from pydantic import BaseModel
from datetime import datetime


class BacktestTrade(BaseModel):

    entry_time: datetime
    exit_time: datetime | None = None

    strategy: str
    direction: str

    entry_price: float
    exit_price: float | None = None

    stop_loss: float
    take_profit: float

    position_size: float

    risk: float
    reward: float

    profit_loss: float = 0.0

    result: str = "OPEN"

    # -----------------------------
    # NEW METADATA
    # -----------------------------

    regime: str | None = None

    strategy_score: float | None = None

    confidence: float | None = None

    duration_candles: int = 0

    exit_reason: str | None = None