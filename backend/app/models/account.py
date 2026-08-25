from pydantic import BaseModel, Field


class AccountConfig(BaseModel):
    balance: float = Field(gt=0)
    risk_percent: float = Field(gt=0, le=0.01)