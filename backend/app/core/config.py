"""
Configuration settings for the AI Authenticity Verification Platform
"""
import os
from typing import List
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # App settings
    APP_NAME: str = "AI Authenticity Verification Platform"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    VERSION: str = "1.0.0"
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # Database
    MONGODB_URL: str = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    DATABASE_NAME: str = os.getenv("DATABASE_NAME", "ai_verification_db")
    
    # CORS
    ALLOWED_HOSTS: List[str] = ["*"]
    
    # File upload settings
    MAX_FILE_SIZE: int = 50 * 1024 * 1024  # 50MB
    UPLOAD_DIR: str = "uploads"
    ALLOWED_IMAGE_EXTENSIONS: List[str] = [".jpg", ".jpeg", ".png", ".bmp", ".tiff"]
    ALLOWED_PDF_EXTENSIONS: List[str] = [".pdf"]
    ALLOWED_ARCHIVE_EXTENSIONS: List[str] = [".zip", ".rar", ".7z", ".tar", ".tar.gz"]
    
    # ML Model settings
    MODEL_PATH: str = "ml/models"
    IMAGE_SIZE: tuple = (224, 224)
    BATCH_SIZE: int = 32
    
    # Training dataset paths
    DATASET_PATH: str = "datasets"
    TRAIN_SPLIT: float = 0.8
    VAL_SPLIT: float = 0.1
    TEST_SPLIT: float = 0.1
    
    class Config:
        env_file = ".env"

settings = Settings()