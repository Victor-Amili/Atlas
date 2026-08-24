from pydantic import BaseModel


class AccountConfig(BaseModel):
    balance: float
    risk_percent: float