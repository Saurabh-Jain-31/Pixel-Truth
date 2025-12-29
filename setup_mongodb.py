#!/usr/bin/env python3
"""
MongoDB Atlas setup and connection test for Pixel-Truth
"""
import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ConnectionFailure
from dotenv import load_dotenv

# Load environment variables
load_dotenv('backend/.env.production')

async def test_mongodb_connection():
    """Test MongoDB Atlas connection"""
    
    mongodb_url = os.getenv('MONGODB_URL', 'mongodb://localhost:27017')
    database_name = os.getenv('DATABASE_NAME', 'pixel_truth_db')
    
    print("🔍 Testing MongoDB Connection...")
    print(f"📡 Database URL: {mongodb_url[:50]}...")
    print(f"🗄️ Database Name: {database_name}")
    print()
    
    try:
        # Create client
        client = AsyncIOMotorClient(mongodb_url)
        
        # Test connection
        await client.admin.command('ping')
        print("✅ Successfully connected to MongoDB Atlas!")
        
        # Get database
        db = client[database_name]
        
        # Test database operations
        print("🧪 Testing database operations...")
        
        # Insert test document
        test_doc = {
            "test": True,
            "message": "MongoDB connection test",
            "timestamp": "2024-01-01T00:00:00Z"
        }
        
        result = await db.test_collection.insert_one(test_doc)
        print(f"✅ Test document inserted: {result.inserted_id}")
        
        # Read test document
        found_doc = await db.test_collection.find_one({"_id": result.inserted_id})
        print(f"✅ Test document retrieved: {found_doc['message']}")
        
        # Delete test document
        await db.test_collection.delete_one({"_id": result.inserted_id})
        print("✅ Test document cleaned up")
        
        # Create indexes for production
        print("🔧 Creating production indexes...")
        
        # Users collection indexes
        await db.users.create_index("email", unique=True)
        await db.users.create_index("username", unique=True)
        print("✅ User indexes created")
        
        # Analysis collections indexes
        await db.image_analyses.create_index("user_id")
        await db.image_analyses.create_index("created_at")
        print("✅ Analysis indexes created")
        
        # API logs index
        await db.api_logs.create_index("timestamp")
        await db.api_logs.create_index("user_id")
        print("✅ API log indexes created")
        
        print()
        print("🎉 MongoDB Atlas setup completed successfully!")
        print("📊 Database is ready for production use")
        
        # Close connection
        client.close()
        
    except ConnectionFailure as e:
        print(f"❌ Failed to connect to MongoDB: {e}")
        print()
        print("🔧 Troubleshooting steps:")
        print("1. Check if MongoDB Atlas cluster is running")
        print("2. Verify connection string is correct")
        print("3. Check network access settings in Atlas")
        print("4. Ensure database user has proper permissions")
        
    except Exception as e:
        print(f"❌ Error during MongoDB setup: {e}")

async def create_sample_data():
    """Create sample data for testing"""
    
    mongodb_url = os.getenv('MONGODB_URL', 'mongodb://localhost:27017')
    database_name = os.getenv('DATABASE_NAME', 'pixel_truth_db')
    
    try:
        client = AsyncIOMotorClient(mongodb_url)
        db = client[database_name]
        
        print("📝 Creating sample data...")
        
        # Sample user
        sample_user = {
            "_id": "demo_user_id",
            "username": "demo_user",
            "email": "demo@pixeltruth.com",
            "hashed_password": "$2b$12$sample_hash",
            "is_active": True,
            "plan": "free",
            "analysis_count": 0,
            "monthly_analysis_limit": 10,
            "created_at": "2024-01-01T00:00:00Z"
        }
        
        await db.users.replace_one({"_id": "demo_user_id"}, sample_user, upsert=True)
        print("✅ Sample user created")
        
        # Sample analysis
        sample_analysis = {
            "_id": "sample_analysis_123",
            "user_id": "demo_user_id",
            "original_filename": "sample_image.jpg",
            "filename": "sample_123.jpg",
            "prediction": "authentic",
            "confidence_score": 0.89,
            "model_version": "v2.1.0",
            "processing_time": 2.1,
            "metadata": {
                "exif_anomalies": {"missing_exif": False},
                "quality_metrics": {"sharpness": 850, "noise_level": 25},
                "metadata_suspicion_score": 0.1
            },
            "created_at": "2024-01-01T00:00:00Z",
            "status": "completed"
        }
        
        await db.image_analyses.replace_one({"_id": "sample_analysis_123"}, sample_analysis, upsert=True)
        print("✅ Sample analysis created")
        
        print("🎯 Sample data ready for testing")
        
        client.close()
        
    except Exception as e:
        print(f"❌ Error creating sample data: {e}")

if __name__ == "__main__":
    print("🚀 MongoDB Atlas Setup for Pixel-Truth")
    print("=" * 50)
    
    # Test connection
    asyncio.run(test_mongodb_connection())
    
    print()
    print("📝 Creating sample data for testing...")
    asyncio.run(create_sample_data())
    
    print()
    print("✅ MongoDB setup complete!")
    print("🔗 Your Render app can now connect to MongoDB Atlas")