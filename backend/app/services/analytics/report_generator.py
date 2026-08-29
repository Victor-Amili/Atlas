from models.backtest_report import BacktestReport
from services.backtesting.backtest_result import BacktestResult
from services.analytics.performance_analyzer import analyze_performance


def generate_backtest_report(
    result: BacktestResult
) -> BacktestReport:

    performance = analyze_performance(result)

    return BacktestReport(
        initial_balance=result.initial_balance,
        final_balance=result.final_balance,

        total_trades=performance["total_trades"],
        winning_trades=performance["winning_trades"],
        losing_trades=performance["losing_trades"],

        win_rate=performance["win_rate"],
        net_profit=performance["net_profit"],
        total_return=performance["total_return"],

        average_win=performance["average_win"],
        average_loss=performance["average_loss"],

        profit_factor=performance["profit_factor"],
        expectancy=performance["expectancy"],

        largest_win=performance["largest_win"],
        largest_loss=performance["largest_loss"],

        maximum_drawdown=performance[
            "maximum_drawdown"
        ],

        maximum_drawdown_percent=performance[
            "maximum_drawdown_percent"
        ],

        sharpe_ratio=performance["sharpe_ratio"],
        sortino_ratio=performance["sortino_ratio"],

        equity_curve=performance["equity_curve"],
    )