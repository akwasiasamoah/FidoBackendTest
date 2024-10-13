from src.models.TransactionBaseModel import TransactionBaseModel


class CreateTransactionRequest(TransactionBaseModel):
    user_id: int
