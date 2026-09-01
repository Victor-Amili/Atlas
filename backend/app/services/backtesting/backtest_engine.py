from models.candle import Candle
from models.account import AccountConfig

from services.analysis.market_analysis import analyze_market
from services.backtesting.trade import BacktestTrade
from services.backtesting.backtest_result import BacktestResult


# ---------------------------------------------------------
# BACKTEST SETTINGS
# ---------------------------------------------------------

TRADE_COOLDOWN = 3          # Candles to wait after an exit
MAX_HOLDING_CANDLES = 24    # Maximum holding period


def run_backtest(
    candles: list[Candle],
    initial_balance: float,
    warmup_period: int = 50
) -> BacktestResult:

    # ---------------------------------------------------------
    # VALIDATION
    # ---------------------------------------------------------

    if initial_balance <= 0:
        raise ValueError(
            "Initial balance must be greater than zero"
        )

    if len(candles) <= warmup_period + 1:
        raise ValueError(
            f"At least {warmup_period + 2} candles are required"
        )

    # ---------------------------------------------------------
    # INITIAL STATE
    # ---------------------------------------------------------

    balance = initial_balance

    trades: list[BacktestTrade] = []

    account = AccountConfig(
        balance=balance,
        risk_percent=0.01
    )

    # First candle where trading is allowed
    i = warmup_period

    # ---------------------------------------------------------
    # MAIN BACKTEST LOOP
    # ---------------------------------------------------------

    while i < len(candles) - 1:

        # -----------------------------------------------------
        # ANALYZE MARKET
        # -----------------------------------------------------

        historical_candles = candles[:i + 1]

        analysis = analyze_market(
            historical_candles,
            account
        )

        decision = analysis.trade_decision

        # -----------------------------------------------------
        # NO ENTRY
        # -----------------------------------------------------

        if decision.get("decision") != "ENTER":
            i += 1
            continue

        # -----------------------------------------------------
        # GET TRADE PARAMETERS
        # -----------------------------------------------------

        stop_loss = decision.get("stop_loss")
        take_profit = decision.get("take_profit")
        position_size = decision.get("position_size")

        if (
            stop_loss is None
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
        # Signal is generated using candle i.
        # Trade executes at the OPEN of candle i + 1.
        # -----------------------------------------------------

        entry_index = i + 1

        if entry_index >= len(candles):
            break

        entry_candle = candles[entry_index]

        entry_price = entry_candle.open

        # -----------------------------------------------------
        # CREATE TRADE
        # -----------------------------------------------------

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

        # -----------------------------------------------------
        # SEARCH FOR EXIT
        # -----------------------------------------------------

        exit_found = False

        j = entry_index
        holding_candles = 0

        while j < len(candles):

            candle = candles[j]

            holding_candles += 1

            # -------------------------------------------------
            # LONG POSITION
            # -------------------------------------------------

            if direction == "LONG":

                stop_hit = candle.low <= stop_loss
                target_hit = candle.high >= take_profit

                # Conservative assumption:
                # If SL and TP are both touched in the same
                # candle, assume SL happened first.

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

                    # No exit yet.
                    #
                    # IMPORTANT:
                    # Move j forward so we do not create
                    # an infinite loop.

                    if holding_candles >= MAX_HOLDING_CANDLES:

                        exit_price = candle.close
                        result = "TIME_EXIT"

                    else:

                        j += 1
                        continue

                # Calculate LONG P/L

                profit_loss = (
                    exit_price - entry_price
                ) * position_size

            # -------------------------------------------------
            # SHORT POSITION
            # -------------------------------------------------

            else:

                stop_hit = candle.high >= stop_loss
                target_hit = candle.low <= take_profit

                # Conservative assumption:
                # If SL and TP are both touched in the same
                # candle, assume SL happened first.

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

                    # No exit yet.
                    #
                    # IMPORTANT:
                    # Move j forward so we do not create
                    # an infinite loop.

                    if holding_candles >= MAX_HOLDING_CANDLES:

                        exit_price = candle.close
                        result = "TIME_EXIT"

                    else:

                        j += 1
                        continue

                # Calculate SHORT P/L

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
        # DATASET ENDED BEFORE EXIT
        #
        # Close the remaining trade at the final candle close.
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

            exit_found = True

            # Dataset is finished.
            break

        # -----------------------------------------------------
        # UPDATE ACCOUNT
        # -----------------------------------------------------

        account = AccountConfig(
            balance=balance,
            risk_percent=0.01
        )

        # -----------------------------------------------------
        # MOVE PAST EXIT + COOLDOWN
        #
        # Example:
        # Exit at candle 100
        # Cooldown = 3
        #
        # Next analysis starts at candle 104.
        # -----------------------------------------------------

        i = j + 1 + TRADE_COOLDOWN

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
    # RETURN RESULT
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