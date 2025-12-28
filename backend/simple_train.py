#!/usr/bin/env python3
"""
Simplified training script for AI detection model
"""
import os
import sys
import logging
import random
import shutil
from datetime import datetime
from typing import Dict, Tuple
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
from torchvision import transforms
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Simple CNN Model
class SimpleAIDetectionCNN(nn.Module):
    """Simplified CNN for AI detection"""
    
    def __init__(self, num_classes=3):
        super(SimpleAIDetectionCNN, self).__init__()
        
        self.features = nn.Sequential(
            # First conv block
            nn.Conv2d(3, 32, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),
            
            # Second conv block
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),
            
            # Third conv block
            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),
            
            # Fourth conv block
            nn.Conv2d(128, 256, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),
        )
        
        self.classifier = nn.Sequential(
            nn.Dropout(0.5),
            nn.Linear(256 * 14 * 14, 512),
            nn.ReLU(inplace=True),
            nn.Dropout(0.3),
            nn.Linear(512, 128),
            nn.ReLU(inplace=True),
            nn.Linear(128, num_classes)
        )
        
        self.num_classes = num_classes
        self.class_names = ["authentic", "ai_generated", "manipulated"]
    
    def forward(self, x):
        x = self.features(x)
        x = x.view(x.size(0), -1)
        x = self.classifier(x)
        return x

# Dataset class
class SimpleImageDataset(Dataset):
    """Simple dataset for loading images"""
    
    def __init__(self, dataset_path: str, transform=None):
        self.dataset_path = dataset_path
        self.transform = transform
        self.samples = []
        self.class_to_idx = {}
        
        self._load_samples()
    
    def _load_samples(self):
        """Load all image samples"""
        classes = sorted([d for d in os.listdir(self.dataset_path) 
                         if os.path.isdir(os.path.join(self.dataset_path, d))])
        
        self.class_to_idx = {cls: idx for idx, cls in enumerate(classes)}
        
        for class_name in classes:
            class_path = os.path.join(self.dataset_path, class_name)
            for img_name in os.listdir(class_path):
                img_path = os.path.join(class_path, img_name)
                if os.path.isfile(img_path) and img_name.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp')):
                    self.samples.append((img_path, self.class_to_idx[class_name]))
        
        logger.info(f"Loaded {len(self.samples)} samples from {len(classes)} classes")
    
    def __len__(self):
        return len(self.samples)
    
    def __getitem__(self, idx):
        img_path, label = self.samples[idx]
        
        try:
            image = Image.open(img_path).convert('RGB')
            if self.transform:
                image = self.transform(image)
            return image, label
        except Exception as e:
            logger.error(f"Error loading image {img_path}: {e}")
            # Return a black image as fallback
            if self.transform:
                return self.transform(Image.new('RGB', (224, 224), (0, 0, 0))), label
            return Image.new('RGB', (224, 224), (0, 0, 0)), label

