#!/usr/bin/env python3
"""
Create a sample dataset for AI detection training
This creates synthetic images for demonstration purposes
"""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import random

def create_sample_dataset():
    """Create sample images for training demonstration"""
    
    # Create dataset structure
    categories = ['authentic', 'ai_generated', 'manipulated']
    dataset_path = 'datasets/sample_dataset'
    
    for category in categories:
        os.makedirs(os.path.join(dataset_path, category), exist_ok=True)
    
    # Generate sample images for each category
    for category in categories:
        category_path = os.path.join(dataset_path, category)
        
        for i in range(20):  # 20 images per category
            # Create a 224x224 RGB image
            img = Image.new('RGB', (224, 224))
            draw = ImageDraw.Draw(img)
            
            if category == 'authentic':
                # Simulate authentic photos with natural patterns
                # Add some noise and realistic colors
                pixels = np.random.randint(0, 255, (224, 224, 3), dtype=np.uint8)
                # Add some structure
                for x in range(0, 224, 20):
                    for y in range(0, 224, 20):
                        color = (random.randint(100, 200), random.randint(100, 200), random.randint(100, 200))
                        draw.rectangle([x, y, x+15, y+15], fill=color)
                
            elif category == 'ai_generated':
                # Simulate AI-generated images with perfect patterns
                # Very clean, geometric patterns
                colors = [(255, 100, 100), (100, 255, 100), (100, 100, 255)]
                for x in range(0, 224, 32):
                    for y in range(0, 224, 32):
                        color = random.choice(colors)
                        draw.rectangle([x, y, x+30, y+30], fill=color)
                
            else:  # manipulated
                # Simulate manipulated images with artifacts
                # Mix of patterns to simulate editing artifacts
                base_color = (random.randint(50, 150), random.randint(50, 150), random.randint(50, 150))
                draw.rectangle([0, 0, 224, 224], fill=base_color)
                
                # Add some "manipulation" artifacts
                for _ in range(10):
                    x, y = random.randint(0, 200), random.randint(0, 200)
                    w, h = random.randint(10, 30), random.randint(10, 30)
                    artifact_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                    draw.rectangle([x, y, x+w, y+h], fill=artifact_color)
            
            # Save image
            img_path = os.path.join(category_path, f'{category}_{i:03d}.jpg')
            img.save(img_path, 'JPEG', quality=85)
    
    print(f"Sample dataset created at: {dataset_path}")
    print("Categories:")
    for category in categories:
        count = len(os.listdir(os.path.join(dataset_path, category)))
        print(f"  {category}: {count} images")
    
    return dataset_path

if __name__ == "__main__":
    create_sample_dataset()