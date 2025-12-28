"""
Analysis API endpoints for image and PDF processing
"""
import os
import logging
from typing import List
from fastapi import APIRouter, HTTPException, status, Depends, UploadFile, File, Form
from fastapi.responses import JSONResponse
import uuid
import time

from app.models.user import User
from app.models.analysis import ImageAnalysis, PDFAnalysis, TrainingDataset
from app.api.auth import get_current_user
from app.core.config import settings
from app.core.database import get_database
from app.services.image_analysis import image_analysis_service
from app.services.pdf_analysis import pdf_analysis_service
from app.services.archive_extractor import archive_extractor
from app.utils.file_handler import file_handler

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/upload")
async def upload_file(
    image: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    """Upload file endpoint that frontend expects"""
    
    # Validate file type
    if not image.filename.lower().endswith(tuple(settings.ALLOWED_IMAGE_EXTENSIONS)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file type. Allowed: {settings.ALLOWED_IMAGE_EXTENSIONS}"
        )
    
    # Validate file size
    if image.size and image.size > settings.MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File too large. Max size: {settings.MAX_FILE_SIZE} bytes"
        )
    
    try:
        # Generate unique filename
        file_id = str(uuid.uuid4())
        file_extension = os.path.splitext(image.filename)[1]
        unique_filename = f"{file_id}{file_extension}"
        
        # Save uploaded file
        temp_path = await file_handler.save_upload_file(image)
        
        # Move to uploads directory with unique name
        uploads_dir = "uploads"
        os.makedirs(uploads_dir, exist_ok=True)
        final_path = os.path.join(uploads_dir, unique_filename)
        
        # Move file to final location
        import shutil
        shutil.move(temp_path, final_path)
        
        return {
            "filename": unique_filename,
            "original_name": image.filename,
            "size": image.size,
            "mimetype": image.content_type,
            "upload_id": file_id
        }
        
    except Exception as e:
        logger.error(f"Error uploading file: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Upload failed: {str(e)}"
        )

@router.post("/analyze")
async def analyze_uploaded_file(
    filename: str = Form(...),
    original_name: str = Form(...),
    current_user: User = Depends(get_current_user)
):
    """Analyze uploaded file"""
    
    try:
        # Check if file exists
        file_path = os.path.join("uploads", filename)
        if not os.path.exists(file_path):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="File not found"
            )
        
        # Get file hash
        file_hash = image_analysis_service.get_file_hash(file_path)
        
        # Extract EXIF data
        exif_data = image_analysis_service.extract_exif_data(file_path)
        
        # Perform analysis
        analysis_result = image_analysis_service.analyze_image(file_path, original_name)
        
        # Get file size
        file_size = os.path.getsize(file_path)
        
        # Create analysis record
        analysis = ImageAnalysis(
            user_id=current_user.id,
            filename=original_name,
            file_size=file_size,
            file_hash=file_hash,
            result=analysis_result,
            exif_data=exif_data
        )
        
        # Save to database
        db = get_database()
        result = await db.image_analyses.insert_one(analysis.dict(by_alias=True))
        
        # Log API usage
        await db.api_logs.insert_one({
            "user_id": current_user.id,
            "endpoint": "/api/analyze/analyze",
            "filename": original_name,
            "file_size": file_size,
            "result": analysis_result.prediction,
            "confidence": analysis_result.confidence_score,
            "timestamp": analysis.created_at
        })
        
        return {
            "analysis_id": str(result.inserted_id),
            "prediction": analysis_result.prediction,
            "confidence_score": analysis_result.confidence_score,
            "processing_time": analysis_result.processing_time,
            "metadata": analysis_result.metadata,
            "exif_data": exif_data,
            "status": "completed"
        }
        
    except Exception as e:
        logger.error(f"Error analyzing file: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Analysis failed: {str(e)}"
        )

@router.post("/image")
async def analyze_image(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    """Analyze uploaded image for AI generation detection"""
    
    # Validate file type
    if not file.filename.lower().endswith(tuple(settings.ALLOWED_IMAGE_EXTENSIONS)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file type. Allowed: {settings.ALLOWED_IMAGE_EXTENSIONS}"
        )
    
    # Validate file size
    if file.size > settings.MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File too large. Max size: {settings.MAX_FILE_SIZE} bytes"
        )
    
    try:
        # Save uploaded file temporarily
        temp_path = await file_handler.save_upload_file(file)
        
        # Get file hash
        file_hash = image_analysis_service.get_file_hash(temp_path)
        
        # Extract EXIF data
        exif_data = image_analysis_service.extract_exif_data(temp_path)
        
        # Perform analysis
        analysis_result = image_analysis_service.analyze_image(temp_path, file.filename)
        
        # Create analysis record
        analysis = ImageAnalysis(
            user_id=current_user.id,
            filename=file.filename,
            file_size=file.size,
            file_hash=file_hash,
            result=analysis_result,
            exif_data=exif_data
        )
        
        # Save to database
        db = get_database()
        result = await db.image_analyses.insert_one(analysis.dict(by_alias=True))
        
        # Clean up temp file
        file_handler.cleanup_file(temp_path)
        
        # Log API usage
        await db.api_logs.insert_one({
            "user_id": current_user.id,
            "endpoint": "/analyze/image",
            "filename": file.filename,
            "file_size": file.size,
            "result": analysis_result.prediction,
            "confidence": analysis_result.confidence_score,
            "timestamp": analysis.created_at
        })
        
        return {
            "analysis_id": str(result.inserted_id),
            "prediction": analysis_result.prediction,
            "confidence_score": analysis_result.confidence_score,
            "processing_time": analysis_result.processing_time,
            "metadata": analysis_result.metadata,
            "exif_data": exif_data
        }
        
    except Exception as e:
        logger.error(f"Error analyzing image: {e}")
        # Clean up temp file if it exists
        if 'temp_path' in locals():
            file_handler.cleanup_file(temp_path)
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Analysis failed: {str(e)}"
        )

