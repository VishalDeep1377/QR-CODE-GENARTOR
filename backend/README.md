# QR Code Studio API

## Setup (Windows PowerShell)
```powershell
cd backend
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
Copy-Item .env.example .env
uvicorn app.main:app --reload --port 8000
```

API docs: http://localhost:8000/docs

MongoDB is optional. Without `MONGODB_URI`, local development uses SQLite at `backend/data/qr_studio.db`. Add a MongoDB Atlas connection string to `.env` to use MongoDB. For production, set `PUBLIC_BASE_URL` to the public backend URL and `FRONTEND_ORIGIN` to the deployed frontend URL.
