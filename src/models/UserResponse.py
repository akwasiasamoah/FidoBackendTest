from pydantic import BaseModel

class UserResponse(BaseModel):
    email: str
    class Config:
        orm_mode = True