from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List, Dict, Any

class GraphMeetingResponse(BaseModel):
    id: str
    subject: Optional[str] = None
    start_date_time: Optional[str] = None
    end_date_time: Optional[str] = None
    join_web_url: Optional[str] = None
    organizer: Optional[Dict[str, Any]] = None

class GraphTranscriptResponse(BaseModel):
    id: str
    meeting_id: str
    created_date_time: Optional[str] = None
    transcript_content_url: Optional[str] = None

class GraphTranscriptImportRequest(BaseModel):
    meeting_id: str = Field(..., description="Microsoft Graph meeting ID")
    transcript_id: str = Field(..., description="Microsoft Graph transcript ID")
    custom_filename: Optional[str] = Field(None, description="Custom filename for the imported transcript")

class GraphTranscriptImportResponse(BaseModel):
    transcript_id: int
    filename: str
    meeting_id: str
    graph_transcript_id: str
    message: str

class GraphMeetingListRequest(BaseModel):
    start_date: Optional[str] = Field(None, description="Start date filter (ISO format)")
    end_date: Optional[str] = Field(None, description="End date filter (ISO format)")
    user_id: Optional[str] = Field("me", description="User ID to query meetings for")

class GraphMeetingListResponse(BaseModel):
    meetings: List[GraphMeetingResponse]
    total_count: int

class GraphTranscriptListRequest(BaseModel):
    meeting_id: str = Field(..., description="Microsoft Graph meeting ID")

class GraphTranscriptListResponse(BaseModel):
    transcripts: List[GraphTranscriptResponse]
    meeting_id: str
    total_count: int
