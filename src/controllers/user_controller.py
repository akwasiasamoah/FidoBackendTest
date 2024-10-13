from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from src.services import user_service
from src.database import get_db
from src.models.UserResponse import UserResponse
from src.models.CreateUserRequest import CreateUserRequest
from src.models.UpdateUserRequest import UpdateUserRequest

user_router = APIRouter(
)

@user_router.post("/", response_model=UserResponse,status_code=status.HTTP_201_CREATED)
async def create_user(request: CreateUserRequest, db: AsyncSession = Depends(get_db)):
    user = await user_service.create_user(request, db)
    return user;

@user_router.get("/", response_model=List[UserResponse],status_code=status.HTTP_200_OK)
async def read_users(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    users = await user_service.get_users(db,skip,limit)
    return users


@user_router.get("/{user_id}", response_model=UserResponse)
async def read_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await user_service.get_user(user_id,db)
    return user


@user_router.put("/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, update_request: UpdateUserRequest, db: AsyncSession = Depends(get_db)):
    db_user = await user_service.update_user(user_id,update_request,db)
    return db_user


@user_router.delete("/{user_id}", response_model=dict)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    response = await user_service.delete_user(user_id,db)
    return response

