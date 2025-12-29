#!/usr/bin/env python3
"""
Quick performance test for optimized AI analysis
"""
import sys
import os
import time
from PIL import Image

# Add backend to path
sys.path.append('backend')

def test_optimized_analysis():
    """Test the optimized analysis performance"""
    print("⚡ Testing Optimized AI Analysis Performance")
    print("=" * 50)
    
    try:
        from app.services.image_analysis import image_analysis_service
        
        # Create a test image
        test_image = Image.new('RGB', (512, 512), color=(100, 150, 200))
        test_image.save('perf_test.jpg', quality=85)
        
        print("🧪 Running performance test...")
        
        # Test multiple runs for average
        times = []
        for i in range(3):
            start_time = time.time()
            result = image_analysis_service.analyze_image('perf_test.jpg', 'perf_test.jpg')
            end_time = time.time()
            
            processing_time = end_time - start_time
            times.append(processing_time)
            
            print(f"   Run {i+1}: {processing_time:.3f}s - {result.prediction} ({result.confidence_score:.3f})")
        
        avg_time = sum(times) / len(times)
        min_time = min(times)
        max_time = max(times)
        
        print(f"\n📊 Performance Results:")
        print(f"   Average: {avg_time:.3f}s")
        print(f"   Fastest: {min_time:.3f}s")
        print(f"   Slowest: {max_time:.3f}s")
        
        # Performance rating
        if avg_time < 1.0:
            print(f"   🟢 EXCELLENT - Very fast analysis!")
        elif avg_time < 2.0:
            print(f"   🟡 GOOD - Fast enough for real-time use")
        elif avg_time < 5.0:
            print(f"   🟠 ACCEPTABLE - Reasonable performance")
        else:
            print(f"   🔴 SLOW - May need further optimization")
        
        # Cleanup
        os.remove('perf_test.jpg')
        
        return avg_time < 5.0  # Consider success if under 5 seconds
        
    except Exception as e:
        print(f"❌ Performance test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_optimized_analysis()
    
    if success:
        print("\n✅ Performance optimizations working!")
        print("🚀 AI analysis should now be much faster")
    else:
        print("\n❌ Performance test failed")
        print("🔧 May need additional optimization")