@router.post("/pdf")
async def analyze_pdf(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    """Analyze uploaded PDF for AI-generated content"""
    
    # Validate file type
    if not file.filename.lower().endswith(tuple(settings.ALLOWED_PDF_EXTENSIONS)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file type. Allowed: {settings.ALLOWED_PDF_EXTENSIONS}"
        )
    
    # Validate file size
    if file.size > settings.MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File too large. Max size: {settings.MAX_FILE_SIZE} bytes"
        )
    
    try:
        # Save uploaded file temporarily
        temp_path = await file_handler.save_upload_file(file)
        
        # Get file hash
        file_hash = pdf_analysis_service.get_file_hash(temp_path)
        
        # Extract content
        content = pdf_analysis_service.extract_text_and_metadata(temp_path)
        
        # Perform analysis
        analysis_result = pdf_analysis_service.analyze_pdf(temp_path, file.filename)
        
        # Create analysis record
        analysis = PDFAnalysis(
            user_id=current_user.id,
            filename=file.filename,
            file_size=file.size,
            file_hash=file_hash,
            page_count=content['page_count'],
            result=analysis_result,
            extracted_text=content['text'][:5000],  # Store first 5000 chars
            metadata=content['metadata']
        )
        
        # Save to database
        db = get_database()
        result = await db.pdf_analyses.insert_one(analysis.dict(by_alias=True))
        
        # Clean up temp file
        file_handler.cleanup_file(temp_path)
        
        # Log API usage
        await db.api_logs.insert_one({
            "user_id": current_user.id,
            "endpoint": "/analyze/pdf",
            "filename": file.filename,
            "file_size": file.size,
            "ai_probability": analysis_result.ai_generated_probability,
            "timestamp": analysis.created_at
        })
        
        return {
            "analysis_id": str(result.inserted_id),
            "ai_generated_probability": analysis_result.ai_generated_probability,
            "metadata_inconsistencies": analysis_result.metadata_inconsistencies,
            "suspicious_patterns": analysis_result.suspicious_patterns,
            "processing_time": analysis_result.processing_time,
            "page_count": content['page_count'],
            "text_analysis": analysis_result.text_analysis
        }
        
    except Exception as e:
        logger.error(f"Error analyzing PDF: {e}")
        # Clean up temp file if it exists
        if 'temp_path' in locals():
            file_handler.cleanup_file(temp_path)
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Analysis failed: {str(e)}"
        )

@router.post("/dataset/upload")
async def upload_training_dataset(
    file: UploadFile = File(...),
    name: str = Form(...),
    description: str = Form(None),
    current_user: User = Depends(get_current_user)
):
    """Upload and extract archive for training dataset"""
    
    # Check user permissions (only pro users can upload datasets)
    if current_user.role != "pro":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Pro subscription required for dataset uploads"
        )
    
    # Validate file type
    if not any(file.filename.lower().endswith(ext) for ext in settings.ALLOWED_ARCHIVE_EXTENSIONS):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid archive type. Allowed: {settings.ALLOWED_ARCHIVE_EXTENSIONS}"
        )
    
    # Validate file size
    if file.size > settings.MAX_FILE_SIZE * 5:  # Allow larger archives
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"Archive too large. Max size: {settings.MAX_FILE_SIZE * 5} bytes"
        )
    
    try:
        # Save uploaded archive
        temp_path = await file_handler.save_upload_file(file)
        
        # Extract archive
        success, extract_path, category_counts = archive_extractor.extract_archive(
            temp_path, name
        )
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to extract archive"
            )
        
        # Create dataset record
        dataset = TrainingDataset(
            name=name,
            description=description,
            archive_filename=file.filename,
            extracted_path=extract_path,
            total_images=sum(category_counts.values()),
            categories=category_counts,
            status="ready"
        )
        
        # Save to database
        db = get_database()
        result = await db.training_datasets.insert_one(dataset.dict(by_alias=True))
        
        # Clean up temp archive
        file_handler.cleanup_file(temp_path)
        
        logger.info(f"Dataset uploaded: {name} with {dataset.total_images} images")
        
        return {
            "dataset_id": str(result.inserted_id),
            "name": name,
            "total_images": dataset.total_images,
            "categories": category_counts,
            "status": "ready",
            "message": "Dataset uploaded and extracted successfully"
        }
        
    except Exception as e:
        logger.error(f"Error uploading dataset: {e}")
        # Clean up files if they exist
        if 'temp_path' in locals():
            file_handler.cleanup_file(temp_path)
        if 'extract_path' in locals():
            archive_extractor.cleanup_dataset(extract_path)
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Dataset upload failed: {str(e)}"
        )

@router.get("/datasets")
async def list_datasets(current_user: User = Depends(get_current_user)):
    """List available training datasets"""
    
    if current_user.role != "pro":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Pro subscription required"
        )
    
    try:
        db = get_database()
        datasets = await db.training_datasets.find().to_list(length=100)
        
        return {
            "datasets": [
                {
                    "id": str(dataset["_id"]),
                    "name": dataset["name"],
                    "description": dataset.get("description"),
                    "total_images": dataset["total_images"],
                    "categories": dataset["categories"],
                    "status": dataset["status"],
                    "created_at": dataset["created_at"]
                }
                for dataset in datasets
            ]
        }
        
    except Exception as e:
        logger.error(f"Error listing datasets: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to list datasets"
        )