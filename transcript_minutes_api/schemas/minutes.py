from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class MinutesCreate(BaseModel):
    transcript_id: int = Field(..., description="ID of the transcript to generate minutes from")

class MinutesResponse(BaseModel):
    minutes_id: int
    content: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class MinutesDetailResponse(BaseModel):
    id: int
    transcript_id: int
    user_id: int
    content: str
    created_at: datetime
    transcript_filename: Optional[str] = None
    
    class Config:
        from_attributes = True
