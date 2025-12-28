"""
Archive extraction service for training datasets
Supports ZIP, RAR, 7Z, TAR formats
"""
import os
import logging
import zipfile
import tarfile
import shutil
from pathlib import Path
from typing import List, Dict, Tuple
import hashlib
from PIL import Image
import rarfile

from app.core.config import settings
from app.models.analysis import TrainingDataset

logger = logging.getLogger(__name__)

class ArchiveExtractor:
    def __init__(self):
        self.supported_formats = {
            '.zip': self._extract_zip,
            '.rar': self._extract_rar,
            '.7z': self._extract_7z,
            '.tar': self._extract_tar,
            '.tar.gz': self._extract_tar,
            '.tgz': self._extract_tar
        }
        
        # Ensure dataset directory exists
        os.makedirs(settings.DATASET_PATH, exist_ok=True)

    def get_file_hash(self, filepath: str) -> str:
        """Generate SHA256 hash of file"""
        hash_sha256 = hashlib.sha256()
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha256.update(chunk)
        return hash_sha256.hexdigest()

    def is_valid_image(self, filepath: str) -> bool:
        """Check if file is a valid image"""
        try:
            with Image.open(filepath) as img:
                img.verify()
            return True
        except Exception:
            return False

    def _extract_zip(self, archive_path: str, extract_to: str) -> bool:
        """Extract ZIP archive"""
        try:
            with zipfile.ZipFile(archive_path, 'r') as zip_ref:
                zip_ref.extractall(extract_to)
            return True
        except Exception as e:
            logger.error(f"Error extracting ZIP: {e}")
            return False

    def _extract_rar(self, archive_path: str, extract_to: str) -> bool:
        """Extract RAR archive"""
        try:
            with rarfile.RarFile(archive_path, 'r') as rar_ref:
                rar_ref.extractall(extract_to)
            return True
        except Exception as e:
            logger.error(f"Error extracting RAR: {e}")
            return False

    def _extract_7z(self, archive_path: str, extract_to: str) -> bool:
        """Extract 7Z archive using py7zr"""
        try:
            import py7zr
            with py7zr.SevenZipFile(archive_path, mode='r') as z:
                z.extractall(extract_to)
            return True
        except Exception as e:
            logger.error(f"Error extracting 7Z: {e}")
            return False

    def _extract_tar(self, archive_path: str, extract_to: str) -> bool:
        """Extract TAR archive"""
        try:
            with tarfile.open(archive_path, 'r:*') as tar_ref:
                tar_ref.extractall(extract_to)
            return True
        except Exception as e:
            logger.error(f"Error extracting TAR: {e}")
            return False

    def extract_archive(self, archive_path: str, dataset_name: str) -> Tuple[bool, str, Dict[str, int]]:
        """
        Extract archive and organize images by category
        Returns: (success, extract_path, category_counts)
        """
        # Determine file extension
        file_ext = None
        for ext in self.supported_formats.keys():
            if archive_path.lower().endswith(ext):
                file_ext = ext
                break
        
        if not file_ext:
            logger.error(f"Unsupported archive format: {archive_path}")
            return False, "", {}

        # Create extraction directory
        extract_path = os.path.join(settings.DATASET_PATH, dataset_name)
        os.makedirs(extract_path, exist_ok=True)

        # Extract archive
        success = self.supported_formats[file_ext](archive_path, extract_path)
        if not success:
            return False, "", {}

        # Organize and count images by category
        category_counts = self._organize_images(extract_path)
        
        return True, extract_path, category_counts

    def _organize_images(self, extract_path: str) -> Dict[str, int]:
        """
        Organize extracted images into categories and count them
        Expected structure: dataset/category/images
        """
        category_counts = {}
        
        # Walk through extracted directory
        for root, dirs, files in os.walk(extract_path):
            # Skip root directory
            if root == extract_path:
                continue
                
            # Get category name (folder name)
            category = os.path.basename(root)
            if category not in category_counts:
                category_counts[category] = 0
            
            # Count valid images in this category
            for file in files:
                file_path = os.path.join(root, file)
                file_ext = os.path.splitext(file)[1].lower()
                
                if file_ext in settings.ALLOWED_IMAGE_EXTENSIONS:
                    if self.is_valid_image(file_path):
                        category_counts[category] += 1
                    else:
                        # Remove invalid image
                        os.remove(file_path)
                        logger.warning(f"Removed invalid image: {file_path}")
                else:
                    # Remove non-image files
                    os.remove(file_path)
        
        # Remove empty categories
        empty_categories = [cat for cat, count in category_counts.items() if count == 0]
        for cat in empty_categories:
            cat_path = os.path.join(extract_path, cat)
            if os.path.exists(cat_path):
                shutil.rmtree(cat_path)
            del category_counts[cat]
        
        logger.info(f"Organized dataset: {category_counts}")
        return category_counts

    def get_dataset_structure(self, dataset_path: str) -> Dict[str, List[str]]:
        """Get the structure of an extracted dataset"""
        structure = {}
        
        for category in os.listdir(dataset_path):
            category_path = os.path.join(dataset_path, category)
            if os.path.isdir(category_path):
                images = []
                for file in os.listdir(category_path):
                    file_path = os.path.join(category_path, file)
                    if os.path.isfile(file_path):
                        file_ext = os.path.splitext(file)[1].lower()
                        if file_ext in settings.ALLOWED_IMAGE_EXTENSIONS:
                            images.append(file_path)
                structure[category] = images
        
        return structure

    def cleanup_dataset(self, dataset_path: str):
        """Remove extracted dataset directory"""
        try:
            if os.path.exists(dataset_path):
                shutil.rmtree(dataset_path)
                logger.info(f"Cleaned up dataset: {dataset_path}")
        except Exception as e:
            logger.error(f"Error cleaning up dataset: {e}")

# Global extractor instance
archive_extractor = ArchiveExtractor()