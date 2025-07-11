from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from modules.database import get_db, User, Transcript
from modules.auth import get_current_user
from modules.graph_client import graph_client
from modules.transcript_processor import transcript_processor
from schemas.graph import (
    GraphMeetingListRequest, GraphMeetingListResponse,
    GraphTranscriptListRequest, GraphTranscriptListResponse,
    GraphTranscriptImportRequest, GraphTranscriptImportResponse,
    GraphMeetingResponse, GraphTranscriptResponse
)
from modules.logger import get_logger

logger = get_logger(__name__)
router = APIRouter()

@router.post("/meetings", response_model=GraphMeetingListResponse)
async def list_meetings(
    request: GraphMeetingListRequest,
    current_user: User = Depends(get_current_user)
):
    logger.info("Listing Microsoft Graph meetings", extra={
        "user_id": current_user.user_id,
        "start_date": request.start_date,
        "end_date": request.end_date
    })
    
    try:
        if request.start_date and request.end_date:
            meetings = await graph_client.search_meetings_by_date_range(
                request.start_date, request.end_date, request.user_id
            )
        else:
            meetings = await graph_client.get_online_meetings(request.user_id)
        
        graph_meetings = [
            GraphMeetingResponse(
                id=meeting.get("id", ""),
                subject=meeting.get("subject"),
                start_date_time=meeting.get("startDateTime"),
                end_date_time=meeting.get("endDateTime"),
                join_web_url=meeting.get("joinWebUrl"),
                organizer=meeting.get("organizer")
            )
            for meeting in meetings
        ]
        
        logger.info("Microsoft Graph meetings retrieved", extra={
            "user_id": current_user.user_id,
            "meeting_count": len(graph_meetings)
        })
        
        return GraphMeetingListResponse(
            meetings=graph_meetings,
            total_count=len(graph_meetings)
        )
        
    except Exception as e:
        logger.error("Failed to retrieve Microsoft Graph meetings", extra={
            "user_id": current_user.user_id,
            "error": str(e)
        })
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve meetings: {str(e)}"
        )

@router.post("/meetings/{meeting_id}/transcripts", response_model=GraphTranscriptListResponse)
async def list_meeting_transcripts(
    meeting_id: str,
    current_user: User = Depends(get_current_user)
):
    logger.info("Listing meeting transcripts", extra={
        "user_id": current_user.user_id,
        "meeting_id": meeting_id
    })
    
    try:
        transcripts = await graph_client.get_meeting_transcripts(meeting_id)
        
        graph_transcripts = [
            GraphTranscriptResponse(
                id=transcript.get("id", ""),
                meeting_id=meeting_id,
                created_date_time=transcript.get("createdDateTime"),
                transcript_content_url=transcript.get("transcriptContentUrl")
            )
            for transcript in transcripts
        ]
        
        logger.info("Meeting transcripts retrieved", extra={
            "user_id": current_user.user_id,
            "meeting_id": meeting_id,
            "transcript_count": len(graph_transcripts)
        })
        
        return GraphTranscriptListResponse(
            transcripts=graph_transcripts,
            meeting_id=meeting_id,
            total_count=len(graph_transcripts)
        )
        
    except Exception as e:
        logger.error("Failed to retrieve meeting transcripts", extra={
            "user_id": current_user.user_id,
            "meeting_id": meeting_id,
            "error": str(e)
        })
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve transcripts: {str(e)}"
        )

@router.post("/import", response_model=GraphTranscriptImportResponse, status_code=status.HTTP_201_CREATED)
async def import_transcript_from_graph(
    request: GraphTranscriptImportRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    logger.info("Importing transcript from Microsoft Graph", extra={
        "user_id": current_user.user_id,
        "meeting_id": request.meeting_id,
        "transcript_id": request.transcript_id
    })
    
    try:
        content = await graph_client.get_transcript_content(
            request.meeting_id, request.transcript_id
        )
        
        processed_content = transcript_processor._preprocess_content(content)
        
        filename = request.custom_filename or f"graph_transcript_{request.meeting_id}_{request.transcript_id}.txt"
        
        db_transcript = Transcript(
            user_id=current_user.id,
            filename=filename,
            content=processed_content
        )
        
        db.add(db_transcript)
        db.commit()
        db.refresh(db_transcript)
        
        logger.info("Transcript imported successfully from Microsoft Graph", extra={
            "user_id": current_user.user_id,
            "transcript_id": db_transcript.id,
            "meeting_id": request.meeting_id,
            "graph_transcript_id": request.transcript_id
        })
        
        return GraphTranscriptImportResponse(
            transcript_id=db_transcript.id,
            filename=filename,
            meeting_id=request.meeting_id,
            graph_transcript_id=request.transcript_id,
            message="Transcript imported successfully from Microsoft Graph"
        )
        
    except Exception as e:
        logger.error("Failed to import transcript from Microsoft Graph", extra={
            "user_id": current_user.user_id,
            "meeting_id": request.meeting_id,
            "transcript_id": request.transcript_id,
            "error": str(e)
        })
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to import transcript: {str(e)}"
        )
