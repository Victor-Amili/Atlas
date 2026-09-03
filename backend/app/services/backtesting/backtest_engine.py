from models.candle import Candle
from models.account import AccountConfig

from services.analysis.market_analysis import analyze_market
from services.backtesting.trade import BacktestTrade
from services.backtesting.backtest_result import BacktestResult
from services.risk.risk_management import calculate_risk
from services.risk.position_sizing import calculate_position_size


# ---------------------------------------------------------
# BACKTEST SETTINGS
# ---------------------------------------------------------

TRADE_COOLDOWN = 3
MAX_HOLDING_CANDLES = 24


def run_backtest(
    candles: list[Candle],
    initial_balance: float,
    warmup_period: int = 50
) -> BacktestResult:

    # -----------------------------------------------------
    # VALIDATION
    # -----------------------------------------------------

    if initial_balance <= 0:
        raise ValueError(
            "Initial balance must be greater than zero"
        )

    if len(candles) <= warmup_period + 1:
        raise ValueError(
            f"At least {warmup_period + 2} candles are required"
        )

    # -----------------------------------------------------
    # ACCOUNT
    # -----------------------------------------------------

    balance = initial_balance

    account = AccountConfig(
        balance=balance,
        risk_percent=0.01
    )

    trades: list[BacktestTrade] = []

    # First possible analysis candle
    i = warmup_period

    # -----------------------------------------------------
    # MAIN BACKTEST LOOP
    # -----------------------------------------------------

    while i < len(candles) - 1:

        # -------------------------------------------------
        # ANALYSIS
        # -------------------------------------------------

        historical_candles = candles[:i + 1]

        analysis = analyze_market(
            historical_candles,
            account
        )

        decision = analysis.trade_decision

        # -------------------------------------------------
        # NO ENTRY
        # -------------------------------------------------

        if decision.get("decision") != "ENTER":
            i += 1
            continue

        # -------------------------------------------------
        # EXECUTION
        #
        # Signal is generated on candle i.
        # Trade executes on candle i + 1 OPEN.
        #
        # IMPORTANT:
        # Risk and position size must be recalculated from
        # the actual simulated execution price. Using the
        # signal candle close here creates a look/price mismatch
        # between risk calculation and trade execution.
        # -------------------------------------------------

        entry_index = i + 1

        if entry_index >= len(candles):
            break

        entry_candle = candles[entry_index]

        entry_price = entry_candle.open

        # -------------------------------------------------
        # ENTRY-AWARE RISK
        # -------------------------------------------------

        risk = calculate_risk(
            trade_signal=analysis.trade_signal,
            candles=historical_candles,
            entry_price=entry_price
        )

        if not risk.get("valid", False):
            i += 1
            continue

        position = calculate_position_size(
            account_balance=balance,
            risk_percent=account.risk_percent,
            risk_analysis=risk
        )

        if not position.get("valid", False):
            i += 1
            continue

        stop_loss = risk.get("stop_loss")
        take_profit = risk.get("take_profit")
        position_size = position.get("position_size")

        if (
            stop_loss is None
            or take_profit is None
            or position_size is None
            or position_size <= 0
        ):
            i += 1
            continue

        direction = decision.get("direction", "NONE")

        if direction not in ("LONG", "SHORT"):
            i += 1
            continue

        # -------------------------------------------------
        # CREATE TRADE
        # -------------------------------------------------

        trade = BacktestTrade(
            entry_time=entry_candle.timestamp,
            strategy=decision.get(
                "strategy",
                "UNKNOWN"
            ),
            direction=direction,
            entry_price=entry_price,
            stop_loss=stop_loss,
            take_profit=take_profit,
            position_size=position_size,
            risk=decision.get("risk", 0.0),
            reward=decision.get("reward", 0.0)
        )

        # -------------------------------------------------
        # SEARCH FOR EXIT
        # -------------------------------------------------

        j = entry_index
        holding_candles = 0
        exit_found = False

        while j < len(candles):

            candle = candles[j]
            holding_candles += 1

            exit_price = None
            result = None

            # -------------------------------------------------
            # LONG
            # -------------------------------------------------

            if direction == "LONG":

                stop_hit = candle.low <= stop_loss
                target_hit = candle.high >= take_profit

                # Conservative assumption:
                # SL happens first if both touched.

                if stop_hit and target_hit:
                    exit_price = stop_loss
                    result = "LOSS"

                elif stop_hit:
                    exit_price = stop_loss
                    result = "LOSS"

                elif target_hit:
                    exit_price = take_profit
                    result = "WIN"

            # -------------------------------------------------
            # SHORT
            # -------------------------------------------------

            else:

                stop_hit = candle.high >= stop_loss
                target_hit = candle.low <= take_profit

                # Conservative assumption:
                # SL happens first if both touched.

                if stop_hit and target_hit:
                    exit_price = stop_loss
                    result = "LOSS"

                elif stop_hit:
                    exit_price = stop_loss
                    result = "LOSS"

                elif target_hit:
                    exit_price = take_profit
                    result = "WIN"

            # -------------------------------------------------
            # SL / TP EXIT FOUND
            # -------------------------------------------------

            if exit_price is not None:

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

            # -------------------------------------------------
            # MAX HOLDING TIME
            # -------------------------------------------------

            if holding_candles >= MAX_HOLDING_CANDLES:

                exit_price = candle.close

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
                trade.result = "TIME_EXIT"

                balance += profit_loss

                trades.append(trade)

                exit_found = True

                break

            # -------------------------------------------------
            # MOVE TO NEXT CANDLE
            # -------------------------------------------------

            j += 1

        # -------------------------------------------------
        # NO EXIT FOUND
        #
        # Dataset ended before SL/TP/time exit.
        # Close at final candle close.
        # -------------------------------------------------

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

            # Dataset is finished
            break

        # -------------------------------------------------
        # UPDATE ACCOUNT
        # -------------------------------------------------

        account = AccountConfig(
            balance=balance,
            risk_percent=0.01
        )

        # -------------------------------------------------
        # COOLDOWN
        #
        # Move past the exit candle plus cooldown.
        # -------------------------------------------------

        i = j + TRADE_COOLDOWN + 1

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