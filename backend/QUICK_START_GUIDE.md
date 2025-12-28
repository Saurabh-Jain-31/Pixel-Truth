# 🚀 Quick Start Guide - Pixel-Truth Platform

## ✅ **Current Status: SERVERS ARE RUNNING!**

Your Pixel-Truth platform is now running with both frontend and backend servers active.

## 🌐 **Access Your Application**

### **Option 1: Frontend Development Server (Recommended)**
**URL**: http://localhost:3000
- Full React.js interface
- Hot reload for development
- All frontend features working

### **Option 2: Backend with Built Frontend**
**URL**: http://localhost:5000
- Integrated backend + frontend
- Production-like setup
- API documentation at /docs

## 🔧 **Current Server Status**

### ✅ **Backend Server**
- **Status**: Running ✅
- **Port**: 5000
- **URL**: http://localhost:5000
- **API**: http://localhost:5000/api/health
- **Docs**: http://localhost:5000/docs

### ✅ **Frontend Server**
- **Status**: Running ✅
- **Port**: 3000
- **URL**: http://localhost:3000
- **Framework**: React.js + Vite

## 🎯 **How to Access Your App**

1. **Open your web browser**
2. **Go to**: http://localhost:3000
3. **You should see**: Pixel-Truth homepage with navigation
4. **Features available**:
   - User registration/login
   - File upload interface
   - AI detection results
   - Analysis history

## 🔍 **If You See "Connection Refused"**

This usually means you need to start the servers. Here's how:

### **Start Backend Server**
```bash
# In terminal 1
cd backend
python simple_start.py
```

### **Start Frontend Server**
```bash
# In terminal 2
cd backend
npm run dev
```

## 🛠️ **Troubleshooting**

### **Problem**: "localhost refused to connect"
**Solution**: Make sure both servers are running
```bash
# Check if servers are running
curl http://localhost:5000/api/health  # Backend
curl http://localhost:3000             # Frontend
```

### **Problem**: Frontend shows 404
**Solution**: 
1. Make sure you're accessing http://localhost:3000 (not 5000)
2. Check if npm run dev is still running
3. Restart frontend: `npm run dev`

### **Problem**: API calls failing
**Solution**:
1. Backend should be on port 5000
2. Check: http://localhost:5000/docs
3. Restart backend: `python simple_start.py`

## 🎉 **What You Can Do Now**

### **1. Test the Homepage**
- Visit: http://localhost:3000
- Should see Pixel-Truth landing page

### **2. Test User Registration**
- Click "Register" or "Login"
- Create a new account
- Login with credentials

### **3. Test File Upload**
- Go to "Upload" page
- Drag & drop an image
- Click "Analyze Image"

### **4. Test AI Detection**
- Upload different types of images
- See AI detection results
- Check confidence scores

### **5. View Analysis History**
- Go to "Dashboard" or "History"
- See past analysis results

## 📊 **Expected Results**

When everything is working, you should see:
- ✅ Modern React.js interface
- ✅ User authentication working
- ✅ File upload with drag & drop
- ✅ AI analysis results
- ✅ Confidence scores and metadata
- ✅ Analysis history tracking

## 🚀 **Next Steps**

1. **Access the app**: http://localhost:3000
2. **Register an account**
3. **Upload and analyze images**
4. **Explore all features**

## 📞 **Still Having Issues?**

If you're still seeing "connection refused":

1. **Check if processes are running**:
   - Look for "uvicorn" process (backend)
   - Look for "vite" process (frontend)

2. **Restart everything**:
   ```bash
   # Stop all processes (Ctrl+C)
   # Then restart:
   python simple_start.py  # Terminal 1
   npm run dev            # Terminal 2
   ```

3. **Try the integrated version**:
   ```bash
   npm run build
   python simple_start.py
   # Then visit: http://localhost:5000
   ```

## 🎯 **Success Indicators**

You'll know it's working when:
- ✅ http://localhost:3000 shows the Pixel-Truth homepage
- ✅ You can register/login
- ✅ File upload interface appears
- ✅ AI analysis returns results

**Your Pixel-Truth AI detection platform is ready to use!** 🚀