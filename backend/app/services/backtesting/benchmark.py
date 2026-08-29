def calculate_buy_and_hold(
    candles,
    initial_balance: float
) -> dict:

    if initial_balance <= 0:
        raise ValueError(
            "Initial balance must be greater than zero"
        )

    if len(candles) < 2:
        raise ValueError(
            "At least 2 candles are required"
        )

    entry_price = candles[0].close
    exit_price = candles[-1].close

    buy_and_hold_return = (
        (exit_price - entry_price)
        / entry_price
    )

    final_balance = (
        initial_balance
        * (1 + buy_and_hold_return)
    )

    return {
        "initial_balance": initial_balance,
        "final_balance": final_balance,
        "net_profit": final_balance - initial_balance,
        "total_return": buy_and_hold_return,
        "entry_price": entry_price,
        "exit_price": exit_price
    }