"""
Authentication service with JWT token management
"""
import logging
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status
from app.core.config import settings
from app.core.database import get_database
from app.models.user import UserInDB, UserCreate, User

logger = logging.getLogger(__name__)

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    def __init__(self):
        self.db = get_database()

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash"""
        return pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        """Hash a password"""
        return pwd_context.hash(password)

    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None):
        """Create JWT access token"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode.update({"exp": expire, "type": "access"})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt

    def create_refresh_token(self, data: dict):
        """Create JWT refresh token"""
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        to_encode.update({"exp": expire, "type": "refresh"})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt

    def verify_token(self, token: str, token_type: str = "access"):
        """Verify and decode JWT token"""
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            email: str = payload.get("sub")
            token_type_check: str = payload.get("type")
            
            if email is None or token_type_check != token_type:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token"
                )
            return email
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )

    async def get_user_by_email(self, email: str) -> Optional[UserInDB]:
        """Get user by email from database"""
        user_doc = await self.db.users.find_one({"email": email})
        if user_doc:
            return UserInDB(**user_doc)
        return None

    async def get_user_by_username(self, username: str) -> Optional[UserInDB]:
        """Get user by username from database"""
        user_doc = await self.db.users.find_one({"username": username})
        if user_doc:
            return UserInDB(**user_doc)
        return None

    async def create_user(self, user_create: UserCreate) -> User:
        """Create a new user"""
        # Check if user already exists
        existing_user = await self.get_user_by_email(user_create.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        existing_username = await self.get_user_by_username(user_create.username)
        if existing_username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )

        # Create user document
        user_dict = user_create.dict()
        user_dict["hashed_password"] = self.get_password_hash(user_create.password)
        user_dict["plan"] = "free"  # Default plan
        user_dict["analysis_count"] = 0
        user_dict["monthly_analysis_limit"] = 10  # Free plan limit
        del user_dict["password"]
        
        user_in_db = UserInDB(**user_dict)
        
        # Insert into database
        result = await self.db.users.insert_one(user_in_db.dict(by_alias=True))
        
        # Return user without password
        created_user = await self.db.users.find_one({"_id": result.inserted_id})
        return User(**created_user)

    async def authenticate_user(self, email: str, password: str) -> Optional[UserInDB]:
        """Authenticate user with email and password"""
        user = await self.get_user_by_email(email)
        if not user:
            return None
        if not self.verify_password(password, user.hashed_password):
            return None
        return user

    async def get_current_user(self, token: str) -> User:
        """Get current user from JWT token"""
        email = self.verify_token(token)
        user = await self.get_user_by_email(email)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )
        return User(**user.dict())

# Global auth service instance
auth_service = AuthService()