"""
Training script for AI detection model
Supports training from extracted archive datasets
"""
import os
import logging
import argparse
from datetime import datetime
from typing import Dict, Tuple
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
from torchvision import datasets
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image
import numpy as np

from ml.model import AIDetectionCNN, ImagePreprocessor, ModelManager
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Simple config for training
class SimpleConfig:
    BATCH_SIZE = 32
    DATASET_PATH = "datasets"
    ALLOWED_IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']

settings = SimpleConfig()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CustomImageDataset(Dataset):
    """Custom dataset for loading images from extracted archives"""
    
    def __init__(self, dataset_path: str, transform=None):
        self.dataset_path = dataset_path
        self.transform = transform
        self.samples = []
        self.class_to_idx = {}
        
        self._load_samples()
    
    def _load_samples(self):
        """Load all image samples and create class mapping"""
        classes = sorted([d for d in os.listdir(self.dataset_path) 
                         if os.path.isdir(os.path.join(self.dataset_path, d))])
        
        self.class_to_idx = {cls: idx for idx, cls in enumerate(classes)}
        
        for class_name in classes:
            class_path = os.path.join(self.dataset_path, class_name)
            for img_name in os.listdir(class_path):
                img_path = os.path.join(class_path, img_name)
                if os.path.isfile(img_path):
                    self.samples.append((img_path, self.class_to_idx[class_name]))
        
        logger.info(f"Loaded {len(self.samples)} samples from {len(classes)} classes")
        logger.info(f"Classes: {list(self.class_to_idx.keys())}")
    
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

