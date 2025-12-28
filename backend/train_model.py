#!/usr/bin/env python3
"""
Standalone training script for AI detection model
Usage: python train_model.py --archive dataset.zip --name my_dataset
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ml.train import main

if __name__ == "__main__":
    main()