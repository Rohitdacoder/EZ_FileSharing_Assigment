# app/routes/ops_user.py

import os
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, database
from app.utils.auth_helper import decode_token
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

UPLOAD_DIR = "files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

ALLOWED_EXTENSIONS = ['.docx', '.pptx', '.xlsx']

def get_current_ops_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    payload = decode_token(token)
    if not payload or payload["role"] != "ops":
        raise HTTPException(status_code=403, detail="Access denied")
    user = db.query(models.User).filter_by(email=payload["sub"]).first()
    return user

@router.post("/upload")
def upload_file(file: UploadFile = File(...), db: Session = Depends(database.get_db), user: models.User = Depends(get_current_ops_user)):
    ext = os.path.splitext(file.filename)[1]
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Invalid file type")

    file_path = os.path.join(UPLOAD_DIR, f"{datetime.utcnow().timestamp()}_{file.filename}")
    with open(file_path, "wb") as f:
        f.write(file.file.read())

    db_file = models.File(filename=file_path, uploader_id=user.id)
    db.add(db_file)
    db.commit()
    return {"message": "File uploaded successfully", "filename": file.filename}
