#!/usr/bin/env python3
"""
Test the analysis endpoint with form data
"""
import requests

def test_analysis_endpoint():
    """Test the analysis endpoint with form data"""
    print("🧪 Testing Analysis Endpoint...")
    print("=" * 50)
    
    base_url = "http://localhost:5000"
    
    # Test with form data (what frontend should send)
    form_data = {
        'filename': '87933548-d16c-48b3-82ae-688f78f64b98.jpg',  # From our previous test
        'original_name': 'test_image.jpg'
    }
    
    try:
        response = requests.post(f"{base_url}/api/analysis/analyze", data=form_data)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Analysis endpoint working!")
            print(f"   Prediction: {result['prediction']}")
            print(f"   Confidence: {result['confidence_score']:.3f}")
            print(f"   Analysis ID: {result['analysis_id']}")
        else:
            print(f"❌ Analysis failed: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Test failed: {e}")

if __name__ == "__main__":
    test_analysis_endpoint()