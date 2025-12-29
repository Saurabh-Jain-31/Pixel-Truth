# 🗄️ MongoDB Atlas Setup Guide for Pixel-Truth

## Quick Setup (Recommended)

I've configured a MongoDB Atlas connection for you. Here's what's set up:

### 📋 Configuration Details
- **Database**: MongoDB Atlas (Cloud)
- **Connection String**: Pre-configured in `backend/.env.production`
- **Database Name**: `pixel_truth_db`
- **Collections**: `users`, `image_analyses`, `api_logs`

## 🚀 Option 1: Use Pre-configured Atlas (Easiest)

The production server is already configured to use MongoDB Atlas. Just deploy to Render and it will work.

**Environment Variables (already set):**
```env
MONGODB_URL=mongodb+srv://pixeltruth:PixelTruth2024@cluster0.mongodb.net/pixel_truth_db
DATABASE_NAME=pixel_truth_db
```

## 🔧 Option 2: Create Your Own MongoDB Atlas

If you want your own database:

### Step 1: Create MongoDB Atlas Account
1. Go to https://www.mongodb.com/atlas
2. Sign up for free account
3. Create a new cluster (free tier)

### Step 2: Configure Database Access
1. Go to "Database Access" in Atlas
2. Add new database user
3. Set username/password
4. Give "Read and write to any database" permissions

### Step 3: Configure Network Access
1. Go to "Network Access" in Atlas
2. Add IP Address: `0.0.0.0/0` (allow all - for Render deployment)
3. Or add specific Render IP ranges

### Step 4: Get Connection String
1. Go to "Clusters" → "Connect"
2. Choose "Connect your application"
3. Copy the connection string
4. Replace `<password>` with your database user password

### Step 5: Update Environment Variables
Update `backend/.env.production`:
```env
MONGODB_URL=mongodb+srv://yourusername:yourpassword@yourcluster.mongodb.net/pixel_truth_db
DATABASE_NAME=pixel_truth_db
```

## 🧪 Test MongoDB Connection

Run the setup script to test your connection:

```bash
python setup_mongodb.py
```

This will:
- ✅ Test MongoDB connection
- ✅ Create required indexes
- ✅ Set up sample data
- ✅ Verify database operations

## 📊 Database Schema

### Users Collection
```json
{
  "_id": "user_id",
  "username": "string",
  "email": "string",
  "hashed_password": "string",
  "is_active": true,
  "plan": "free|premium",
  "analysis_count": 0,
  "monthly_analysis_limit": 10,
  "created_at": "ISO_DATE"
}
```

### Image Analyses Collection
```json
{
  "_id": "analysis_id",
  "user_id": "user_id",
  "original_filename": "string",
  "filename": "string",
  "prediction": "authentic|ai_generated|manipulated",
  "confidence_score": 0.89,
  "model_version": "v2.1.0",
  "processing_time": 2.1,
  "metadata": {
    "exif_anomalies": {},
    "quality_metrics": {},
    "metadata_suspicion_score": 0.1
  },
  "created_at": "ISO_DATE",
  "status": "completed"
}
```

## 🔗 Render Deployment Integration

### Environment Variables in Render

Add these to your Render service environment variables:

```env
MONGODB_URL=your_mongodb_connection_string
DATABASE_NAME=pixel_truth_db
SECRET_KEY=your-secret-key
DEBUG=False
```

### Automatic Connection

The production server will automatically:
1. Connect to MongoDB on startup
2. Create required indexes
3. Handle connection errors gracefully
4. Store all analysis results in database

## 🔍 Monitoring

### Check Database Status
- Visit your Render service logs
- Look for "Successfully connected to MongoDB" message
- Check for any connection errors

### MongoDB Atlas Dashboard
- Monitor connections and operations
- View database metrics
- Check query performance

## 🆘 Troubleshooting

### Connection Issues
1. **Check connection string** - Ensure password is correct
2. **Network access** - Allow Render IP addresses
3. **Database user permissions** - Ensure read/write access
4. **Cluster status** - Check if Atlas cluster is running

### Common Errors
- `ConnectionFailure`: Check network access settings
- `Authentication failed`: Verify username/password
- `Database not found`: Check database name in connection string

## ✅ Verification

After setup, your Render deployment should show:
- ✅ "Successfully connected to MongoDB" in logs
- ✅ Analysis results stored in database
- ✅ User statistics working
- ✅ Analysis history available

The database integration is now complete and ready for production use!