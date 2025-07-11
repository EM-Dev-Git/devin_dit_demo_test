from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from modules.database import get_db, User
from modules.auth import verify_password, get_password_hash, create_access_token
from schemas.user import UserCreate, UserLogin, Token, UserResponse
from modules.logger import get_logger

logger = get_logger(__name__)
router = APIRouter()

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    logger.info("User registration attempt", extra={"user_id": user.user_id})
    
    db_user = db.query(User).filter(User.user_id == user.user_id).first()
    if db_user:
        logger.warning("User registration failed - user already exists", extra={"user_id": user.user_id})
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already registered"
        )
    
    hashed_password = get_password_hash(user.password)
    db_user = User(user_id=user.user_id, password_hash=hashed_password)
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    logger.info("User registered successfully", extra={"user_id": user.user_id, "db_user_id": db_user.id})
    return db_user

@router.post("/login", response_model=Token)
async def login_user(user: UserLogin, db: Session = Depends(get_db)):
    logger.info("User login attempt", extra={"user_id": user.user_id})
    
    db_user = db.query(User).filter(User.user_id == user.user_id).first()
    if not db_user or not verify_password(user.password, db_user.password_hash):
        logger.warning("User login failed - invalid credentials", extra={"user_id": user.user_id})
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect user_id or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": db_user.user_id})
    
    logger.info("User logged in successfully", extra={"user_id": user.user_id})
    return {"access_token": access_token, "token_type": "bearer"}
