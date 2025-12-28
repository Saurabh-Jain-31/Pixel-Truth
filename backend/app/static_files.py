"""
Static file serving for frontend integration
"""
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
from pathlib import Path

def setup_static_files(app: FastAPI):
    """Setup static file serving for frontend"""
    
    # Path to frontend build directory (dist folder from Vite build)
    dist_dir = Path(__file__).parent.parent / "dist"
    uploads_dir = Path(__file__).parent.parent / "uploads"
    
    # Create uploads directory if it doesn't exist
    uploads_dir.mkdir(exist_ok=True)
    
    # Mount uploads directory for file serving
    if uploads_dir.exists():
        app.mount("/uploads", StaticFiles(directory=str(uploads_dir)), name="uploads")
    
    # Mount static files from Vite build
    if dist_dir.exists():
        # Mount assets directory
        assets_dir = dist_dir / "assets"
        if assets_dir.exists():
            app.mount("/assets", StaticFiles(directory=str(assets_dir)), name="assets")
        
        # Serve React app at root
        @app.get("/")
        async def serve_frontend():
            """Serve the React app"""
            index_file = dist_dir / "index.html"
            if index_file.exists():
                return FileResponse(str(index_file))
            else:
                return {
                    "message": "AI Authenticity Verification Platform API", 
                    "status": "healthy",
                    "frontend": "not_built",
                    "note": "Run 'npm run build' to build the frontend"
                }
        
        # Catch-all route for React Router (SPA routing)
        @app.get("/{path:path}")
        async def serve_frontend_routes(path: str):
            """Serve React app for all frontend routes"""
            # Don't intercept API routes, docs, or static assets
            if (path.startswith("api/") or 
                path.startswith("docs") or 
                path.startswith("redoc") or 
                path.startswith("uploads/") or
                path.startswith("assets/")):
                raise HTTPException(status_code=404, detail="Not found")
            
            index_file = dist_dir / "index.html"
            if index_file.exists():
                return FileResponse(str(index_file))
            else:
                raise HTTPException(status_code=404, detail="Frontend not built")
    else:
        # If no dist directory, just serve API info at root
        @app.get("/")
        async def api_info():
            return {
                "message": "AI Authenticity Verification Platform API",
                "status": "healthy", 
                "version": "1.0.0",
                "frontend": "not_built",
                "note": "Run 'npm run build' to build the frontend",
                "api_docs": "/docs"
            }
    
    return app