class Trainer:
    """Training manager for AI detection model"""
    
    def __init__(self, dataset_path: str, model_save_path: str = "ml/models"):
        self.dataset_path = dataset_path
        self.model_save_path = model_save_path
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.preprocessor = ImagePreprocessor()
        
        # Training parameters
        self.batch_size = settings.BATCH_SIZE
        self.learning_rate = 0.001
        self.num_epochs = 50
        self.patience = 10  # Early stopping patience
        
        logger.info(f"Training on device: {self.device}")
    
    def prepare_datasets(self) -> Tuple[DataLoader, DataLoader, DataLoader]:
        """Prepare train, validation, and test datasets"""
        
        # Create datasets
        train_dataset = CustomImageDataset(
            os.path.join(self.dataset_path, 'train'),
            transform=self.preprocessor.get_train_transform()
        )
        
        val_dataset = CustomImageDataset(
            os.path.join(self.dataset_path, 'val'),
            transform=self.preprocessor.get_val_transform()
        )
        
        test_dataset = CustomImageDataset(
            os.path.join(self.dataset_path, 'test'),
            transform=self.preprocessor.get_val_transform()
        )
        
        # Create data loaders
        train_loader = DataLoader(
            train_dataset, 
            batch_size=self.batch_size, 
            shuffle=True, 
            num_workers=4
        )
        
        val_loader = DataLoader(
            val_dataset, 
            batch_size=self.batch_size, 
            shuffle=False, 
            num_workers=4
        )
        
        test_loader = DataLoader(
            test_dataset, 
            batch_size=self.batch_size, 
            shuffle=False, 
            num_workers=4
        )
        
        return train_loader, val_loader, test_loader
    
    def train_epoch(self, model: nn.Module, train_loader: DataLoader, 
                   optimizer: optim.Optimizer, criterion: nn.Module) -> float:
        """Train for one epoch"""
        model.train()
        total_loss = 0.0
        
        for batch_idx, (data, target) in enumerate(train_loader):
            data, target = data.to(self.device), target.to(self.device)
            
            optimizer.zero_grad()
            output = model(data)
            loss = criterion(output, target)
            loss.backward()
            optimizer.step()
            
            total_loss += loss.item()
            
            if batch_idx % 100 == 0:
                logger.info(f'Batch {batch_idx}/{len(train_loader)}, Loss: {loss.item():.6f}')
        
        return total_loss / len(train_loader)
    
    def validate(self, model: nn.Module, val_loader: DataLoader, 
                criterion: nn.Module) -> Tuple[float, float]:
        """Validate the model"""
        model.eval()
        total_loss = 0.0
        all_predictions = []
        all_targets = []
        
        with torch.no_grad():
            for data, target in val_loader:
                data, target = data.to(self.device), target.to(self.device)
                output = model(data)
                loss = criterion(output, target)
                total_loss += loss.item()
                
                pred = output.argmax(dim=1)
                all_predictions.extend(pred.cpu().numpy())
                all_targets.extend(target.cpu().numpy())
        
        avg_loss = total_loss / len(val_loader)
        accuracy = accuracy_score(all_targets, all_predictions)
        
        return avg_loss, accuracy
    
    def train_model(self, dataset_name: str) -> Dict[str, float]:
        """Main training loop"""
        logger.info(f"Starting training for dataset: {dataset_name}")
        
        # Prepare datasets
        train_loader, val_loader, test_loader = self.prepare_datasets()
        
        # Initialize model
        num_classes = len(train_loader.dataset.class_to_idx)
        model = AIDetectionCNN(num_classes=num_classes, pretrained=True)
        model.to(self.device)
        
        # Loss and optimizer
        criterion = nn.CrossEntropyLoss()
        optimizer = optim.Adam(model.parameters(), lr=self.learning_rate, weight_decay=1e-4)
        scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, 'min', patience=5)
        
        # Training tracking
        best_val_accuracy = 0.0
        patience_counter = 0
        train_losses = []
        val_losses = []
        val_accuracies = []
        
        for epoch in range(self.num_epochs):
            logger.info(f"Epoch {epoch+1}/{self.num_epochs}")
            
            # Train
            train_loss = self.train_epoch(model, train_loader, optimizer, criterion)
            
            # Validate
            val_loss, val_accuracy = self.validate(model, val_loader, criterion)
            
            # Update scheduler
            scheduler.step(val_loss)
            
            # Track metrics
            train_losses.append(train_loss)
            val_losses.append(val_loss)
            val_accuracies.append(val_accuracy)
            
            logger.info(f"Train Loss: {train_loss:.4f}, Val Loss: {val_loss:.4f}, Val Acc: {val_accuracy:.4f}")
            
            # Save best model
            if val_accuracy > best_val_accuracy:
                best_val_accuracy = val_accuracy
                patience_counter = 0
                
                # Save model
                model_manager = ModelManager(self.model_save_path)
                model_manager.save_model(
                    model, optimizer, epoch, val_loss, val_accuracy,
                    f"ai_detection_model_{dataset_name}.pth"
                )
                logger.info(f"New best model saved with accuracy: {val_accuracy:.4f}")
            else:
                patience_counter += 1
            
            # Early stopping
            if patience_counter >= self.patience:
                logger.info(f"Early stopping at epoch {epoch+1}")
                break
        
        # Final evaluation on test set
        test_loss, test_accuracy = self.validate(model, test_loader, criterion)
        logger.info(f"Final Test Accuracy: {test_accuracy:.4f}")
        
        # Generate training plots
        self._plot_training_history(train_losses, val_losses, val_accuracies, dataset_name)
        
        # Generate evaluation report
        evaluation_report = self._evaluate_model(model, test_loader)
        
        return {
            'best_val_accuracy': best_val_accuracy,
            'test_accuracy': test_accuracy,
            'final_train_loss': train_losses[-1],
            'final_val_loss': val_losses[-1],
            **evaluation_report
        }
    
    def _plot_training_history(self, train_losses, val_losses, val_accuracies, dataset_name):
        """Plot training history"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
        
        # Loss plot
        ax1.plot(train_losses, label='Train Loss')
        ax1.plot(val_losses, label='Val Loss')
        ax1.set_title('Training and Validation Loss')
        ax1.set_xlabel('Epoch')
        ax1.set_ylabel('Loss')
        ax1.legend()
        
        # Accuracy plot
        ax2.plot(val_accuracies, label='Val Accuracy')
        ax2.set_title('Validation Accuracy')
        ax2.set_xlabel('Epoch')
        ax2.set_ylabel('Accuracy')
        ax2.legend()
        
        plt.tight_layout()
        plt.savefig(f'ml/training_history_{dataset_name}.png')
        plt.close()
    
    def _evaluate_model(self, model: nn.Module, test_loader: DataLoader) -> Dict[str, float]:
        """Comprehensive model evaluation"""
        model.eval()
        all_predictions = []
        all_targets = []
        
        with torch.no_grad():
            for data, target in test_loader:
                data, target = data.to(self.device), target.to(self.device)
                output = model(data)
                pred = output.argmax(dim=1)
                all_predictions.extend(pred.cpu().numpy())
                all_targets.extend(target.cpu().numpy())
        
        # Calculate metrics
        accuracy = accuracy_score(all_targets, all_predictions)
        precision, recall, f1, _ = precision_recall_fscore_support(
            all_targets, all_predictions, average='weighted'
        )
        
        # Confusion matrix
        cm = confusion_matrix(all_targets, all_predictions)
        
        # Plot confusion matrix
        plt.figure(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
        plt.title('Confusion Matrix')
        plt.ylabel('True Label')
        plt.xlabel('Predicted Label')
        plt.savefig('ml/confusion_matrix.png')
        plt.close()
        
        return {
            'precision': precision,
            'recall': recall,
            'f1_score': f1
        }

def split_dataset(dataset_path: str, train_ratio: float = 0.8, val_ratio: float = 0.1):
    """Split dataset into train/val/test sets"""
    import shutil
    import random
    
    # Create split directories
    split_dirs = ['train', 'val', 'test']
    for split_dir in split_dirs:
        os.makedirs(os.path.join(dataset_path, split_dir), exist_ok=True)
    
    # Get all categories
    categories = [d for d in os.listdir(dataset_path) 
                 if os.path.isdir(os.path.join(dataset_path, d)) and d not in split_dirs]
    
    for category in categories:
        category_path = os.path.join(dataset_path, category)
        images = [f for f in os.listdir(category_path) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp'))]
        
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
        
        # Move images to respective splits
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

def main():
    parser = argparse.ArgumentParser(description='Train AI Detection Model')
    parser.add_argument('--dataset', type=str, required=True, help='Dataset name or path')
    parser.add_argument('--archive', type=str, help='Archive file to extract')
    parser.add_argument('--epochs', type=int, default=50, help='Number of epochs')
    parser.add_argument('--batch_size', type=int, default=32, help='Batch size')
    parser.add_argument('--lr', type=float, default=0.001, help='Learning rate')
    
    args = parser.parse_args()
    
    # Extract archive if provided
    if args.archive:
        logger.info(f"Extracting archive: {args.archive}")
        success, extract_path, category_counts = archive_extractor.extract_archive(
            args.archive, args.dataset
        )
        if not success:
            logger.error("Failed to extract archive")
            return
        
        dataset_path = extract_path
        logger.info(f"Extracted to: {dataset_path}")
        logger.info(f"Categories: {category_counts}")
        
        # Split dataset
        split_dataset(dataset_path)
    else:
        dataset_path = os.path.join(settings.DATASET_PATH, args.dataset)
    
    # Initialize trainer
    trainer = Trainer(dataset_path)
    trainer.num_epochs = args.epochs
    trainer.batch_size = args.batch_size
    trainer.learning_rate = args.lr
    
    # Train model
    results = trainer.train_model(args.dataset)
    
    logger.info("Training completed!")
    logger.info(f"Results: {results}")

if __name__ == "__main__":
    main()