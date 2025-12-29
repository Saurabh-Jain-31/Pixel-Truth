@echo off
echo 🚀 Starting Pixel Truth Production Server with Real AI Model
echo.
echo 🤖 AI Model: Your trained CNN model
echo 🗄️ Database: MongoDB integration  
echo 🔍 Analysis: Real AI detection + OSINT
echo.

cd backend
echo Installing dependencies...
pip install -r requirements.txt

echo.
echo 🌐 Starting server on http://localhost:5000
echo 📖 API Documentation: http://localhost:5000/docs
echo.

python production_server.py

pause