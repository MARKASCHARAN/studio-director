# ⚙️ Setup Guide — StudioDirector AI

## 1. Frontend Setup

cd frontend
npm install
npm run dev

## 2. Backend Setup

cd backend
pip install -r requirements.txt
uvicorn main:app --reload

## 3. Worker Setup

cd worker
pip install -r requirements.txt
python worker.py

## 4. Environment Variables

Create `.env` in backend:

FIBO_API_KEY=
GOOGLE_API_KEY=
SUPABASE_URL=
SUPABASE_KEY=
S3_BUCKET=
