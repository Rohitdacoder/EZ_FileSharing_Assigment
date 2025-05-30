# app/main.py

from fastapi import FastAPI
from app.routes import auth, ops_user, client_user

# app/main.py
from dotenv import load_dotenv
load_dotenv()  # Load .env into os.environ


app = FastAPI()

# Routes
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(ops_user.router, prefix="/ops", tags=["Ops User"])
app.include_router(client_user.router, prefix="/client", tags=["Client User"])

@app.get("/")
def read_root():
    return {"message": "Secure File Sharing API"}
