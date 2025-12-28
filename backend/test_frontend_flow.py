#!/usr/bin/env python3
"""
Test the complete frontend-to-backend flow
"""
import requests
from PIL import Image
import io

def create_test_image():
    """Create a simple test image"""
    img = Image.new('RGB', (100, 100), color='blue')
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='JPEG')
    img_bytes.seek(0)
    return img_bytes

def test_complete_flow():
    """Test the complete upload and analysis flow as frontend would do it"""
    print("🧪 Testing Complete Frontend Flow...")
    print("=" * 50)
    
    base_url = "http://localhost:5000"
    
    try:
        # Step 1: Upload image (multipart/form-data)
        print("📤 Step 1: Upload image...")
        test_image = create_test_image()
        files = {'image': ('test_frontend.jpg', test_image, 'image/jpeg')}
        
        upload_response = requests.post(f"{base_url}/api/upload", files=files)
        
        if upload_response.status_code != 200:
            print(f"❌ Upload failed: {upload_response.status_code}")
            return False
            
        upload_data = upload_response.json()
        print(f"✅ Upload successful: {upload_data['filename']}")
        
        # Step 2: Analyze image (form data - as frontend now sends)
        print("🔍 Step 2: Analyze image...")
        form_data = {
            'filename': upload_data['filename'],
            'original_name': upload_data['original_name']
        }
        
        analysis_response = requests.post(f"{base_url}/api/analysis/analyze", data=form_data)
        
        if analysis_response.status_code != 200:
            print(f"❌ Analysis failed: {analysis_response.status_code}")
            print(f"   Response: {analysis_response.text}")
            return False
            
        analysis_data = analysis_response.json()
        print(f"✅ Analysis successful!")
        print(f"   Prediction: {analysis_data['prediction']}")
        print(f"   Confidence: {analysis_data['confidence_score']:.3f}")
        print(f"   Analysis ID: {analysis_data['analysis_id']}")
        
        # Step 3: Check if analysis appears in history
        print("📊 Step 3: Check history...")
        history_response = requests.get(f"{base_url}/api/history")
        
        if history_response.status_code == 200:
            history_data = history_response.json()
            print(f"✅ History accessible: {len(history_data['analyses'])} analyses")
        else:
            print(f"⚠️ History check failed: {history_response.status_code}")
        
        return True
        
    except Exception as e:
        print(f"❌ Flow test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_complete_flow()
    
    print("\n🎯 Frontend Flow Test Summary:")
    print("=" * 50)
    if success:
        print("✅ Complete frontend flow working!")
        print("🚀 Frontend should now work without 422 errors")
        print("   1. Upload: multipart/form-data ✅")
        print("   2. Analysis: form data ✅") 
        print("   3. History: JSON response ✅")
    else:
        print("❌ Frontend flow has issues")
        print("🔧 Check the error messages above")