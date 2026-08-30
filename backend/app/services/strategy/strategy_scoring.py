# from services.analysis.breakout_analysis import analyze_breakout

# MIN_STRATEGY_SCORE = 0.5

# # Volatility percentage ranges
# LOW_VOLATILITY_PERCENT = 0.50
# HIGH_VOLATILITY_PERCENT = 1.00


# def score_strategies(
#     regime_analysis: dict,
#     volatility_analysis: dict,
#     breakout_analysis: dict | None = None
# ) -> dict:

#     regime = regime_analysis.get("regime", "UNKNOWN")
#     confidence = regime_analysis.get("confidence", 0.0)

#     volatility_percent = volatility_analysis.get(
#         "volatility_percent",
#         0.0
#     )

#     scores = {
#         "TREND_FOLLOWING": 0.0,
#         "BREAKOUT": 0.0,
#         "MEAN_REVERSION": 0.0
#     }

# # ---------------------------------------------------------
# # TREND FOLLOWING
# # ---------------------------------------------------------

#     if regime in ("BULL_TREND", "BEAR_TREND"):

#         trend_strength = regime_analysis.get(
#             "trend_strength",
#             confidence
#         )

#         price_change_percent = abs(
#             regime_analysis.get(
#                 "price_change_percent",
#                 0.0 
#             )
#         )
    

#     # Normalize price movement.
#         price_score = min(
#             price_change_percent / 1.0,
#             1.0
#         )

#         trend_score = (
#             confidence * 0.40
#             + trend_strength * 0.40
#             + price_score * 0.20
#         )

#         scores["TREND_FOLLOWING"] = round(
#             trend_score,
#             4   
#         )
#     # ---------------------------------------------------------
#     # HIGH VOLATILITY / BREAKOUT
#     # ---------------------------------------------------------

#     elif regime == "HIGH_VOLATILITY":

#         if breakout_analysis is None:
#          breakout_analysis = {}

#         volatility_score = 0.0

#         if volatility_percent <= LOW_VOLATILITY_PERCENT:
#             volatility_score = 0.0

#         elif volatility_percent >= HIGH_VOLATILITY_PERCENT:
#             volatility_score = 1.0

#         else:
#             volatility_score = (
#                 (volatility_percent - LOW_VOLATILITY_PERCENT)
#                 /
#                 (HIGH_VOLATILITY_PERCENT - LOW_VOLATILITY_PERCENT)
#             )

#         structure_score = breakout_analysis.get(
#             "score",
#             0.0
#         )

#         breakout_direction = breakout_analysis.get(
#          "breakout",
#             "NONE"
#         )

#         # ---------------------------------------------------------
#         # BREAKOUT REQUIRES PRICE-STRUCTURE EVIDENCE
#     #  ---------------------------------------------------------

#         if breakout_direction in ("BULLISH", "BEARISH"):

#             scores["BREAKOUT"] = round(
#                 (volatility_score * 0.4)
#                 +
#                 (structure_score * 0.6),
#                 4
#             )

#         else:

#             scores["BREAKOUT"] = round(
#                 structure_score * 0.6,
#                 4
#             )

#     # ---------------------------------------------------------
#     # RANGE / MEAN REVERSION
#     # ---------------------------------------------------------

#     elif regime == "RANGE":

#         scores["MEAN_REVERSION"] = 1.0 - confidence

#     return scores


# def select_best_strategy(scores: dict) -> str:

#     if not scores:
#         return "NO_STRATEGY"

#     best_strategy = max(scores, key=scores.get)

#     if scores[best_strategy] < MIN_STRATEGY_SCORE:
#         return "NO_STRATEGY"

#     return best_strategy


MIN_STRATEGY_SCORE = 0.50


def clamp(value: float) -> float:
    return max(0.0, min(value, 1.0))


def score_strategies(
    regime_analysis: dict,
    volatility_analysis: dict,
    breakout_analysis: dict | None = None,
    trend_analysis: dict | None = None,
) -> dict:

    regime = regime_analysis.get("regime", "UNKNOWN")
    regime_confidence = regime_analysis.get("confidence", 0.0)

    volatility_percent = volatility_analysis.get(
        "volatility_percent",
        0.0
    )

    breakout_analysis = breakout_analysis or {}
    trend_analysis = trend_analysis or {}

    scores = {
        "TREND_FOLLOWING": 0.0,
        "BREAKOUT": 0.0,
        "MEAN_REVERSION": 0.0,
    }

    # =========================================================
    # TREND FOLLOWING
    # =========================================================

    trend_strength = trend_analysis.get(
        "strength",
        regime_analysis.get("trend_strength", 0.0)
    )

    price_change_percent = abs(
        regime_analysis.get("price_change_percent", 0.0)
    )

    trend_direction_score = clamp(
        trend_strength
    )

    price_momentum_score = clamp(
        price_change_percent / 2.0
    )

    if regime in ("BULL_TREND", "BEAR_TREND"):

        scores["TREND_FOLLOWING"] = round(
            (
                regime_confidence * 0.40
                + trend_direction_score * 0.35
                + price_momentum_score * 0.25
            ),
            4
        )

    # =========================================================
    # BREAKOUT
    # =========================================================

    breakout_score = breakout_analysis.get(
        "score",
        0.0
    )

    breakout_direction = breakout_analysis.get(
        "breakout",
        "NONE"
    )

    volatility_score = clamp(
        volatility_percent / 2.0
    )

    structure_score = clamp(
        breakout_score
    )

    if breakout_direction in ("BULLISH", "BEARISH"):

        scores["BREAKOUT"] = round(
            (
                structure_score * 0.50
                + volatility_score * 0.30
                + regime_confidence * 0.20
            ),
            4
        )

    else:

        # A breakout strategy can still be considered,
        # but without confirmed price structure it receives
        # a heavily reduced score.
        scores["BREAKOUT"] = round(
            structure_score * 0.30
            + volatility_score * 0.10,
            4
        )

    # =========================================================
    # MEAN REVERSION
    # =========================================================

    if regime == "RANGE":

        range_score = clamp(
            1.0 - regime_confidence
        )

        # Stronger range conditions receive higher scores.
        scores["MEAN_REVERSION"] = round(
            range_score,
            4
        )

    else:

        # Mean reversion is possible outside a range,
        # but should receive a strong penalty.
        scores["MEAN_REVERSION"] = 0.0

    return scores


def select_best_strategy(scores: dict) -> str:

    if not scores:
        return "NO_STRATEGY"

    best_strategy = max(
        scores,
        key=scores.get
    )

    best_score = scores[best_strategy]

    if best_score < MIN_STRATEGY_SCORE:
        return "NO_STRATEGY"

    return best_strategy

