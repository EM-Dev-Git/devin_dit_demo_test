from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    user_id: str = Field(..., min_length=3, max_length=50, description="ユーザーID")
    password: str = Field(..., min_length=6, description="パスワード")

class UserLogin(BaseModel):
    user_id: str = Field(..., description="ユーザーID")
    password: str = Field(..., description="パスワード")

class UserResponse(BaseModel):
    id: int
    user_id: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    user_id: Optional[str] = None
