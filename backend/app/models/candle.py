from datetime import datetime

from pydantic import BaseModel, Field, model_validator


class Candle(BaseModel):
    timestamp: datetime

    open: float = Field(gt=0)
    high: float = Field(gt=0)
    low: float = Field(gt=0)
    close: float = Field(gt=0)
    volume: float = Field(ge=0)

    @model_validator(mode="after")
    def validate_price_range(self):
        if self.high < self.open:
            raise ValueError("High cannot be lower than open")

        if self.high < self.close:
            raise ValueError("High cannot be lower than close")

        if self.low > self.open:
            raise ValueError("Low cannot be higher than open")

        if self.low > self.close:
            raise ValueError("Low cannot be higher than close")

        if self.low > self.high:
            raise ValueError("Low cannot be higher than high")

        return self