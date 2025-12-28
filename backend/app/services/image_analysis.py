"""
Image analysis service for AI detection and metadata extraction
"""
import os
import logging
import hashlib
import time
from typing import Dict, Any, Optional
from PIL import Image, ExifTags
from PIL.ExifTags import TAGS
import torch
import cv2
import numpy as np

from app.core.config import settings
from ml.model import model_manager, ImagePreprocessor
from app.models.analysis import ImageAnalysisResult

logger = logging.getLogger(__name__)

class ImageAnalysisService:
    def __init__(self):
        self.preprocessor = ImagePreprocessor()
        # Load model on initialization
        model_manager.load_model()
    
    def get_file_hash(self, file_path: str) -> str:
        """Generate SHA256 hash of file"""
        hash_sha256 = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha256.update(chunk)
        return hash_sha256.hexdigest()
    
    def extract_exif_data(self, image_path: str) -> Dict[str, Any]:
        """Extract EXIF metadata from image"""
        exif_data = {}
        
        try:
            with Image.open(image_path) as image:
                # Get EXIF data
                exif = image.getexif()
                
                if exif is not None:
                    for tag_id, value in exif.items():
                        tag = TAGS.get(tag_id, tag_id)
                        
                        # Convert bytes to string if needed
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
            logger.error(f"Error extracting EXIF data: {e}")
        
        return exif_data
    
    def detect_metadata_anomalies(self, exif_data: Dict[str, Any]) -> Dict[str, Any]:
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
        suspicious_software = ['photoshop', 'gimp', 'midjourney', 'dalle', 'stable diffusion']
        if any(sus in software for sus in suspicious_software):
            anomalies['suspicious_software'] = True
        
        # Check for missing timestamp
        timestamp_tags = ['DateTime', 'DateTimeOriginal', 'DateTimeDigitized']
        if not any(tag in exif_data for tag in timestamp_tags):
            anomalies['missing_timestamp'] = True
        
        # Check for unusual dimensions (common AI generation sizes)
        size = exif_data.get('size', (0, 0))
        ai_common_sizes = [(512, 512), (1024, 1024), (768, 768), (256, 256)]
        if size in ai_common_sizes:
            anomalies['unusual_dimensions'] = True
        
        return anomalies
    
    def analyze_image_quality(self, image_path: str) -> Dict[str, float]:
        """Analyze image quality metrics that might indicate AI generation"""
        try:
            # Load image with OpenCV
            img = cv2.imread(image_path)
            if img is None:
                return {}
            
            # Convert to grayscale
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            # Calculate various quality metrics
            metrics = {}
            
            # Laplacian variance (sharpness)
            metrics['sharpness'] = cv2.Laplacian(gray, cv2.CV_64F).var()
            
            # Noise estimation using standard deviation
            metrics['noise_level'] = np.std(gray)
            
            # Contrast (standard deviation of pixel intensities)
            metrics['contrast'] = np.std(gray) / np.mean(gray) if np.mean(gray) > 0 else 0
            
            # Brightness
            metrics['brightness'] = np.mean(gray) / 255.0
            
            # Edge density
            edges = cv2.Canny(gray, 50, 150)
            metrics['edge_density'] = np.sum(edges > 0) / edges.size
            
            return metrics
            
        except Exception as e:
            logger.error(f"Error analyzing image quality: {e}")
            return {}
    
    def preprocess_image_for_model(self, image_path: str) -> torch.Tensor:
        """Preprocess image for model inference"""
        try:
            image = Image.open(image_path).convert('RGB')
            transform = self.preprocessor.get_val_transform()
            tensor = transform(image)
            return tensor
        except Exception as e:
            logger.error(f"Error preprocessing image: {e}")
            raise
    
    def analyze_image(self, image_path: str, filename: str) -> ImageAnalysisResult:
        """Complete image analysis pipeline"""
        start_time = time.time()
        
        try:
            # Extract EXIF data
            exif_data = self.extract_exif_data(image_path)
            
            # Detect metadata anomalies
            metadata_anomalies = self.detect_metadata_anomalies(exif_data)
            
            # Analyze image quality
            quality_metrics = self.analyze_image_quality(image_path)
            
            # Preprocess image for model
            image_tensor = self.preprocess_image_for_model(image_path)
            
            # Get AI detection prediction
            prediction_result = model_manager.predict_image(image_tensor)
            
            # Calculate processing time
            processing_time = time.time() - start_time
            
            # Combine metadata analysis with ML prediction
            metadata_score = self._calculate_metadata_suspicion_score(metadata_anomalies, quality_metrics)
            
            # Adjust confidence based on metadata
            adjusted_confidence = self._adjust_confidence_with_metadata(
                prediction_result['confidence'], 
                metadata_score
            )
            
            # Create result
            result = ImageAnalysisResult(
                prediction=prediction_result['prediction'],
                confidence_score=adjusted_confidence,
                model_version="1.0.0",
                processing_time=processing_time,
                metadata={
                    'exif_anomalies': metadata_anomalies,
                    'quality_metrics': quality_metrics,
                    'metadata_suspicion_score': metadata_score,
                    'ml_probabilities': prediction_result.get('probabilities', {}),
                    'original_confidence': prediction_result['confidence']
                }
            )
            
            logger.info(f"Image analysis completed: {filename} -> {result.prediction} ({result.confidence_score:.3f})")
            return result
            
        except Exception as e:
            logger.error(f"Error analyzing image {filename}: {e}")
            # Return error result
            return ImageAnalysisResult(
                prediction="error",
                confidence_score=0.0,
                model_version="1.0.0",
                processing_time=time.time() - start_time,
                metadata={'error': str(e)}
            )
    
    def _calculate_metadata_suspicion_score(self, anomalies: Dict[str, bool], 
                                          quality_metrics: Dict[str, float]) -> float:
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
            if sharpness > 1000:  # Threshold for unusually sharp images
                score += 0.1
            
            # Very low noise might indicate AI generation
            noise = quality_metrics.get('noise_level', 50)
            if noise < 10:  # Threshold for unusually clean images
                score += 0.1
        
        return min(score, 1.0)  # Cap at 1.0
    
    def _adjust_confidence_with_metadata(self, ml_confidence: float, 
                                       metadata_score: float) -> float:
        """Adjust ML confidence based on metadata analysis"""
        # Simple weighted combination
        metadata_weight = 0.2
        ml_weight = 0.8
        
        # If metadata suggests suspicion, adjust accordingly
        if metadata_score > 0.5:
            # High metadata suspicion - boost AI/manipulated predictions
            adjusted = ml_confidence * ml_weight + metadata_score * metadata_weight
        else:
            # Low metadata suspicion - maintain ML confidence
            adjusted = ml_confidence
        
        return min(adjusted, 1.0)

# Global service instance
image_analysis_service = ImageAnalysisService()