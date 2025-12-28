#!/usr/bin/env python3
"""
Analyze the uploaded image for AI detection
"""
import torch
import torch.nn.functional as F
from torchvision import transforms
from PIL import Image, ExifTags
import os
import numpy as np
import cv2
from simple_train import SimpleAIDetectionCNN

def extract_exif_data(image_path):
    """Extract EXIF metadata from image"""
    exif_data = {}
    
    try:
        with Image.open(image_path) as image:
            exif = image.getexif()
            
            if exif is not None:
                for tag_id, value in exif.items():
                    tag = ExifTags.TAGS.get(tag_id, tag_id)
                    
                    if isinstance(value, bytes):
                        try:
                            value = value.decode('utf-8')
                        except UnicodeDecodeError:
                            value = str(value)
                    
                    exif_data[tag] = value
            
            # Additional image info
            exif_data.update({
                'format': image.format,
                'mode': image.mode,
                'size': image.size,
                'has_transparency': image.mode in ('RGBA', 'LA') or 'transparency' in image.info
            })
            
    except Exception as e:
        print(f"Error extracting EXIF data: {e}")
    
    return exif_data

def analyze_image_quality(image_path):
    """Analyze image quality metrics"""
    try:
        img = cv2.imread(image_path)
        if img is None:
            return {}
        
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        metrics = {}
        
        # Laplacian variance (sharpness)
        metrics['sharpness'] = cv2.Laplacian(gray, cv2.CV_64F).var()
        
        # Noise estimation
        metrics['noise_level'] = np.std(gray)
        
        # Contrast
        metrics['contrast'] = np.std(gray) / np.mean(gray) if np.mean(gray) > 0 else 0
        
        # Brightness
        metrics['brightness'] = np.mean(gray) / 255.0
        
        # Edge density
        edges = cv2.Canny(gray, 50, 150)
        metrics['edge_density'] = np.sum(edges > 0) / edges.size
        
        return metrics
        
    except Exception as e:
        print(f"Error analyzing image quality: {e}")
        return {}

def detect_metadata_anomalies(exif_data):
    """Detect suspicious metadata patterns"""
    anomalies = {
        'missing_camera_info': False,
        'suspicious_software': False,
        'missing_timestamp': False,
        'unusual_dimensions': False,
        'missing_exif': False
    }
    
    # Check for missing EXIF data
    if not exif_data or len(exif_data) < 5:
        anomalies['missing_exif'] = True
    
    # Check for missing camera information
    camera_tags = ['Make', 'Model', 'LensModel']
    if not any(tag in exif_data for tag in camera_tags):
        anomalies['missing_camera_info'] = True
    
    # Check for suspicious software signatures
    software = exif_data.get('Software', '').lower()
    suspicious_software = ['photoshop', 'gimp', 'midjourney', 'dalle', 'stable diffusion', 'ai', 'generated']
    if any(sus in software for sus in suspicious_software):
        anomalies['suspicious_software'] = True
    
    # Check for missing timestamp
    timestamp_tags = ['DateTime', 'DateTimeOriginal', 'DateTimeDigitized']
    if not any(tag in exif_data for tag in timestamp_tags):
        anomalies['missing_timestamp'] = True
    
    # Check for unusual dimensions (common AI generation sizes)
    size = exif_data.get('size', (0, 0))
    ai_common_sizes = [(512, 512), (1024, 1024), (768, 768), (256, 256), (640, 640)]
    if size in ai_common_sizes:
        anomalies['unusual_dimensions'] = True
    
    return anomalies

