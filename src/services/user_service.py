from src.models.CreateUserRequest import CreateUserRequest
from src.models.UpdateUserRequest import UpdateUserRequest
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from src.schemas.entities import User
from src.utils.hash import Hash
from sqlalchemy.future import select 


async def create_user(user: CreateUserRequest, db: AsyncSession):
    try:
        db_user = User(email=user.email, password=Hash.bcrypt(user.password))
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        return db_user
    except Exception as e:
        print(f"An error occurred: {e}")
        await db.rollback()
        raise HTTPException(status_code=500, detail="An error occurred while creating the user.")


async def get_users(db: AsyncSession,skip: int = 0, limit: int = 10 ):
    try:
        print("Attempting to fetch users from the database")  
        users_response = select(User).offset(skip).limit(limit) 
        result = await db.execute(users_response)
        print("SQLAlchemy execute result: ", result)  
        users = result.scalars().all()
        print("Fetched users: ", users)  # Debugging
        return users
    except Exception as e:
        print(f"An error occurred while fetching users: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while fetching users.")


async def get_user(user_id: int, db: AsyncSession):
   try:
    user_response = select(User).filter_by(id=user_id) 
    result = await db.execute(user_response) 
    user = result.scalar()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user
   except Exception as e:
        print(f"An error occurred while fetching the user: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while fetching the user.")


async def update_user(user_id: int, user: UpdateUserRequest, db: AsyncSession):
    try:
        user_to_update = select(User).filter_by(id=user_id)
        result = await db.execute(user_to_update)
        db_user = result.scalar()

        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")

        for key, value in user.dict(exclude_unset=True).items():
            if key == "password": 
                hashed_password = Hash.bcrypt(value)
                setattr(db_user, key, hashed_password)
            else:
                setattr(db_user, key, value)

        await db.commit()
        await db.refresh(db_user)

        return db_user
    except Exception as e:
        print(f"An error occurred while updating the user: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while updating the user.")


async def delete_user(user_id: int, db: AsyncSession):
    try:
        user_to_delete = select(User).filter_by(id=user_id)
        result = await db.execute(user_to_delete)
        db_user = result.scalar()

        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")

        await db.delete(db_user)

        await db.commit()

        return {"detail": "User deleted"}
    except Exception as e:
        print(f"An error occurred while deleting the user: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while deleting the user.")
