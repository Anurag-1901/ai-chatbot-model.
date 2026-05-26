from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import SessionLocal
from models.schemas import UserCreate, UserLogin, UserResponse
from services.auth_service import create_user, authenticate_user

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/signup", response_model=UserResponse)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, user)

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    token = authenticate_user(db, user)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"access_token": token, "token_type": "bearer"}
