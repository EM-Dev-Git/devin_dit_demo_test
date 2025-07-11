from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class MinutesGenerateRequest(BaseModel):
    transcript_id: int = Field(..., description="トランスクリプトID")

class MinutesGenerateResponse(BaseModel):
    minutes_id: int
    transcript_id: int
    content: str
    created_at: datetime
    message: str

class MinutesResponse(BaseModel):
    id: int
    transcript_id: int
    user_id: int
    content: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class MinutesListResponse(BaseModel):
    minutes: list[MinutesResponse]
    total_count: int
