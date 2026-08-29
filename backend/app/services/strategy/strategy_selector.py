from services.strategy.strategy_scoring import select_best_strategy


def select_strategy(strategy_scores: dict) -> dict:

    strategy = select_best_strategy(strategy_scores)

    score = strategy_scores.get(strategy, 0.0)

    return {
        "strategy": strategy,
        "score": score,
        "available_strategies": strategy_scores
    }