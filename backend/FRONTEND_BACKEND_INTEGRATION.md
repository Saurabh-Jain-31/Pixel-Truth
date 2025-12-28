# 🔗 Frontend-Backend Integration Guide

## ✅ Integration Complete!

Your Pixel-Truth platform now has a fully integrated frontend and backend system.

## 🏗️ **Architecture Overview**

```
Pixel-Truth Platform
├── Frontend (React + Vite)
│   ├── Port: 3000 (development)
│   ├── Built to: dist/ (production)
│   └── Proxy: /api -> localhost:5000
├── Backend (FastAPI + Python)
│   ├── Port: 5000
│   ├── API Routes: /api/*
│   └── Serves: Frontend + API
└── Database (MongoDB)
    └── Collections: users, image_analyses, etc.
```

## 🚀 **How to Run**

### **Option 1: Development Mode (Recommended for development)**
```bash
# Run both frontend and backend separately
python run_dev.py

# Or manually:
# Terminal 1 - Backend
python start.py

# Terminal 2 - Frontend  
npm run dev
```

**Access:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:5000
- API Docs: http://localhost:5000/docs

### **Option 2: Production Mode (Single server)**
```bash
# Build and run integrated app
python build_and_run.py

# Or manually:
npm run build
python start.py
```

**Access:**
- Full App: http://localhost:5000
- API Docs: http://localhost:5000/docs

## 🔌 **API Integration Points**

### **Authentication**
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login  
- `GET /api/auth/me` - Get current user
- `GET /api/auth/test` - Test connection
- `POST /api/auth/logout` - Logout

### **File Upload & Analysis**
- `POST /api/upload` - Upload image file
- `POST /api/analyze/analyze` - Analyze uploaded file
- `GET /api/history` - Get analysis history

### **Static Files**
- `/uploads/*` - Uploaded files
- `/assets/*` - Frontend assets
- `/*` - SPA routing (serves React app)

## 🔧 **Configuration**

### **Frontend (Vite)**
```javascript
// vite.config.js
server: {
  proxy: {
    '/api': 'http://localhost:5000',
    '/uploads': 'http://localhost:5000'
  }
}
```

### **Backend (FastAPI)**
```python
# Port 5000 (matches frontend expectations)
# CORS enabled for localhost:3000
# Static file serving for built frontend
```

## 📁 **File Structure**
```
backend/
├── src/                    # React frontend source
├── dist/                   # Built frontend (after npm run build)
├── app/                    # FastAPI backend
├── uploads/                # User uploaded files
├── package.json            # Frontend dependencies
├── requirements.txt        # Backend dependencies
├── vite.config.js         # Frontend build config
└── start.py               # Backend server
```

## 🎯 **Key Features Integrated**

### **Frontend Features**
- ✅ User authentication (login/register)
- ✅ File upload with drag & drop
- ✅ Image analysis results display
- ✅ Analysis history dashboard
- ✅ Responsive design
- ✅ Error handling & notifications

### **Backend Features**  
- ✅ JWT authentication
- ✅ File upload handling
- ✅ AI image detection (trained model)
- ✅ OSINT metadata analysis
- ✅ MongoDB data storage
- ✅ API documentation

### **AI Detection System**
- ✅ CNN model for image classification
- ✅ EXIF metadata extraction
- ✅ Quality metrics analysis
- ✅ Confidence scoring
- ✅ Results: authentic/ai_generated/manipulated

## 🔄 **Data Flow**

1. **User uploads image** → Frontend sends to `/api/upload`
2. **File saved** → Backend stores in `/uploads/` directory  
3. **Analysis triggered** → Frontend calls `/api/analyze/analyze`
4. **AI processing** → Backend runs ML model + OSINT analysis
5. **Results stored** → MongoDB saves analysis results
6. **Results displayed** → Frontend shows prediction + confidence
7. **History tracked** → User can view past analyses

## 🛠️ **Development Workflow**

### **Frontend Changes**
```bash
# Edit files in src/
# Changes auto-reload at localhost:3000
npm run dev
```

### **Backend Changes**  
```bash
# Edit files in app/
# Restart server to see changes
python start.py
```

### **Production Build**
```bash
# Build frontend for production
npm run build

# Run integrated server
python start.py
# Now serves frontend from dist/ at localhost:5000
```

## 🔍 **Testing the Integration**

1. **Start the application**:
   ```bash
   python run_dev.py
   ```

2. **Test authentication**:
   - Go to http://localhost:3000
   - Register a new account
   - Login with credentials

3. **Test file upload**:
   - Go to Upload page
   - Drag & drop an image
   - Click "Analyze Image"

4. **Test AI detection**:
   - Upload different types of images
   - Check analysis results
   - View history in Dashboard

## 🚨 **Troubleshooting**

### **Frontend not loading**
```bash
# Check if dist/ exists
ls dist/

# If not, build frontend
npm run build
```

### **API calls failing**
```bash
# Check backend is running on port 5000
curl http://localhost:5000/api/auth/test

# Check CORS settings in app/main.py
```

### **File uploads failing**
```bash
# Check uploads directory exists
mkdir uploads

# Check file permissions
chmod 755 uploads/
```

## 🎉 **Success!**

Your Pixel-Truth platform is now fully integrated with:
- ✅ React frontend with modern UI
- ✅ FastAPI backend with AI detection
- ✅ Trained ML model for image analysis
- ✅ OSINT metadata analysis
- ✅ User authentication & history
- ✅ Production-ready deployment

**The frontend and backend are now connected and working together!** 🚀