from models.candle import Candle
from services.backtesting.backtest_engine import run_backtest


def run_walk_forward(
    candles: list[Candle],
    initial_balance: float,
    train_size: int = 200,
    test_size: int = 100,
    step_size: int = 100
) -> dict:

    if initial_balance <= 0:
        raise ValueError(
            "Initial balance must be greater than zero"
        )

    if train_size <= 0:
        raise ValueError(
            "Train size must be greater than zero"
        )

    if test_size <= 0:
        raise ValueError(
            "Test size must be greater than zero"
        )

    if len(candles) < train_size + test_size:
        raise ValueError(
            "Not enough candles for walk-forward testing"
        )

    windows = []

    start = 0

    while start + train_size + test_size <= len(candles):

        train_end = start + train_size
        test_end = train_end + test_size

        train_candles = candles[start:train_end]
        test_candles = candles[train_end:test_end]

        # -----------------------------------------------------
        # TRAINING PHASE
        # -----------------------------------------------------

        # For now we only validate that the training window
        # can be processed successfully.
        training_result = run_backtest(
            train_candles,
            initial_balance
        )

        # -----------------------------------------------------
        # OUT-OF-SAMPLE TEST
        # -----------------------------------------------------

        testing_result = run_backtest(
            test_candles,
            initial_balance
        )

        windows.append({
            "train_start": start,
            "train_end": train_end,
            "test_start": train_end,
            "test_end": test_end,
            "training": training_result,
            "testing": testing_result
        })

        start += step_size

    return {
        "initial_balance": initial_balance,
        "train_size": train_size,
        "test_size": test_size,
        "step_size": step_size,
        "windows": windows,
        "total_windows": len(windows)
    }