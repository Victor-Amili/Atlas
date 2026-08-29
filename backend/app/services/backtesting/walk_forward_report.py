from services.backtesting.walk_forward import run_walk_forward


def analyze_walk_forward(
    candles,
    initial_balance: float,
    train_size: int = 200,
    test_size: int = 100,
    step_size: int = 100
) -> dict:

    result = run_walk_forward(
        candles,
        initial_balance,
        train_size,
        test_size,
        step_size
    )

    windows = result["windows"]

    if not windows:
        return {
            "total_windows": 0,
            "average_training_return": 0.0,
            "average_testing_return": 0.0,
            "positive_testing_windows": 0,
            "negative_testing_windows": 0,
            "testing_returns": []
        }

    training_returns = [
        window["training"].total_return
        for window in windows
    ]

    testing_returns = [
        window["testing"].total_return
        for window in windows
    ]

    positive_testing_windows = sum(
        1
        for value in testing_returns
        if value > 0
    )

    negative_testing_windows = sum(
        1
        for value in testing_returns
        if value < 0
    )

    return {
        "total_windows": len(windows),

        "average_training_return": (
            sum(training_returns)
            / len(training_returns)
        ),

        "average_testing_return": (
            sum(testing_returns)
            / len(testing_returns)
        ),

        "positive_testing_windows":
            positive_testing_windows,

        "negative_testing_windows":
            negative_testing_windows,

        "testing_returns": testing_returns,

        "training_returns": training_returns
    }