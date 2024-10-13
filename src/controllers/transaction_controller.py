from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from src.services import transaction_service
from src.database import get_db
from src.models.TransactionResponse import TransactionResponse
from src.models.CreateTransactionRequest import CreateTransactionRequest
from src.models.UpdateTransactionRequest import TransactionUpdateRequest

transaction_router = APIRouter(
)

@transaction_router.post("/", response_model=TransactionResponse)
async def create_transaction(transaction: CreateTransactionRequest, db: AsyncSession = Depends(get_db)):
    transaction = await transaction_service.create_transaction(transaction, db)
    return transaction

@transaction_router.get("/{user_id}/users", response_model=list[TransactionResponse])
async def get_user_transactions(
    user_id: int,
    skip: int = Query(0, ge=0), 
    limit: int = Query(10, ge=1), 
    db: AsyncSession = Depends(get_db)
):
    transactions = await transaction_service.get_user_transactions(user_id,skip,limit,db)
    return transactions

@transaction_router.put("/{transaction_id}/users/{user_id}", response_model=TransactionResponse)
async def update_user_transaction(
    user_id: int,
    transaction_id: int,
    transaction: TransactionUpdateRequest,
    db: AsyncSession = Depends(get_db)
):
    updated_transaction = await transaction_service.update_transaction(user_id, transaction_id, transaction, db)
    return updated_transaction

@transaction_router.delete("/{transaction_id}/users/{user_id}")
async def delete_user_transaction(
    user_id: int,
    transaction_id: int,
    db: AsyncSession = Depends(get_db)
):
    response =  await transaction_service.delete_transaction(user_id, transaction_id, db)
    return response


@transaction_router.get("/transaction-analytics/{user_id}")
async def get_transaction_analytics(user_id: int, db: AsyncSession = Depends(get_db)):
    analytics_result = await transaction_service.get_transaction_analytics(user_id,db)
    return analytics_result