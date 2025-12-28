#!/usr/bin/env python3
"""
Test script to verify upload and analysis functionality
"""
import requests
import os
from PIL import Image
import io

def create_test_image():
    """Create a simple test image"""
    # Create a simple 100x100 red image
    img = Image.new('RGB', (100, 100), color='red')
    
    # Save to bytes
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='JPEG')
    img_bytes.seek(0)
    
    return img_bytes

def test_upload_and_analysis():
    """Test the complete upload and analysis flow"""
    print("🧪 Testing Upload and Analysis Flow...")
    print("=" * 50)
    
    base_url = "http://localhost:5000"
    
    # Create test image
    test_image = create_test_image()
    
    try:
        # Step 1: Upload image
        print("📤 Step 1: Uploading image...")
        files = {'image': ('test_image.jpg', test_image, 'image/jpeg')}
        upload_response = requests.post(f"{base_url}/api/upload", files=files)
        
        if upload_response.status_code == 200:
            upload_data = upload_response.json()
            print(f"✅ Upload successful!")
            print(f"   Filename: {upload_data['filename']}")
            print(f"   Size: {upload_data['size']} bytes")
            
            # Step 2: Analyze image
            print("\n🔍 Step 2: Analyzing image...")
            analysis_data = {
                'filename': upload_data['filename'],
                'original_name': upload_data['original_name']
            }
            
            analysis_response = requests.post(f"{base_url}/api/analysis/analyze", data=analysis_data)
            
            if analysis_response.status_code == 200:
                analysis_result = analysis_response.json()
                print(f"✅ Analysis successful!")
                print(f"   Prediction: {analysis_result['prediction']}")
                print(f"   Confidence: {analysis_result['confidence_score']:.3f}")
                print(f"   Processing time: {analysis_result['processing_time']:.2f}s")
                print(f"   Model status: {analysis_result['metadata']['model_status']}")
                
                return True
            else:
                print(f"❌ Analysis failed: {analysis_response.status_code}")
                print(f"   Response: {analysis_response.text}")
                return False
        else:
            print(f"❌ Upload failed: {upload_response.status_code}")
            print(f"   Response: {upload_response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        return False

if __name__ == "__main__":
    success = test_upload_and_analysis()
    
    print("\n🎯 Test Summary:")
    print("=" * 50)
    if success:
        print("✅ Upload and Analysis flow working correctly!")
        print("🚀 Frontend should now be able to:")
        print("   1. Upload images successfully")
        print("   2. Get AI analysis results")
        print("   3. Display results to users")
    else:
        print("❌ Upload and Analysis flow has issues")
        print("🔧 Check server logs for more details")