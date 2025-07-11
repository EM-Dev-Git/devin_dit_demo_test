from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from modules.database import get_db, User, Transcript
from modules.auth import get_current_user
from modules.transcript_processor import transcript_processor
from schemas.transcript import TranscriptResponse, TranscriptUploadResponse
from modules.logger import get_logger

logger = get_logger(__name__)
router = APIRouter()

@router.post("/upload", response_model=TranscriptUploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_transcript(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    logger.info("Transcript upload started", extra={"user_id": current_user.user_id, "filename": file.filename})
    
    try:
        processed_content = await transcript_processor.process_file(file)
        
        db_transcript = Transcript(
            user_id=current_user.id,
            filename=file.filename,
            content=processed_content
        )
        
        db.add(db_transcript)
        db.commit()
        db.refresh(db_transcript)
        
        logger.info("Transcript uploaded successfully", extra={
            "user_id": current_user.user_id,
            "transcript_id": db_transcript.id,
            "filename": file.filename
        })
        
        return TranscriptUploadResponse(
            transcript_id=db_transcript.id,
            filename=file.filename,
            message="Transcript uploaded successfully"
        )
        
    except Exception as e:
        logger.error("Transcript upload failed", extra={
            "user_id": current_user.user_id,
            "filename": file.filename,
            "error": str(e)
        })
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to upload transcript"
        )

@router.get("/list", response_model=List[TranscriptResponse])
async def list_transcripts(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    logger.info("Listing transcripts", extra={"user_id": current_user.user_id})
    
    transcripts = db.query(Transcript).filter(Transcript.user_id == current_user.id).all()
    
    logger.info("Transcripts listed", extra={
        "user_id": current_user.user_id,
        "count": len(transcripts)
    })
    
    return transcripts

@router.get("/{transcript_id}", response_model=TranscriptResponse)
async def get_transcript(
    transcript_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    logger.info("Getting transcript", extra={
        "user_id": current_user.user_id,
        "transcript_id": transcript_id
    })
    
    transcript = db.query(Transcript).filter(
        Transcript.id == transcript_id,
        Transcript.user_id == current_user.id
    ).first()
    
    if not transcript:
        logger.warning("Transcript not found", extra={
            "user_id": current_user.user_id,
            "transcript_id": transcript_id
        })
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transcript not found"
        )
    
    logger.info("Transcript retrieved", extra={
        "user_id": current_user.user_id,
        "transcript_id": transcript_id
    })
    
    return transcript
