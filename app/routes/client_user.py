# app/routes/client_user.py

import os
import uuid
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app import models, database
from app.utils.auth_helper import decode_token
from fastapi.security import OAuth2PasswordBearer

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# In-memory store for download tokens (can use Redis in production)
download_links = {}

def get_current_client_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    payload = decode_token(token)
    if not payload or payload["role"] != "client":
        raise HTTPException(status_code=403, detail="Access denied")
    user = db.query(models.User).filter_by(email=payload["sub"]).first()
    return user

@router.get("/files")
def list_files(db: Session = Depends(database.get_db), user: models.User = Depends(get_current_client_user)):
    files = db.query(models.File).all()
    return [{"id": f.id, "filename": f.filename, "uploaded_by": f.uploader.email} for f in files]

@router.get("/download-link/{file_id}")
def get_download_link(file_id: int, db: Session = Depends(database.get_db), user: models.User = Depends(get_current_client_user)):
    file = db.query(models.File).filter_by(id=file_id).first()
    if not file:
        raise HTTPException(status_code=404, detail="File not found")

    token = str(uuid.uuid4())
    download_links[token] = file.filename
    return {"download-link": f"/client/download/{token}", "message": "success"}

@router.get("/download/{token}")
def download_file(token: str, user: models.User = Depends(get_current_client_user)):
    if token not in download_links:
        raise HTTPException(status_code=403, detail="Invalid or expired download token")

    file_path = download_links[token]
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(file_path, filename=os.path.basename(file_path), media_type='application/octet-stream')
