from services.strategy.strategy_scoring import (
    score_strategies,
    select_best_strategy
)


tests = [
    {
        "regime": "BULL_TREND",
        "confidence": 1.0
    },
    {
        "regime": "BEAR_TREND",
        "confidence": 0.5
    },
    {
        "regime": "HIGH_VOLATILITY",
        "confidence": 0.9
    },
    {
        "regime": "RANGE",
        "confidence": 0.7
    },
    {
        "regime": "UNKNOWN",
        "confidence": 0.5
    }
]


for regime in tests:

    scores = score_strategies(regime)

    best_strategy = select_best_strategy(scores)

    print("Regime:", regime)
    print("Scores:", scores)
    print("Best strategy:", best_strategy)
    print()