def split_dataset(dataset_path: str, train_ratio: float = 0.7, val_ratio: float = 0.2):
    """Split dataset into train/val/test sets"""
    
    # Create split directories
    split_dirs = ['train', 'val', 'test']
    for split_dir in split_dirs:
        os.makedirs(os.path.join(dataset_path, split_dir), exist_ok=True)
    
    # Get all categories
    categories = [d for d in os.listdir(dataset_path) 
                 if os.path.isdir(os.path.join(dataset_path, d)) and d not in split_dirs]
    
    for category in categories:
        category_path = os.path.join(dataset_path, category)
        images = [f for f in os.listdir(category_path) 
                 if f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp'))]
        
        # Shuffle images
        random.shuffle(images)
        
        # Calculate split sizes
        total = len(images)
        train_size = int(total * train_ratio)
        val_size = int(total * val_ratio)
        
        # Split images
        train_images = images[:train_size]
        val_images = images[train_size:train_size + val_size]
        test_images = images[train_size + val_size:]
        
        # Create category directories in splits
        for split_dir in split_dirs:
            os.makedirs(os.path.join(dataset_path, split_dir, category), exist_ok=True)
        
        # Copy images to respective splits
        for img in train_images:
            shutil.copy2(
                os.path.join(category_path, img),
                os.path.join(dataset_path, 'train', category, img)
            )
        
        for img in val_images:
            shutil.copy2(
                os.path.join(category_path, img),
                os.path.join(dataset_path, 'val', category, img)
            )
        
        for img in test_images:
            shutil.copy2(
                os.path.join(category_path, img),
                os.path.join(dataset_path, 'test', category, img)
            )
        
        logger.info(f"Split {category}: {len(train_images)} train, {len(val_images)} val, {len(test_images)} test")

def train_model():
    """Main training function"""
    
    print("🚀 Starting AI Detection Model Training...")
    print("=" * 50)
    
    # Configuration
    dataset_path = 'datasets/sample_dataset'
    batch_size = 8
    num_epochs = 10
    learning_rate = 0.001
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    print(f"Using device: {device}")
    
    # Data transforms
    train_transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.RandomHorizontalFlip(p=0.5),
        transforms.RandomRotation(degrees=10),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    
    val_transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    
    # Split dataset
    print("✂️ Splitting dataset...")
    split_dataset(dataset_path)
    
    # Create datasets
    train_dataset = SimpleImageDataset(
        os.path.join(dataset_path, 'train'),
        transform=train_transform
    )
    
    val_dataset = SimpleImageDataset(
        os.path.join(dataset_path, 'val'),
        transform=val_transform
    )
    
    test_dataset = SimpleImageDataset(
        os.path.join(dataset_path, 'test'),
        transform=val_transform
    )
    
    # Create data loaders
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)
    
    # Initialize model
    num_classes = len(train_dataset.class_to_idx)
    model = SimpleAIDetectionCNN(num_classes=num_classes)
    model.to(device)
    
    # Loss and optimizer
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)
    
    # Training loop
    best_val_accuracy = 0.0
    train_losses = []
    val_accuracies = []
    
    print("🏋️ Training model...")
    
    for epoch in range(num_epochs):
        # Training phase
        model.train()
        total_loss = 0.0
        
        for batch_idx, (data, target) in enumerate(train_loader):
            data, target = data.to(device), target.to(device)
            
            optimizer.zero_grad()
            output = model(data)
            loss = criterion(output, target)
            loss.backward()
            optimizer.step()
            
            total_loss += loss.item()
        
        avg_train_loss = total_loss / len(train_loader)
        train_losses.append(avg_train_loss)
        
        # Validation phase
        model.eval()
        val_predictions = []
        val_targets = []
        
        with torch.no_grad():
            for data, target in val_loader:
                data, target = data.to(device), target.to(device)
                output = model(data)
                pred = output.argmax(dim=1)
                val_predictions.extend(pred.cpu().numpy())
                val_targets.extend(target.cpu().numpy())
        
        val_accuracy = accuracy_score(val_targets, val_predictions)
        val_accuracies.append(val_accuracy)
        
        print(f"Epoch {epoch+1}/{num_epochs}: Train Loss: {avg_train_loss:.4f}, Val Acc: {val_accuracy:.4f}")
        
        # Save best model
        if val_accuracy > best_val_accuracy:
            best_val_accuracy = val_accuracy
            torch.save({
                'epoch': epoch,
                'model_state_dict': model.state_dict(),
                'optimizer_state_dict': optimizer.state_dict(),
                'val_accuracy': val_accuracy,
                'class_names': model.class_names
            }, 'ml/models/simple_ai_detection_model.pth')
    
    # Test evaluation
    model.eval()
    test_predictions = []
    test_targets = []
    
    with torch.no_grad():
        for data, target in test_loader:
            data, target = data.to(device), target.to(device)
            output = model(data)
            pred = output.argmax(dim=1)
            test_predictions.extend(pred.cpu().numpy())
            test_targets.extend(target.cpu().numpy())
    
    test_accuracy = accuracy_score(test_targets, test_predictions)
    precision, recall, f1, _ = precision_recall_fscore_support(
        test_targets, test_predictions, average='weighted'
    )
    
    # Plot training history
    plt.figure(figsize=(12, 4))
    
    plt.subplot(1, 2, 1)
    plt.plot(train_losses, label='Train Loss')
    plt.title('Training Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()
    
    plt.subplot(1, 2, 2)
    plt.plot(val_accuracies, label='Val Accuracy')
    plt.title('Validation Accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.legend()
    
    plt.tight_layout()
    plt.savefig('ml/training_history.png')
    plt.close()
    
    # Results
    print("\n🎉 Training completed!")
    print("=" * 50)
    print("📊 Final Results:")
    print(f"  Best Validation Accuracy: {best_val_accuracy:.4f}")
    print(f"  Test Accuracy: {test_accuracy:.4f}")
    print(f"  Precision: {precision:.4f}")
    print(f"  Recall: {recall:.4f}")
    print(f"  F1 Score: {f1:.4f}")
    print(f"\n📁 Model saved to: ml/models/simple_ai_detection_model.pth")
    print(f"📈 Training plot saved to: ml/training_history.png")
    
    return {
        'best_val_accuracy': best_val_accuracy,
        'test_accuracy': test_accuracy,
        'precision': precision,
        'recall': recall,
        'f1_score': f1
    }

if __name__ == "__main__":
    try:
        results = train_model()
        print("\n✅ AI model training completed successfully!")
    except Exception as e:
        print(f"\n❌ Training failed: {e}")
        import traceback
        traceback.print_exc()