from statistics import stdev


def calculate_volatility(returns: list[float]) -> float:
    if len(returns) < 2:
        return 0.0

    return stdev(returns)