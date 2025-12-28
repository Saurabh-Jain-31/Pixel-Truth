@echo off
echo 🚀 Building Full-Stack Pixel-Truth Application
echo ==============================================

echo 📦 Building Frontend...
cd frontend
call npm install
call npm run build

echo 📁 Copying frontend build to backend...
cd ..
if exist backend\static rmdir /s /q backend\static
xcopy frontend\dist backend\static /e /i /y

echo 🐍 Installing backend dependencies...
cd backend
pip install -r requirements.txt

echo 🌟 Starting integrated application...
echo Frontend: http://localhost:8000
echo API docs: http://localhost:8000/docs
python start.py