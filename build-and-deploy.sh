#!/bin/bash
# Full-stack build and deployment script

echo "🚀 Building Full-Stack Pixel-Truth Application"
echo "=============================================="

# Step 1: Build Frontend
echo "📦 Building Frontend..."
cd frontend
npm install
npm run build

# Step 2: Copy frontend build to backend static directory
echo "📁 Copying frontend build to backend..."
cd ..
rm -rf backend/static
cp -r frontend/dist backend/static

# Step 3: Install backend dependencies
echo "🐍 Installing backend dependencies..."
cd backend
pip install -r requirements.txt

# Step 4: Start the integrated application
echo "🌟 Starting integrated application..."
echo "Frontend will be served from: http://localhost:8000"
echo "API documentation: http://localhost:8000/docs"
python start.py