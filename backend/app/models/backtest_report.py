from pydantic import BaseModel, Field


class BacktestReport(BaseModel):

    initial_balance: float = Field(ge=0)
    final_balance: float = Field(ge=0)

    total_trades: int = Field(ge=0)
    winning_trades: int = Field(ge=0)
    losing_trades: int = Field(ge=0)

    win_rate: float = Field(ge=0)
    net_profit: float
    total_return: float

    average_win: float
    average_loss: float

    profit_factor: float = Field(ge=0)
    expectancy: float

    largest_win: float
    largest_loss: float

    maximum_drawdown: float = Field(ge=0)
    maximum_drawdown_percent: float = Field(ge=0)

    sharpe_ratio: float
    sortino_ratio: float

    equity_curve: list[float]