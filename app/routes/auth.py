# app/routes/auth.py

from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from app import models, database
from app.utils import auth_helper, email_service
from pydantic import BaseModel, EmailStr

router = APIRouter()

class UserSignup(BaseModel):
    email: EmailStr
    password: str
    role: str  # 'client' or 'ops'

class UserLogin(BaseModel):
    email: EmailStr
    password: str

@router.post("/signup")
def signup(user: UserSignup, db: Session = Depends(database.get_db)):
    existing = db.query(models.User).filter_by(email=user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed = auth_helper.hash_password(user.password)
    db_user = models.User(email=user.email, password=hashed, role=user.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    token = auth_helper.create_access_token({"sub": user.email})
    email_service.send_verification_email(user.email, token)
    return {"message": "Signup successful. Verify your email.", "verify_url": f"/auth/verify?token={token}"}

@router.get("/verify")
def verify_email(token: str, db: Session = Depends(database.get_db)):
    data = auth_helper.decode_token(token)
    if not data:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    user = db.query(models.User).filter_by(email=data["sub"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.is_verified = True
    db.commit()
    return {"message": "Email verified!"}

@router.post("/login")
def login(data: UserLogin, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter_by(email=data.email).first()
    if not user or not auth_helper.verify_password(data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not user.is_verified:
        raise HTTPException(status_code=403, detail="Please verify your email first")

    token = auth_helper.create_access_token({"sub": user.email, "role": user.role})
    return {"access_token": token, "token_type": "bearer"}
