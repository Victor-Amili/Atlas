from models.candle import Candle
from models.account import AccountConfig

from services.analysis.market_analysis import analyze_market

from services.backtesting.trade import BacktestTrade
from services.backtesting.backtest_result import BacktestResult


def run_backtest(
    candles: list[Candle],
    initial_balance: float,
    warmup_period: int = 50
) -> BacktestResult:

    if initial_balance <= 0:
        raise ValueError("Initial balance must be greater than zero")

    if len(candles) <= warmup_period:
        raise ValueError(
            f"At least {warmup_period + 1} candles are required"
        )

    balance = initial_balance
    trades: list[BacktestTrade] = []

    account = AccountConfig(
        balance=balance,
        risk_percent=0.01
    )

    i = warmup_period

    while i < len(candles) - 1:

        historical_candles = candles[:i + 1]

        analysis = analyze_market(
            historical_candles,
            account
        )

        decision = analysis.trade_decision

        if decision.get("decision") != "ENTER":
            i += 1
            continue

        entry_price = decision.get("entry_price")
        stop_loss = decision.get("stop_loss")
        take_profit = decision.get("take_profit")
        position_size = decision.get("position_size")

        if (
            entry_price is None
            or stop_loss is None
            or take_profit is None
            or position_size is None
        ):
            i += 1
            continue

        direction = decision.get("direction", "NONE")

        entry_candle = candles[i]

        trade = BacktestTrade(
            entry_time=entry_candle.timestamp,
            strategy=decision.get("strategy", "UNKNOWN"),
            direction=direction,
            entry_price=entry_price,
            stop_loss=stop_loss,
            take_profit=take_profit,
            position_size=position_size,
            risk=decision.get("risk", 0.0),
            reward=decision.get("reward", 0.0)
        )

        exit_found = False

        j = i + 1

        while j < len(candles):

            candle = candles[j]

            if direction == "LONG":

                stop_hit = candle.low <= stop_loss
                target_hit = candle.high >= take_profit

                if stop_hit and target_hit:
                    exit_price = stop_loss
                    result = "LOSS"

                elif stop_hit:
                    exit_price = stop_loss
                    result = "LOSS"

                elif target_hit:
                    exit_price = take_profit
                    result = "WIN"

                else:
                    j += 1
                    continue

            elif direction == "SHORT":

                stop_hit = candle.high >= stop_loss
                target_hit = candle.low <= take_profit

                if stop_hit and target_hit:
                    exit_price = stop_loss
                    result = "LOSS"

                elif stop_hit:
                    exit_price = stop_loss
                    result = "LOSS"

                elif target_hit:
                    exit_price = take_profit
                    result = "WIN"

                else:
                    j += 1
                    continue

            else:
                break

            if direction == "LONG":
                profit_loss = (
                    exit_price - entry_price
                ) * position_size
            else:
                profit_loss = (
                    entry_price - exit_price
                ) * position_size

            trade.exit_time = candle.timestamp
            trade.exit_price = exit_price
            trade.profit_loss = profit_loss
            trade.result = result

            balance += profit_loss

            trades.append(trade)

            exit_found = True

            break

        if exit_found:
            account = AccountConfig(
                balance=balance,
                risk_percent=0.01
            )

            i = j + 1

        else:
            break

    total_trades = len(trades)

    winning_trades = sum(
        1 for trade in trades
        if trade.result == "WIN"
    )

    losing_trades = sum(
        1 for trade in trades
        if trade.result == "LOSS"
    )

    net_profit = balance - initial_balance

    total_return = (
        net_profit / initial_balance
    )

    win_rate = (
        winning_trades / total_trades
        if total_trades > 0
        else 0.0
    )

    return BacktestResult(
        initial_balance=initial_balance,
        final_balance=balance,
        total_trades=total_trades,
        winning_trades=winning_trades,
        losing_trades=losing_trades,
        net_profit=net_profit,
        total_return=total_return,
        win_rate=win_rate,
        trades=trades
    )