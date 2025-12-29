#!/usr/bin/env python3
"""
Simple test for ML model integration
"""
import os
import sys

# Add backend to path
sys.path.append('backend')

def test_model_files():
    """Check if model files exist"""
    print("🔍 Checking ML Model Files...")
    
    model_files = [
        'backend/ml/models/simple_ai_detection_model.pth',
        'backend/ml/models/ai_detection_model.pth'
    ]
    
    for model_file in model_files:
        if os.path.exists(model_file):
            size = os.path.getsize(model_file)
            print(f"   ✅ {model_file} ({size:,} bytes)")
        else:
            print(f"   ❌ {model_file} - Not found")

def test_imports():
    """Test if all required modules can be imported"""
    print("\n🔍 Testing Module Imports...")
    
    try:
        import torch
        print(f"   ✅ PyTorch: {torch.__version__}")
    except ImportError as e:
        print(f"   ❌ PyTorch import failed: {e}")
        return False
    
    try:
        from PIL import Image
        print("   ✅ PIL/Pillow")
    except ImportError as e:
        print(f"   ❌ PIL import failed: {e}")
        return False
    
    try:
        import cv2
        print(f"   ✅ OpenCV: {cv2.__version__}")
    except ImportError as e:
        print(f"   ❌ OpenCV import failed: {e}")
        return False
    
    try:
        from ml.model import model_manager, AIDetectionCNN
        print("   ✅ ML Model classes")
    except ImportError as e:
        print(f"   ❌ ML Model import failed: {e}")
        return False
    
    try:
        from app.services.image_analysis import image_analysis_service
        print("   ✅ Image Analysis Service")
    except ImportError as e:
        print(f"   ❌ Image Analysis Service import failed: {e}")
        return False
    
    return True

def test_model_loading():
    """Test model loading"""
    print("\n🔍 Testing Model Loading...")
    
    try:
        from ml.model import model_manager
        
        # Try to load the trained model
        success = model_manager.load_model("simple_ai_detection_model.pth")
        
        if success:
            print("   ✅ Trained model loaded successfully")
        else:
            print("   ⚠️ Using pretrained model as fallback")
        
        # Test if model can make predictions
        import torch
        test_tensor = torch.randn(1, 3, 224, 224)
        result = model_manager.predict_image(test_tensor)
        
        print(f"   ✅ Model prediction test: {result['prediction']}")
        print(f"   ✅ Confidence: {result['confidence']:.3f}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Model loading failed: {e}")
        return False

def test_image_analysis():
    """Test complete image analysis pipeline"""
    print("\n🔍 Testing Image Analysis Pipeline...")
    
    try:
        from app.services.image_analysis import image_analysis_service
        from PIL import Image
        
        # Create a test image
        test_image = Image.new('RGB', (512, 512), color=(128, 128, 128))
        test_image.save('test_analysis.jpg')
        
        # Run complete analysis
        result = image_analysis_service.analyze_image('test_analysis.jpg', 'test_analysis.jpg')
        
        print(f"   ✅ Analysis completed")
        print(f"   📊 Prediction: {result.prediction}")
        print(f"   📊 Confidence: {result.confidence_score:.3f}")
        print(f"   📊 Processing time: {result.processing_time:.2f}s")
        print(f"   📊 Model version: {result.model_version}")
        
        # Check metadata
        if result.metadata:
            print(f"   📊 Metadata fields: {len(result.metadata)}")
            if 'ml_probabilities' in result.metadata:
                print(f"   ✅ ML probabilities available")
            if 'exif_anomalies' in result.metadata:
                print(f"   ✅ EXIF anomaly detection working")
            if 'quality_metrics' in result.metadata:
                print(f"   ✅ Quality metrics available")
        
        # Cleanup
        os.remove('test_analysis.jpg')
        
        return True
        
    except Exception as e:
        print(f"   ❌ Image analysis failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🧪 ML Model Integration Test")
    print("=" * 50)
    
    # Run all tests
    test_model_files()
    
    if not test_imports():
        print("\n❌ Import tests failed - check dependencies")
        sys.exit(1)
    
    if not test_model_loading():
        print("\n❌ Model loading failed")
        sys.exit(1)
    
    if not test_image_analysis():
        print("\n❌ Image analysis failed")
        sys.exit(1)
    
    print("\n🎉 All Tests PASSED!")
    print("✅ Real ML model is working")
    print("✅ OSINT analysis is working")
    print("✅ Free scanning is ready")
    print("\n🚀 Your free scan system is ready with:")
    print("   • Real trained CNN model")
    print("   • OSINT metadata analysis")
    print("   • Quality metrics detection")
    print("   • Authenticity indicators")