@echo off
REM Full-stack build and deployment script for Windows

echo 🚀 Building Full-Stack Pixel-Truth Application
echo ==============================================

REM Step 1: Build Frontend
echo 📦 Building Frontend...
cd frontend
call npm install
call npm run build

REM Step 2: Copy frontend build to backend static directory
echo 📁 Copying frontend build to backend...
cd ..
if exist backend\static rmdir /s /q backend\static
xcopy frontend\dist backend\static /e /i /y

REM Step 3: Install backend dependencies
echo 🐍 Installing backend dependencies...
cd backend
pip install -r requirements.txt

REM Step 4: Start the integrated application
echo 🌟 Star