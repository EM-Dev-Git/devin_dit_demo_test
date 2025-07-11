from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class TranscriptUploadResponse(BaseModel):
    id: int
    filename: str
    content_length: int
    message: str
    created_at: datetime

class TranscriptResponse(BaseModel):
    id: int
    filename: str
    content: str
    created_at: datetime
    user_id: int
    
    class Config:
        from_attributes = True

class TranscriptListResponse(BaseModel):
    transcripts: list[TranscriptResponse]
    total_count: int

class TranscriptRequest(BaseModel):
    transcript_id: int = Field(..., description="トランスクリプトID")
