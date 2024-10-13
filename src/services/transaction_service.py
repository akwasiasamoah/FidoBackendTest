from src.models.CreateTransactionRequest import CreateTransactionRequest
from src.models.UpdateTransactionRequest import TransactionUpdateRequest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func
from fastapi import HTTPException, Query
from src.schemas.entities import User, Transaction
from sqlalchemy.future import select 
from sqlalchemy.exc import SQLAlchemyError


async def create_transaction(transaction: CreateTransactionRequest, db: AsyncSession):
    try:
        result = await db.execute(select(User).filter(User.id == transaction.user_id))
        user = result.scalars().first()
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Create the transaction
        db_transaction = Transaction(**transaction.dict())
        db.add(db_transaction)
        await db.commit()
        await db.refresh(db_transaction)
        
        return db_transaction
    
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail="An error occurred while processing the transaction.") from e
    
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred.") from e


async def get_user_transactions(user_id: int, skip: int, limit: int, db: AsyncSession):
    try:
        result = await db.execute(select(User).filter(User.id == user_id))
        user = result.scalars().first()
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        

        transaction_check = await db.execute(
            select(Transaction).filter(Transaction.user_id == user_id)
        )
        if len(transaction_check.scalars().all()) == 0:
            raise HTTPException(status_code=404, detail="No transactions found for this user.")
        
        transactions_result = await db.execute(
            select(Transaction).filter(Transaction.user_id == user_id).offset(skip).limit(limit)
        )
        transactions = transactions_result.scalars().all()
        
        return transactions
    
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail="An error occurred while fetching transactions.") from e
    
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred.") from e


async def update_transaction(
    user_id: int, 
    transaction_id: int,
    transaction: TransactionUpdateRequest,
    db: AsyncSession
):

    try:
        result = await db.execute(select(Transaction).filter(Transaction.id == transaction_id))
        db_transaction = result.scalars().first()
        
        if not db_transaction:
            raise HTTPException(status_code=404, detail="Transaction not found")
        
        if db_transaction.user_id != user_id:
            raise HTTPException(status_code=403, detail="You do not have permission to update this transaction.")
        
        for key, value in transaction.dict(exclude_unset=True).items():
            setattr(db_transaction, key, value)
        
        # Commit the changes
        await db.commit()
        await db.refresh(db_transaction)
        
        return db_transaction
    
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail="An error occurred while updating the transaction.") from e
    
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred.") from e

async def delete_transaction(
    user_id: int, 
    transaction_id: int,
    db: AsyncSession
):
    try:
        result = await db.execute(select(Transaction).filter(Transaction.id == transaction_id))
        db_transaction = result.scalars().first()

        if not db_transaction:
            raise HTTPException(status_code=404, detail="Transaction not found")

        if db_transaction.user_id != user_id:
            raise HTTPException(status_code=403, detail="You do not have permission to delete this transaction.")

        db.delete(db_transaction)
        await db.commit()

        return {"detail": "Transaction deleted"}
    
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail="An error occurred while deleting the transaction.") from e

    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred.") from e

async def get_transaction_analytics(user_id: int, db: AsyncSession):
    try:
        average_amount = select(func.avg(Transaction.transaction_amount)).filter(Transaction.user_id == user_id)
        result = await db.execute(average_amount)
        avg_transaction_value = result.scalar()

        day_with_most_transactions = (
            select(
                Transaction.transaction_date,
                func.count(Transaction.id).label('transaction_count')
            )
            .filter(Transaction.user_id == user_id)
            .group_by(Transaction.transaction_date)
            .order_by(func.count(Transaction.id).desc())
            .limit(1) 
        )

        result = await db.execute(day_with_most_transactions)
        day_with_most_transactions = result.first()

        if day_with_most_transactions is None:
            raise HTTPException(status_code=404, detail="User not found or no transactions available")

        return {
            "average_transaction_value": avg_transaction_value,
            "day_with_most_transactions": {
                "date": day_with_most_transactions.transaction_date,
                "count": day_with_most_transactions.transaction_count
            }
        }
    
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail="An error occurred performing your analytics.") from e

    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="An internal server error occurred")