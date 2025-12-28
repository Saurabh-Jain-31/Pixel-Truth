"""
Analysis data models and schemas
"""
from datetime import datetime
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field
from bson import ObjectId
from app.models.user import PyObjectId

class ImageAnalysisResult(BaseModel):
    prediction: str  # "ai_generated", "manipulated", "authentic"
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    model_version: str
    processing_time: float
    metadata: Dict[str, Any] = {}

class ImageAnalysis(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user_id: PyObjectId
    filename: str
    file_size: int
    file_hash: str
    result: ImageAnalysisResult
    exif_data: Dict[str, Any] = {}
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class PDFAnalysisResult(BaseModel):
    ai_generated_probability: float = Field(..., ge=0.0, le=1.0)
    metadata_inconsistencies: List[str] = []
    suspicious_patterns: List[str] = []
    text_analysis: Dict[str, Any] = {}
    processing_time: float

class PDFAnalysis(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user_id: PyObjectId
    filename: str
    file_size: int
    file_hash: str
    page_count: int
    result: PDFAnalysisResult
    extracted_text: str
    metadata: Dict[str, Any] = {}
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class AnalysisHistory(BaseModel):
    analyses: List[Dict[str, Any]]
    total_count: int
    page: int
    page_size: int

class TrainingDataset(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str
    description: Optional[str] = None
    archive_filename: str
    extracted_path: str
    total_images: int
    categories: Dict[str, int]  # category -> count
    created_at: datetime = Field(default_factory=datetime.utcnow)
    status: str = "processing"  # processing, ready, error

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}