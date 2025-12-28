#!/usr/bin/env python3
"""
Quick training script for demonstration
This will train a simple model on the sample dataset
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
import logging
from create_sample_dataset import create_sample_dataset
from ml.train import Trainer, split_dataset

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def quick_train():
    """Quick training demonstration"""
    
    print("🚀 Starting AI Detection Model Training...")
    print("=" * 50)
    
    # Step 1: Create sample dataset
    print("📁 Creating sample dataset...")
    dataset_path = create_sample_dataset()
    
    # Step 2: Split dataset
    print("✂️ Splitting dataset into train/val/test...")
    split_dataset(dataset_path, train_ratio=0.7, val_ratio=0.2)
    
    # Step 3: Initialize trainer with reduced parameters for demo
    print("🏋️ Initializing trainer...")
    trainer = Trainer(dataset_path)
    trainer.num_epochs = 5  # Quick training
    trainer.batch_size = 8  # Small batch for demo
    trainer.learning_rate = 0.001
    trainer.patience = 3    # Early stopping
    
    # Step 4: Train model
    print("🤖 Training AI detection model...")
    print("This may take a few minutes...")
    
    try:
        results = trainer.train_model("sample_dataset")
        
        print("\n🎉 Training completed!")
        print("=" * 50)
        print("📊 Training Results:")
        print(f"  Best Validation Accuracy: {results['best_val_accuracy']:.4f}")
        print(f"  Test Accuracy: {results['test_accuracy']:.4f}")
        print(f"  Final Training Loss: {results['final_train_loss']:.4f}")
        print(f"  Precision: {results.get('precision', 0):.4f}")
        print(f"  Recall: {results.get('recall', 0):.4f}")
        print(f"  F1 Score: {results.get('f1_score', 0):.4f}")
        
        print("\n📁 Model saved to: ml/models/ai_detection_model_sample_dataset.pth")
        print("🔍 Training plots saved to: ml/training_history_sample_dataset.png")
        print("📈 Confusion matrix saved to: ml/confusion_matrix.png")
        
        return True
        
    except Exception as e:
        logger.error(f"Training failed: {e}")
        print(f"\n❌ Training failed: {e}")
        return False

if __name__ == "__main__":
    success = quick_train()
    if success:
        print("\n✅ AI model training completed successfully!")
        print("You can now use the trained model for image analysis.")
    else:
        print("\n❌ Training failed. Check the logs for details.")