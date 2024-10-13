from pydantic import BaseModel
from datetime import datetime

class TransactionResponse(BaseModel):
    transaction_date: datetime

    class Config:
        orm_mode = True