def calculate_metadata_suspicion_score(anomalies, quality_metrics):
    """Calculate suspicion score based on metadata analysis"""
    score = 0.0
    
    # Anomaly weights
    anomaly_weights = {
        'missing_exif': 0.3,
        'missing_camera_info': 0.2,
        'suspicious_software': 0.4,
        'missing_timestamp': 0.1,
        'unusual_dimensions': 0.2
    }
    
    # Add anomaly scores
    for anomaly, present in anomalies.items():
        if present:
            score += anomaly_weights.get(anomaly, 0.1)
    
    # Quality metric analysis
    if quality_metrics:
        # Very high sharpness might indicate AI generation
        sharpness = quality_metrics.get('sharpness', 0)
        if sharpness > 1000:
            score += 0.1
        
        # Very low noise might indicate AI generation
        noise = quality_metrics.get('noise_level', 50)
        if noise < 10:
            score += 0.1
    
    return min(score, 1.0)

def load_trained_model():
    """Load the trained model"""
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    try:
        # Load checkpoint
        checkpoint = torch.load('ml/models/simple_ai_detection_model.pth', map_location=device)
        
        # Initialize model
        model = SimpleAIDetectionCNN(num_classes=3)
        model.load_state_dict(checkpoint['model_state_dict'])
        model.to(device)
        model.eval()
        
        class_names = checkpoint.get('class_names', ['authentic', 'ai_generated', 'manipulated'])
        
        return model, class_names, device
    except Exception as e:
        print(f"Error loading model: {e}")
        return None, None, None

