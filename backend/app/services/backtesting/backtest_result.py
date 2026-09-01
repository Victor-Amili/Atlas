
from pydantic import BaseModel, Field

from services.backtesting.trade import BacktestTrade


class BacktestResult(BaseModel):

    initial_balance: float

    final_balance: float

    total_trades: int = 0

    winning_trades: int = 0

    losing_trades: int = 0

    net_profit: float = 0.0

    total_return: float = 0.0

    win_rate: float = 0.0

    trades: list[BacktestTrade] = Field(
        default_factory=list
    )

