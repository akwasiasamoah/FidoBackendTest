from pydantic import BaseModel
from src.models.TransactionType import TransactionType


class TransactionBaseModel(BaseModel):
    full_name: str
    transaction_amount: float
    transaction_type: TransactionType
