from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from modules.database import get_db, User, Transcript, Minutes
from modules.auth import get_current_user
from modules.openai_client import openai_client
from schemas.minutes import MinutesGenerateRequest, MinutesGenerateResponse, MinutesListResponse
from modules.logger import get_logger

logger = get_logger(__name__)
router = APIRouter()

@router.post("/generate", response_model=MinutesGenerateResponse, status_code=status.HTTP_201_CREATED)
async def generate_minutes(
    request: MinutesGenerateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    logger.info("Minutes generation started", extra={
        "user_id": current_user.user_id,
        "transcript_id": request.transcript_id
    })
    
    transcript = db.query(Transcript).filter(
        Transcript.id == request.transcript_id,
        Transcript.user_id == current_user.id
    ).first()
    
    if not transcript:
        logger.warning("Transcript not found for minutes generation", extra={
            "user_id": current_user.user_id,
            "transcript_id": request.transcript_id
        })
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transcript not found"
        )
    
    try:
        minutes_content = await openai_client.generate_minutes(transcript.content)
        
        db_minutes = Minutes(
            transcript_id=transcript.id,
            user_id=current_user.id,
            content=minutes_content
        )
        
        db.add(db_minutes)
        db.commit()
        db.refresh(db_minutes)
        
        logger.info("Minutes generated successfully", extra={
            "user_id": current_user.user_id,
            "transcript_id": request.transcript_id,
            "minutes_id": db_minutes.id
        })
        
        return MinutesGenerateResponse(
            minutes_id=db_minutes.id,
            transcript_id=transcript.id,
            content=minutes_content,
            created_at=db_minutes.created_at,
            message="Minutes generated successfully"
        )
        
    except Exception as e:
        logger.error("Minutes generation failed", extra={
            "user_id": current_user.user_id,
            "transcript_id": request.transcript_id,
            "error": str(e)
        })
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate minutes: {str(e)}"
        )

@router.get("/list", response_model=MinutesListResponse)
async def list_minutes(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    logger.info("Listing minutes", extra={"user_id": current_user.user_id})
    
    minutes = db.query(Minutes).filter(Minutes.user_id == current_user.id).all()
    
    logger.info("Minutes retrieved", extra={
        "user_id": current_user.user_id,
        "minutes_count": len(minutes)
    })
    
    return MinutesListResponse(
        minutes=minutes,
        total_count=len(minutes)
    )

@router.get("/{minutes_id}")
async def get_minutes(
    minutes_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    logger.info("Getting minutes", extra={
        "user_id": current_user.user_id,
        "minutes_id": minutes_id
    })
    
    minutes = db.query(Minutes).filter(
        Minutes.id == minutes_id,
        Minutes.user_id == current_user.id
    ).first()
    
    if not minutes:
        logger.warning("Minutes not found", extra={
            "user_id": current_user.user_id,
            "minutes_id": minutes_id
        })
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Minutes not found"
        )
    
    logger.info("Minutes retrieved", extra={
        "user_id": current_user.user_id,
        "minutes_id": minutes_id
    })
    
    return minutes