def analyze_uploaded_image(image_path):
    """Complete analysis of the uploaded image"""
    
    print("🔍 AI AUTHENTICITY ANALYSIS")
    print("=" * 50)
    
    # Load model
    model, class_names, device = load_trained_model()
    if model is None:
        print("❌ Could not load trained model")
        return
    
    print(f"✅ Model loaded successfully")
    print(f"📊 Classes: {class_names}")
    
    # Extract EXIF data
    print("\n📋 EXIF METADATA ANALYSIS")
    print("-" * 30)
    exif_data = extract_exif_data(image_path)
    
    if exif_data:
        print(f"📐 Image size: {exif_data.get('size', 'Unknown')}")
        print(f"📷 Format: {exif_data.get('format', 'Unknown')}")
        print(f"🎨 Mode: {exif_data.get('mode', 'Unknown')}")
        
        if 'Make' in exif_data:
            print(f"📱 Camera make: {exif_data['Make']}")
        if 'Model' in exif_data:
            print(f"📷 Camera model: {exif_data['Model']}")
        if 'Software' in exif_data:
            print(f"💻 Software: {exif_data['Software']}")
        if 'DateTime' in exif_data:
            print(f"📅 Date taken: {exif_data['DateTime']}")
    else:
        print("⚠️ No EXIF data found")
    
    # Analyze metadata anomalies
    print("\n🚨 METADATA ANOMALY DETECTION")
    print("-" * 30)
    anomalies = detect_metadata_anomalies(exif_data)
    
    for anomaly, present in anomalies.items():
        status = "🔴" if present else "🟢"
        print(f"{status} {anomaly.replace('_', ' ').title()}: {'Yes' if present else 'No'}")
    
    # Analyze image quality
    print("\n📊 TECHNICAL QUALITY ANALYSIS")
    print("-" * 30)
    quality_metrics = analyze_image_quality(image_path)
    
    if quality_metrics:
        print(f"🔍 Sharpness: {quality_metrics.get('sharpness', 0):.2f}")
        print(f"📡 Noise level: {quality_metrics.get('noise_level', 0):.2f}")
        print(f"🌈 Contrast: {quality_metrics.get('contrast', 0):.3f}")
        print(f"💡 Brightness: {quality_metrics.get('brightness', 0):.3f}")
        print(f"📏 Edge density: {quality_metrics.get('edge_density', 0):.3f}")
    
    # Calculate metadata suspicion score
    metadata_score = calculate_metadata_suspicion_score(anomalies, quality_metrics)
    print(f"\n🎯 Metadata Suspicion Score: {metadata_score:.3f}")
    
    # ML Model Prediction
    print("\n🤖 AI MODEL PREDICTION")
    print("-" * 30)
    
    # Image preprocessing
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    
    try:
        # Load and preprocess image
        image = Image.open(image_path).convert('RGB')
        image_tensor = transform(image).unsqueeze(0).to(device)
        
        # Make prediction
        with torch.no_grad():
            outputs = model(image_tensor)
            probabilities = F.softmax(outputs, dim=1)
            predicted_class = torch.argmax(probabilities, dim=1).item()
            confidence = probabilities[0][predicted_class].item()
        
        # Get all probabilities
        all_probs = {
            class_names[i]: probabilities[0][i].item() 
            for i in range(len(class_names))
        }
        
        print(f"🎯 Prediction: {class_names[predicted_class].upper()}")
        print(f"📊 Confidence: {confidence:.3f}")
        print("\n📈 All Probabilities:")
        for class_name, prob in all_probs.items():
            bar = "█" * int(prob * 20)
            print(f"  {class_name:12}: {prob:.3f} {bar}")
        
        # Combined analysis
        print("\n🔬 COMBINED ANALYSIS")
        print("-" * 30)
        
        # Adjust confidence based on metadata
        if metadata_score > 0.5:
            adjusted_confidence = min(confidence * 1.2, 1.0)
            print(f"⚠️ High metadata suspicion detected")
        else:
            adjusted_confidence = confidence
        
        print(f"🎯 Final Assessment: {class_names[predicted_class].upper()}")
        print(f"📊 Adjusted Confidence: {adjusted_confidence:.3f}")
        
        # Interpretation
        print("\n💡 INTERPRETATION")
        print("-" * 30)
        
        if class_names[predicted_class] == 'authentic':
            if confidence > 0.8:
                print("✅ HIGH CONFIDENCE: This appears to be an authentic photograph")
            elif confidence > 0.6:
                print("🟡 MEDIUM CONFIDENCE: Likely authentic, but some uncertainty")
            else:
                print("🟠 LOW CONFIDENCE: Uncertain classification")
        
        elif class_names[predicted_class] == 'ai_generated':
            if confidence > 0.8:
                print("🤖 HIGH CONFIDENCE: This appears to be AI-generated")
            elif confidence > 0.6:
                print("🟡 MEDIUM CONFIDENCE: Likely AI-generated")
            else:
                print("🟠 LOW CONFIDENCE: Uncertain classification")
        
        else:  # manipulated
            if confidence > 0.8:
                print("✂️ HIGH CONFIDENCE: This appears to be manipulated/edited")
            elif confidence > 0.6:
                print("🟡 MEDIUM CONFIDENCE: Likely manipulated")
            else:
                print("🟠 LOW CONFIDENCE: Uncertain classification")
        
        # Additional insights
        print("\n🔍 ADDITIONAL INSIGHTS")
        print("-" * 30)
        
        if anomalies['missing_camera_info']:
            print("📷 No camera information found - common in AI-generated images")
        
        if anomalies['unusual_dimensions']:
            print("📐 Unusual dimensions detected - typical of AI generation")
        
        if quality_metrics.get('sharpness', 0) > 1000:
            print("🔍 Very high sharpness - may indicate AI generation")
        
        if quality_metrics.get('noise_level', 50) < 10:
            print("📡 Very low noise - may indicate AI generation")
        
        return {
            'prediction': class_names[predicted_class],
            'confidence': confidence,
            'adjusted_confidence': adjusted_confidence,
            'metadata_score': metadata_score,
            'anomalies': anomalies,
            'quality_metrics': quality_metrics,
            'probabilities': all_probs
        }
        
    except Exception as e:
        print(f"❌ Error during prediction: {e}")
        return None

if __name__ == "__main__":
    # Save the uploaded image temporarily
    image_path = "uploaded_image.jpg"
    
    # Note: In a real scenario, the image would be saved from the upload
    # For now, we'll assume the image is available
    
    if os.path.exists(image_path):
        result = analyze_uploaded_image(image_path)
    else:
        print("❌ Image file not found. Please save the uploaded image as 'uploaded_image.jpg'")