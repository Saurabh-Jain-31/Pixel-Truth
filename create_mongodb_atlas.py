#!/usr/bin/env python3
"""
Instructions to create MongoDB Atlas for Pixel-Truth
"""

def print_mongodb_setup_instructions():
    print("🗄️ MongoDB Atlas Setup for Render Deployment")
    print("=" * 60)
    print()
    
    print("📋 Quick Setup Steps:")
    print()
    
    print("1️⃣ Create MongoDB Atlas Account:")
    print("   • Go to: https://www.mongodb.com/atlas")
    print("   • Sign up for FREE account")
    print("   • Create new project: 'Pixel-Truth'")
    print()
    
    print("2️⃣ Create Free Cluster:")
    print("   • Click 'Create' → 'Shared' (FREE)")
    print("   • Choose AWS, region closest to you")
    print("   • Cluster name: 'Cluster0' (default)")
    print("   • Click 'Create Cluster'")
    print()
    
    print("3️⃣ Create Database User:")
    print("   • Go to 'Database Access'")
    print("   • Click 'Add New Database User'")
    print("   • Username: pixeltruth")
    print("   • Password: PixelTruth2024")
    print("   • Role: 'Read and write to any database'")
    print("   • Click 'Add User'")
    print()
    
    print("4️⃣ Configure Network Access:")
    print("   • Go to 'Network Access'")
    print("   • Click 'Add IP Address'")
    print("   • Choose 'Allow access from anywhere' (0.0.0.0/0)")
    print("   • Click 'Confirm'")
    print()
    
    print("5️⃣ Get Connection String:")
    print("   • Go to 'Clusters' → Click 'Connect'")
    print("   • Choose 'Connect your application'")
    print("   • Driver: Python, Version: 3.6 or later")
    print("   • Copy the connection string")
    print("   • Replace <password> with: PixelTruth2024")
    print()
    
    print("6️⃣ Add to Render Environment Variables:")
    print("   • Go to your Render service dashboard")
    print("   • Click 'Environment'")
    print("   • Add these variables:")
    print()
    print("   MONGODB_URL=mongodb+srv://pixeltruth:PixelTruth2024@cluster0.xxxxx.mongodb.net/pixel_truth_db")
    print("   DATABASE_NAME=pixel_truth_db")
    print("   SECRET_KEY=pixel-truth-production-secret-key-2024")
    print("   DEBUG=False")
    print()
    
    print("🚀 Alternative: Use Environment Variables in Render")
    print()
    print("If you don't want to set up MongoDB Atlas right now,")
    print("the app will work without database (using fallback mode).")
    print()
    print("Just add these environment variables to Render:")
    print("   SECRET_KEY=pixel-truth-production-secret-key-2024")
    print("   DEBUG=False")
    print()
    
    print("✅ Your app will:")
    print("   • Work with or without MongoDB")
    print("   • Store data in database if connected")
    print("   • Use fallback mode if database unavailable")
    print("   • Show real AI predictions in both cases")
    print()
    
    print("🔗 Test your deployment:")
    print("   • Visit: https://pixel-truth.onrender.com")
    print("   • Check logs for database connection status")
    print("   • Test login and image upload")

if __name__ == "__main__":
    print_mongodb_setup_instructions()