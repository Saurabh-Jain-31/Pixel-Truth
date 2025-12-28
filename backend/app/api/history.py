"""
Analysis history API endpoints
"""
import logging
from typing import Optional
from fastapi import APIRouter, HTTPException, status, Depends, Query
from app.models.user import User
from app.models.analysis import AnalysisHistory
from app.api.auth import get_current_user
from app.core.database import get_database

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("", response_model=AnalysisHistory)
async def get_analysis_history(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    analysis_type: Optional[str] = Query(None, regex="^(image|pdf)$"),
    current_user: User = Depends(get_current_user)
):
    """Get user's analysis history with pagination"""
    
    try:
        db = get_database()
        skip = (page - 1) * page_size
        
        # Build query
        query = {"user_id": current_user.id}
        
        # Combine both collections
        analyses = []
        
        # Get image analyses
        if analysis_type is None or analysis_type == "image":
            image_analyses = await db.image_analyses.find(query).sort("created_at", -1).to_list(length=None)
            for analysis in image_analyses:
                analyses.append({
                    "id": str(analysis["_id"]),
                    "type": "image",
                    "filename": analysis["filename"],
                    "file_size": analysis["file_size"],
                    "prediction": analysis["result"]["prediction"],
                    "confidence_score": analysis["result"]["confidence_score"],
                    "processing_time": analysis["result"]["processing_time"],
                    "created_at": analysis["created_at"]
                })
        
        # Get PDF analyses
        if analysis_type is None or analysis_type == "pdf":
            pdf_analyses = await db.pdf_analyses.find(query).sort("created_at", -1).to_list(length=None)
            for analysis in pdf_analyses:
                analyses.append({
                    "id": str(analysis["_id"]),
                    "type": "pdf",
                    "filename": analysis["filename"],
                    "file_size": analysis["file_size"],
                    "ai_probability": analysis["result"]["ai_generated_probability"],
                    "processing_time": analysis["result"]["processing_time"],
                    "page_count": analysis["page_count"],
                    "created_at": analysis["created_at"]
                })
        
        # Sort by created_at descending
        analyses.sort(key=lambda x: x["created_at"], reverse=True)
        
        # Apply pagination
        total_count = len(analyses)
        paginated_analyses = analyses[skip:skip + page_size]
        
        return AnalysisHistory(
            analyses=paginated_analyses,
            total_count=total_count,
            page=page,
            page_size=page_size
        )
        
    except Exception as e:
        logger.error(f"Error getting analysis history: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve analysis history"
        )

@router.get("/image/{analysis_id}")
async def get_image_analysis_detail(
    analysis_id: str,
    current_user: User = Depends(get_current_user)
):
    """Get detailed image analysis results"""
    
    try:
        db = get_database()
        
        # Find analysis
        analysis = await db.image_analyses.find_one({
            "_id": analysis_id,
            "user_id": current_user.id
        })
        
        if not analysis:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Analysis not found"
            )
        
        return {
            "id": str(analysis["_id"]),
            "filename": analysis["filename"],
            "file_size": analysis["file_size"],
            "file_hash": analysis["file_hash"],
            "result": analysis["result"],
            "exif_data": analysis["exif_data"],
            "created_at": analysis["created_at"]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting image analysis detail: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve analysis details"
        )

@router.get("/pdf/{analysis_id}")
async def get_pdf_analysis_detail(
    analysis_id: str,
    current_user: User = Depends(get_current_user)
):
    """Get detailed PDF analysis results"""
    
    try:
        db = get_database()
        
        # Find analysis
        analysis = await db.pdf_analyses.find_one({
            "_id": analysis_id,
            "user_id": current_user.id
        })
        
        if not analysis:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Analysis not found"
            )
        
        return {
            "id": str(analysis["_id"]),
            "filename": analysis["filename"],
            "file_size": analysis["file_size"],
            "file_hash": analysis["file_hash"],
            "page_count": analysis["page_count"],
            "result": analysis["result"],
            "extracted_text": analysis["extracted_text"],
            "metadata": analysis["metadata"],
            "created_at": analysis["created_at"]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting PDF analysis detail: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve analysis details"
        )

@router.delete("/image/{analysis_id}")
async def delete_image_analysis(
    analysis_id: str,
    current_user: User = Depends(get_current_user)
):
    """Delete an image analysis record"""
    
    try:
        db = get_database()
        
        # Delete analysis
        result = await db.image_analyses.delete_one({
            "_id": analysis_id,
            "user_id": current_user.id
        })
        
        if result.deleted_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Analysis not found"
            )
        
        return {"message": "Analysis deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting image analysis: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete analysis"
        )

@router.delete("/pdf/{analysis_id}")
async def delete_pdf_analysis(
    analysis_id: str,
    current_user: User = Depends(get_current_user)
):
    """Delete a PDF analysis record"""
    
    try:
        db = get_database()
        
        # Delete analysis
        result = await db.pdf_analyses.delete_one({
            "_id": analysis_id,
            "user_id": current_user.id
        })
        
        if result.deleted_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Analysis not found"
            )
        
        return {"message": "Analysis deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting PDF analysis: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete analysis"
        )