from enum import Enum


class TransactionType(str, Enum):
    credit = "credit"
    debit = "debit"