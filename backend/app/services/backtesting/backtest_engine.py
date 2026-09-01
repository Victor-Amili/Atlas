
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

    # ---------------------------------------------------------
    # VALIDATION
    # ---------------------------------------------------------

    if initial_balance <= 0:
        raise ValueError("Initial balance must be greater than zero")

    if len(candles) <= warmup_period + 1:
        raise ValueError(
            f"At least {warmup_period + 2} candles are required"
        )

    balance = initial_balance
    trades: list[BacktestTrade] = []

    account = AccountConfig(
        balance=balance,
        risk_percent=0.01
    )

    # ---------------------------------------------------------
    # MAIN BACKTEST LOOP
    # ---------------------------------------------------------

    i = warmup_period

    while i < len(candles) - 1:

        # -----------------------------------------------------
        # ANALYSIS USES ONLY INFORMATION AVAILABLE AT i
        # -----------------------------------------------------

        historical_candles = candles[:i + 1]

        analysis = analyze_market(
            historical_candles,
            account
        )

        decision = analysis.trade_decision

        if decision.get("decision") != "ENTER":
            i += 1
            continue

        # -----------------------------------------------------
        # TRADE PARAMETERS
        # -----------------------------------------------------

        signal_entry_price = decision.get("entry_price")
        stop_loss = decision.get("stop_loss")
        take_profit = decision.get("take_profit")
        position_size = decision.get("position_size")

        if (
            signal_entry_price is None
            or stop_loss is None
            or take_profit is None
            or position_size is None
        ):
            i += 1
            continue

        direction = decision.get("direction", "NONE")

        if direction not in ("LONG", "SHORT"):
            i += 1
            continue

        # -----------------------------------------------------
        # EXECUTION
        #
        # The signal is generated using candle i.
        # The earliest executable candle is i + 1.
        # -----------------------------------------------------

        entry_index = i + 1
        entry_candle = candles[entry_index]

        # Use the next candle OPEN as the executable entry.
        entry_price = entry_candle.open

        # -----------------------------------------------------
        # CREATE TRADE
        # -----------------------------------------------------

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

        # -----------------------------------------------------
        # SEARCH FOR EXIT
        # -----------------------------------------------------

        j = entry_index

        while j < len(candles):

            candle = candles[j]

            # -------------------------------------------------
            # LONG
            # -------------------------------------------------

            if direction == "LONG":

                stop_hit = candle.low <= stop_loss
                target_hit = candle.high >= take_profit

                # Conservative assumption:
                # if both are touched in the same candle,
                # assume SL happened first.
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

                profit_loss = (
                    exit_price - entry_price
                ) * position_size

            # -------------------------------------------------
            # SHORT
            # -------------------------------------------------

            else:

                stop_hit = candle.high >= stop_loss
                target_hit = candle.low <= take_profit

                # Conservative assumption:
                # if both are touched in the same candle,
                # assume SL happened first.
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

                profit_loss = (
                    entry_price - exit_price
                ) * position_size

            # -------------------------------------------------
            # RECORD EXIT
            # -------------------------------------------------

            trade.exit_time = candle.timestamp
            trade.exit_price = exit_price
            trade.profit_loss = profit_loss
            trade.result = result

            balance += profit_loss

            trades.append(trade)

            exit_found = True

            break

        # -----------------------------------------------------
        # TIME EXIT
        #
        # If neither SL nor TP was reached before the dataset
        # ended, close the position at the final candle close.
        # -----------------------------------------------------

        if not exit_found:

            final_candle = candles[-1]

            exit_price = final_candle.close

            if direction == "LONG":
                profit_loss = (
                    exit_price - entry_price
                ) * position_size

            else:
                profit_loss = (
                    entry_price - exit_price
                ) * position_size

            trade.exit_time = final_candle.timestamp
            trade.exit_price = exit_price
            trade.profit_loss = profit_loss
            trade.result = "TIME_EXIT"

            balance += profit_loss

            trades.append(trade)

            break

        # -----------------------------------------------------
        # UPDATE ACCOUNT
        # -----------------------------------------------------

        account = AccountConfig(
            balance=balance,
            risk_percent=0.01
        )

        # -----------------------------------------------------
        # MOVE PAST THE EXIT CANDLE
        #
        # Prevent overlapping trades.
        # -----------------------------------------------------

        i = j + 1

    # ---------------------------------------------------------
    # PERFORMANCE CALCULATIONS
    # ---------------------------------------------------------

    total_trades = len(trades)

    winning_trades = sum(
        1
        for trade in trades
        if trade.result == "WIN"
    )

    losing_trades = sum(
        1
        for trade in trades
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

    # ---------------------------------------------------------
    # RESULT
    # ---------------------------------------------------------

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