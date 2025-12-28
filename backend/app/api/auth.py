"""
Authentication API endpoints
"""
from datetime import timedelta
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.models.user import UserCreate, UserLogin, Token, User
from app.services.auth import auth_service
from app.core.config import settings

router = APIRouter()
security = HTTPBearer()

@router.post("/register")
async def register(user_data: UserCreate):
    """Register a new user"""
    try:
        user = await auth_service.create_user(user_data)
        
        # Create tokens for immediate login
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = auth_service.create_access_token(
            data={"sub": user.email}, expires_delta=access_token_expires
        )
        refresh_token = auth_service.create_refresh_token(data={"sub": user.email})
        
        return {
            "token": access_token,
            "refresh_token": refresh_token,
            "user": user
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration failed: {str(e)}"
        )

@router.post("/login", response_model=Token)
async def login(user_credentials: UserLogin):
    """Authenticate user and return JWT tokens"""
    user = await auth_service.authenticate_user(
        user_credentials.email, 
        user_credentials.password
    )
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    # Create tokens
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth_service.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    refresh_token = auth_service.create_refresh_token(data={"sub": user.email})
    
    # Convert user to response format
    user_response = User(**user.dict())
    
    return {
        "token": access_token,
        "refresh_token": refresh_token,
        "user": user_response
    }

@router.post("/refresh", response_model=Token)
async def refresh_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Refresh access token using refresh token"""
    try:
        # Verify refresh token
        email = auth_service.verify_token(credentials.credentials, token_type="refresh")
        
        # Get user
        user = await auth_service.get_user_by_email(email)
        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )
        
        # Create new tokens
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = auth_service.create_access_token(
            data={"sub": user.email}, expires_delta=access_token_expires
        )
        refresh_token = auth_service.create_refresh_token(data={"sub": user.email})
        
        return Token(
            access_token=access_token,
            refresh_token=refresh_token
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )

@router.get("/me", response_model=User)
async def get_current_user_info(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Get current user information"""
    user = await auth_service.get_current_user(credentials.credentials)
    return user

@router.get("/test")
async def test_connection():
    """Test backend connection"""
    return {
        "status": "connected",
        "message": "Backend is running",
        "timestamp": "2024-01-01T00:00:00Z"
    }

@router.post("/logout")
async def logout():
    """Logout endpoint (client-side token removal)"""
    return {"message": "Logged out successfully"}

# Dependency for protected routes
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> User:
    """Dependency to get current authenticated user"""
    return await auth_service.get_current_user(credentials.credentials)