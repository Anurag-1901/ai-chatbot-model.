from sqlalchemy.orm import Session
from models.user import User
from core.security import hash_password, verify_password, create_access_token
from models.schemas import UserCreate, UserLogin

def create_user(db: Session, user: UserCreate):
    hashed_pw = hash_password(user.password)
    db_user = User(username=user.username, email=user.email, hashed_password=hashed_pw)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, login: UserLogin):
    user = db.query(User).filter(User.username == login.username).first()
    if not user or not verify_password(login.password, user.hashed_password):
        return None
    return create_access_token({"sub": user.username})
