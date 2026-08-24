MAX_RISK_PERCENT = 0.01


def calculate_position_size(
    account_balance: float,
    risk_percent: float,
    risk_analysis: dict
) -> dict:

    if account_balance <= 0:
        return {
            "valid": False,
            "reason": "Account balance must be greater than zero"
        }

    if risk_percent <= 0:
        return {
            "valid": False,
            "reason": "Risk percentage must be greater than zero"
        }

    if risk_percent > MAX_RISK_PERCENT:
        return {
            "valid": False,
            "reason": "Risk percentage exceeds maximum allowed risk"
        }

    if not risk_analysis.get("valid", False):
        return {
            "valid": False,
            "reason": "Invalid risk analysis"
        }

    risk_per_unit = risk_analysis.get("risk", 0.0)
    entry_price = risk_analysis.get("entry_price", 0.0)

    if risk_per_unit <= 0:
        return {
            "valid": False,
            "reason": "Invalid risk per unit"
        }

    if entry_price <= 0:
        return {
            "valid": False,
            "reason": "Invalid entry price"
        }

    maximum_loss = account_balance * risk_percent

    position_size = maximum_loss / risk_per_unit

    position_value = position_size * entry_price

    return {
        "valid": True,
        "account_balance": account_balance,
        "risk_percent": risk_percent,
        "maximum_loss": maximum_loss,
        "risk_per_unit": risk_per_unit,
        "position_size": position_size,
        "position_value": position_value
    }