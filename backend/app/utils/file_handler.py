"""
File handling utilities for uploads and temporary files
"""
import os
import logging
import tempfile
import shutil
from typing import Optional
from fastapi import UploadFile
from app.core.config import settings

logger = logging.getLogger(__name__)

class FileHandler:
    def __init__(self):
        # Ensure upload directory exists
        os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    
    async def save_upload_file(self, upload_file: UploadFile) -> str:
        """Save uploaded file to temporary location"""
        try:
            # Create temporary file
            suffix = os.path.splitext(upload_file.filename)[1]
            temp_file = tempfile.NamedTemporaryFile(
                delete=False, 
                suffix=suffix,
                dir=settings.UPLOAD_DIR
            )
            
            # Write file content
            content = await upload_file.read()
            temp_file.write(content)
            temp_file.close()
            
            logger.info(f"Saved upload file: {upload_file.filename} -> {temp_file.name}")
            return temp_file.name
            
        except Exception as e:
            logger.error(f"Error saving upload file: {e}")
            raise
    
    def cleanup_file(self, file_path: str):
        """Remove temporary file"""
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.info(f"Cleaned up file: {file_path}")
        except Exception as e:
            logger.error(f"Error cleaning up file {file_path}: {e}")
    
    def cleanup_directory(self, dir_path: str):
        """Remove directory and all contents"""
        try:
            if os.path.exists(dir_path):
                shutil.rmtree(dir_path)
                logger.info(f"Cleaned up directory: {dir_path}")
        except Exception as e:
            logger.error(f"Error cleaning up directory {dir_path}: {e}")
    
    def get_file_size(self, file_path: str) -> int:
        """Get file size in bytes"""
        try:
            return os.path.getsize(file_path)
        except Exception:
            return 0
    
    def is_valid_file_type(self, filename: str, allowed_extensions: list) -> bool:
        """Check if file has valid extension"""
        return any(filename.lower().endswith(ext) for ext in allowed_extensions)

# Global file handler instance
file_handler = FileHandler()