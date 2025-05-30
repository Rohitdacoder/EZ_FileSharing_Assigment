# 🔐 Secure File Sharing API (FastAPI)

A secure backend system for file sharing between two types of users:
- **Ops User**: Can upload `.docx`, `.pptx`, `.xlsx` files
- **Client User**: Can sign up, verify email, login, view and download files via secure encrypted links

---

## 🚀 Features

- ✅ REST API using FastAPI
- 🔐 JWT-based Authentication
- 📧 Email verification with **SendGrid**
- 🗃️ SQLite + SQLAlchemy ORM
- 📁 File upload with type restrictions
- 🔗 Encrypted secure download links
- ✅ Role-based access (Ops / Client)

---

## 🛠️ Tech Stack

- **Backend**: FastAPI, SQLAlchemy
- **Auth**: JWT (via python-jose), bcrypt (via passlib)
- **Database**: SQLite (easily swappable with PostgreSQL)
- **Email**: SendGrid API
- **Testing**: Pytest + TestClient
- **Deployment-ready**: Uvicorn

---

## 📁 Folder Structure

```
secure-file-sharing-api/
├── app/
│   ├── main.py
│   ├── models.py
│   ├── database.py
│   ├── routes/
│   ├── utils/
├── files/                  # Uploaded files
├── tests/                  # Test cases
├── .env                    # Secrets (ignored by Git)
├── requirements.txt
└── README.md
```

---

## 🔧 Setup Instructions

### 1. Clone the Repo
```bash
git clone https://github.com/Rohitdacoder/secure-file-sharing-api.git
cd secure-file-sharing-api
```

### 2. Create Virtual Environment
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# OR
.venv\Scripts\activate     # Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Create `.env` File
```env
SENDGRID_API_KEY=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
EMAIL_USER=rohitsharma3860@gmail.com
```

### 5. Initialize the Database
```bash
python -m app.create_db
```

---

## ▶️ Run the Server

```bash
uvicorn app.main:app --reload
```

Then open Swagger UI at:
👉 [http://localhost:8000/docs](http://localhost:8000/docs)

---

## ✅ API Endpoints

### 🔐 Auth
- `POST /auth/signup` – Sign up user (returns email verification link)
- `GET /auth/verify?token=...` – Verify email
- `POST /auth/login` – Login and get JWT token

### 🔧 Ops User
- `POST /ops/upload` – Upload `.docx`, `.pptx`, `.xlsx` files (JWT required)

### 👤 Client User
- `GET /client/files` – List available files
- `GET /client/download-link/{file_id}` – Get secure download link
- `GET /client/download/{token}` – Download file via secure token

---

## 🧪 Run Tests
```bash
pytest tests/
```

---


## 📦 Deployment Tips

- Use `uvicorn` with `gunicorn` for production
- Use Docker or services like Render/Heroku for deployment
- Keep `.env` secrets safe!

---

## ✨ Contributions

PRs and improvements are welcome! Let's make secure sharing easier.

---

## 📄 License

MIT License © 2025 Rohit Sharma
