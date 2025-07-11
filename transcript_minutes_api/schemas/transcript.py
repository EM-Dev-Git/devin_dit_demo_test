from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class TranscriptCreate(BaseModel):
    filename: str = Field(..., description="Original filename")
    content: str = Field(..., description="Transcript content")

class TranscriptResponse(BaseModel):
    id: int
    user_id: int
    filename: str
    content: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class TranscriptUploadResponse(BaseModel):
    transcript_id: int
    filename: str
    message: str
