import pytest
from unittest.mock import MagicMock, patch, AsyncMock
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.CreateUserRequest import CreateUserRequest
from src.models.UpdateUserRequest import UpdateUserRequest
from src.schemas.entities import User
from src.services.user_service import create_user, get_users, get_user, update_user, delete_user

# @pytest.mark.asyncio
# async def test_create_user():
#     db_mock = AsyncMock()
#     user_data = CreateUserRequest(email="test@example.com", password="password")
    
#     result = await create_user(user_data, db_mock)

#     db_mock.add.assert_called_once()
#     assert result.email == user_data.email

# @pytest.mark.asyncio
# async def test_get_users():
#     # Mock the database session
#     db_mock = MagicMock(spec=AsyncSession)

#     # Create a mock result object with scalars().all() method
#     mock_result = MagicMock()
#     mock_result.scalars.return_value.all.return_value = [User(email="test@example.com", password="hashed_password")]

#     # Mock db.execute() to return the mock result
#     db_mock.execute.return_value = mock_result

#     # Call the function to test
#     users = await get_users(db_mock)

#     # Assert the results
#     assert len(users) == 1
#     assert users[0].email == "test@example.com"

# @pytest.mark.asyncio
# async def test_get_user_not_found():
#     # Create a MagicMock for the database session
#     db_mock = MagicMock()

#     # Mock the execute method to return a scalar result of None
#     mock_execute = AsyncMock()
#     mock_execute.scalar.return_value = None  # Simulate that no user is found

#     # Set the db_mock to return the mock_execute when execute is called
#     db_mock.execute = AsyncMock(return_value=mock_execute)

#     # Test the case where the user is not found
#     with pytest.raises(HTTPException) as excinfo:
#         await get_user(1, db_mock)  # Call the function to get the user

#     # Assert the correct HTTPException is raised with the expected status code and detail
#     assert excinfo.value.status_code == 404
#     assert excinfo.value.detail == "User not found"



# @pytest.mark.asyncio
# async def test_update_user():
#     db_mock = AsyncMock()
#     existing_user = User(email="old@example.com", password="hashed_password")
#     db_mock.execute.return_value.scalar.return_value = existing_user
#     update_data = UpdateUserRequest(email="new@example.com", password="new_password")

#     updated_user = await update_user(1, update_data, db_mock)

#     assert updated_user.email == "new@example.com"
#     db_mock.commit.assert_called_once()

# @pytest.mark.asyncio
# async def test_delete_user():
#     db_mock = AsyncMock()
#     existing_user = User(email="delete@example.com", password="hashed_password")
#     db_mock.execute.return_value.scalar.return_value = existing_user
    
#     result = await delete_user(1, db_mock)

#     assert result == {"detail": "User deleted"}
#     db_mock.delete.assert_called_once()
#     db_mock.commit.assert_called_once()

# @pytest.mark.asyncio
# async def test_create_user_with_exception():
#     db_mock = AsyncMock()
#     user_data = CreateUserRequest(email="test@example.com", password="password")
#     db_mock.commit.side_effect = Exception("Database error")
    
#     with pytest.raises(HTTPException) as excinfo:
#         await create_user(user_data, db_mock)
    
#     assert excinfo.value.status_code == 500
#     assert excinfo.value.detail == "An error occurred while creating the user."
