"""
CNN Model for AI-generated image detection using PyTorch
"""
import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision.transforms as transforms
from torchvision.models import resnet50, ResNet50_Weights
import logging
from typing import Dict, Any
import os

logger = logging.getLogger(__name__)

class AIDetectionCNN(nn.Module):
    """
    CNN model for detecting AI-generated images
    Based on ResNet50 with custom classification head
    """
    
    def __init__(self, num_classes: int = 3, pretrained: bool = True):
        super(AIDetectionCNN, self).__init__()
        
        # Load pretrained ResNet50
        if pretrained:
            self.backbone = resnet50(weights=ResNet50_Weights.IMAGENET1K_V2)
        else:
            self.backbone = resnet50(weights=None)
        
        # Freeze early layers for transfer learning
        for param in list(self.backbone.parameters())[:-20]:
            param.requires_grad = False
        
        # Replace final layer
        num_features = self.backbone.fc.in_features
        self.backbone.fc = nn.Identity()
        
        # Custom classification head
        self.classifier = nn.Sequential(
            nn.Dropout(0.5),
            nn.Linear(num_features, 512),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(512, 256),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(256, num_classes)
        )
        
        self.num_classes = num_classes
        self.class_names = ["authentic", "ai_generated", "manipulated"]
    
    def forward(self, x):
        features = self.backbone(x)
        output = self.classifier(features)
        return output
    
    def predict_proba(self, x):
        """Get prediction probabilities"""
        with torch.no_grad():
            logits = self.forward(x)
            probabilities = F.softmax(logits, dim=1)
        return probabilities
    
    def predict(self, x):
        """Get predictions with confidence scores"""
        probabilities = self.predict_proba(x)
        predicted_classes = torch.argmax(probabilities, dim=1)
        confidence_scores = torch.max(probabilities, dim=1)[0]
        
        results = []
        for i in range(len(predicted_classes)):
            results.append({
                'prediction': self.class_names[predicted_classes[i]],
                'confidence': confidence_scores[i].item(),
                'probabilities': {
                    name: prob.item() 
                    for name, prob in zip(self.class_names, probabilities[i])
                }
            })
        
        return results

class ImagePreprocessor:
    """Image preprocessing for the AI detection model"""
    
    def __init__(self, image_size: tuple = (224, 224)):
        self.image_size = image_size
        
        # Training transforms with augmentation
        self.train_transform = transforms.Compose([
            transforms.Resize((256, 256)),
            transforms.RandomCrop(image_size),
            transforms.RandomHorizontalFlip(p=0.5),
            transforms.RandomRotation(degrees=10),
            transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2, hue=0.1),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
        
        # Validation/inference transforms
        self.val_transform = transforms.Compose([
            transforms.Resize((256, 256)),
            transforms.CenterCrop(image_size),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
    
    def get_train_transform(self):
        return self.train_transform
    
    def get_val_transform(self):
        return self.val_transform

class ModelManager:
    """Manages model loading, saving, and inference"""
    
    def __init__(self, model_path: str = "ml/models"):
        self.model_path = model_path
        self.model = None
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.preprocessor = ImagePreprocessor()
        
        # Ensure model directory exists
        os.makedirs(model_path, exist_ok=True)
        
        logger.info(f"Using device: {self.device}")
    
    def load_model(self, model_file: str = "ai_detection_model.pth") -> bool:
        """Load trained model from file"""
        try:
            model_filepath = os.path.join(self.model_path, model_file)
            
            if not os.path.exists(model_filepath):
                logger.warning(f"Model file not found: {model_filepath}")
                # Load pretrained model as fallback
                self.model = AIDetectionCNN(pretrained=True)
                self.model.to(self.device)
                self.model.eval()
                return False
            
            # Load model state
            checkpoint = torch.load(model_filepath, map_location=self.device)
            
            # Initialize model
            self.model = AIDetectionCNN(
                num_classes=checkpoint.get('num_classes', 3),
                pretrained=False
            )
            
            # Load weights
            self.model.load_state_dict(checkpoint['model_state_dict'])
            self.model.to(self.device)
            self.model.eval()
            
            logger.info(f"Model loaded successfully from {model_filepath}")
            return True
            
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            # Fallback to pretrained model
            self.model = AIDetectionCNN(pretrained=True)
            self.model.to(self.device)
            self.model.eval()
            return False
    
    def save_model(self, model: nn.Module, optimizer, epoch: int, 
                   loss: float, accuracy: float, model_file: str = "ai_detection_model.pth"):
        """Save trained model to file"""
        try:
            model_filepath = os.path.join(self.model_path, model_file)
            
            checkpoint = {
                'epoch': epoch,
                'model_state_dict': model.state_dict(),
                'optimizer_state_dict': optimizer.state_dict(),
                'loss': loss,
                'accuracy': accuracy,
                'num_classes': model.num_classes,
                'class_names': model.class_names
            }
            
            torch.save(checkpoint, model_filepath)
            logger.info(f"Model saved to {model_filepath}")
            
        except Exception as e:
            logger.error(f"Error saving model: {e}")
    
    def predict_image(self, image_tensor: torch.Tensor) -> Dict[str, Any]:
        """Predict on a single image tensor"""
        if self.model is None:
            self.load_model()
        
        try:
            # Ensure model is in eval mode
            self.model.eval()
            
            # Add batch dimension if needed
            if len(image_tensor.shape) == 3:
                image_tensor = image_tensor.unsqueeze(0)
            
            # Move to device
            image_tensor = image_tensor.to(self.device)
            
            # Get prediction
            with torch.no_grad():
                results = self.model.predict(image_tensor)
            
            return results[0]  # Return first (and only) result
            
        except Exception as e:
            logger.error(f"Error during prediction: {e}")
            return {
                'prediction': 'error',
                'confidence': 0.0,
                'probabilities': {}
            }

# Global model manager instance
model_manager = ModelManager()