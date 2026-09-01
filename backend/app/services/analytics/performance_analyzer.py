import math
from unittest import result

from services.backtesting.backtest_result import BacktestResult


def calculate_equity_curve(
    result: BacktestResult
) -> list[float]:

    balance = result.initial_balance
    equity_curve = [balance]

    for trade in result.trades:

        if trade.result in ["WIN", "LOSS"]:
            balance += trade.profit_loss
            equity_curve.append(balance)

    return equity_curve


def calculate_max_drawdown(
    equity_curve: list[float]
) -> dict:

    if not equity_curve:
        return {
            "maximum_drawdown": 0.0,
            "maximum_drawdown_percent": 0.0
        }

    peak = equity_curve[0]
    maximum_drawdown = 0.0
    maximum_drawdown_percent = 0.0

    for equity in equity_curve:

        if equity > peak:
            peak = equity

        drawdown = peak - equity

        if drawdown > maximum_drawdown:
            maximum_drawdown = drawdown

        if peak > 0:
            drawdown_percent = drawdown / peak

            if drawdown_percent > maximum_drawdown_percent:
                maximum_drawdown_percent = drawdown_percent

    return {
        "maximum_drawdown": maximum_drawdown,
        "maximum_drawdown_percent": maximum_drawdown_percent
    }


def calculate_sharpe_ratio(
    equity_curve: list[float]
) -> float:

    if len(equity_curve) < 2:
        return 0.0

    returns = []

    for i in range(1, len(equity_curve)):

        previous = equity_curve[i - 1]
        current = equity_curve[i]

        if previous <= 0:
            continue

        returns.append(
            (current - previous) / previous
        )

    if len(returns) < 2:
        return 0.0

    average_return = sum(returns) / len(returns)

    variance = sum(
        (r - average_return) ** 2
        for r in returns
    ) / (len(returns) - 1)

    standard_deviation = math.sqrt(variance)

    if standard_deviation == 0:
        return 0.0

    return average_return / standard_deviation


def calculate_sortino_ratio(
    equity_curve: list[float]
) -> float:

    if len(equity_curve) < 2:
        return 0.0

    returns = []

    for i in range(1, len(equity_curve)):

        previous = equity_curve[i - 1]
        current = equity_curve[i]

        if previous <= 0:
            continue

        returns.append(
            (current - previous) / previous
        )

    if not returns:
        return 0.0

    average_return = sum(returns) / len(returns)

    downside_returns = [
        r for r in returns
        if r < 0
    ]

    if not downside_returns:
        return 0.0

    downside_variance = sum(
        r ** 2
        for r in downside_returns
    ) / len(downside_returns)

    downside_deviation = math.sqrt(downside_variance)

    if downside_deviation == 0:
        return 0.0

    return average_return / downside_deviation


def analyze_performance(
    result: BacktestResult
) -> dict:

    trades = result.trades

    completed_trades = [
        trade
        for trade in trades
        if trade.result in ["WIN", "LOSS"]
    ]

    if not completed_trades:

        return {
            "total_trades": 0,
            "winning_trades": 0,
            "losing_trades": 0,
            "win_rate": 0.0,
            "net_profit": 0.0,
            "total_return": 0.0,
            "average_win": 0.0,
            "average_loss": 0.0,
            "profit_factor": 0.0,
            "expectancy": 0.0,
            "largest_win": 0.0,
            "largest_loss": 0.0,
            "equity_curve": [result.initial_balance],
            "maximum_drawdown": 0.0,
            "maximum_drawdown_percent": 0.0,
            "sharpe_ratio": 0.0,
            "sortino_ratio": 0.0,
        }

    profits = [
        trade.profit_loss
        for trade in completed_trades
        if trade.profit_loss > 0
    ]

    losses = [
        trade.profit_loss
        for trade in completed_trades
        if trade.profit_loss < 0
    ]

    total_trades = len(completed_trades)
    winning_trades = len(profits)
    losing_trades = len(losses)

    win_rate = winning_trades / total_trades

    net_profit = sum(
        trade.profit_loss
        for trade in completed_trades
    )

    total_return = (
        net_profit / result.initial_balance
    )

    average_win = (
        sum(profits) / len(profits)
        if profits
        else 0.0
    )

    average_loss = (
        sum(losses) / len(losses)
        if losses
        else 0.0
    )

    gross_profit = sum(profits)
    gross_loss = abs(sum(losses))

    profit_factor = (
        gross_profit / gross_loss
        if gross_loss > 0
        else 0.0
    )

    expectancy = net_profit / total_trades

    largest_win = (
        max(profits)
        if profits
        else 0.0
    )

    largest_loss = (
        min(losses)
        if losses
        else 0.0
    )
    
    time_exit_trades = sum(
        1
        for trade in result.trades
        if trade.result == "TIME_EXIT"
    )

    long_trades = sum(
        1
        for trade in result.trades
        if trade.direction == "LONG"
    )

    short_trades = sum(
        1
        for trade in result.trades
        if trade.direction == "SHORT"
    )

    equity_curve = calculate_equity_curve(result)

    drawdown = calculate_max_drawdown(equity_curve)

    sharpe_ratio = calculate_sharpe_ratio(
        equity_curve
    )

    sortino_ratio = calculate_sortino_ratio(
        equity_curve
    )
    
    strategy_stats = {}

    for trade in result.trades:

        name = trade.strategy

        if name not in strategy_stats:
            strategy_stats[name] = {
                "trades": 0,
                "wins": 0,
                "profit": 0.0
            }

        strategy_stats[name]["trades"] += 1
        strategy_stats[name]["profit"] += trade.profit_loss

        if trade.result == "WIN":
            strategy_stats[name]["wins"] += 1

    for name in strategy_stats:

        s = strategy_stats[name]

        s["win_rate"] = (
            s["wins"] / s["trades"]
            if s["trades"]
            else 0
        )
    


    return {
        "total_trades": total_trades,
        "winning_trades": winning_trades,
        "losing_trades": losing_trades,
        "win_rate": win_rate,
        "net_profit": net_profit,
        "total_return": total_return,
        "average_win": average_win,
        "average_loss": average_loss,
        "profit_factor": profit_factor,
        "expectancy": expectancy,
        "largest_win": largest_win,
        "largest_loss": largest_loss,
        "equity_curve": equity_curve,
        "time_exit_trades": time_exit_trades,
        "long_trades": long_trades,
        "short_trades": short_trades,
        "maximum_drawdown": drawdown[
            "maximum_drawdown"
        ],
        "maximum_drawdown_percent": drawdown[
            "maximum_drawdown_percent"
        ],
        "sharpe_ratio": sharpe_ratio,
        "sortino_ratio": sortino_ratio,
        "strategy_statistics": strategy_stats,
    }