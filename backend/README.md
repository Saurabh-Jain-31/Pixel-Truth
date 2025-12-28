# AI Authenticity Verification Platform - Backend

A production-ready backend system for detecting AI-generated content in images and PDFs using machine learning and metadata analysis.

## 🚀 Features

### Core Functionality
- **Image AI Detection**: CNN-based model to classify images as authentic, AI-generated, or manipulated
- **PDF Content Analysis**: Detect AI-generated text patterns and metadata inconsistencies
- **OSINT Metadata Analysis**: Extract and analyze EXIF data, detect suspicious patterns
- **Training Pipeline**: Extract datasets from archives and train custom models
- **Secure Authentication**: JWT-based auth with access/refresh tokens
- **User Management**: Role-based access (free/pro users)

### Technical Features
- **FastAPI Framework**: High-performance async API
- **MongoDB Database**: Scalable document storage
- **PyTorch ML Models**: CNN-based image classification
- **Archive Support**: ZIP, RAR, 7Z, TAR extraction for training data
- **Docker Ready**: Containerized deployment
- **Production Safe**: No hardcoded secrets, proper logging

## 🛠️ Tech Stack

- **Backend**: FastAPI (Python 3.10+)
- **ML Framework**: PyTorch
- **Database**: MongoDB
- **Image Processing**: OpenCV, PIL
- **PDF Processing**: PyMuPDF
- **Authentication**: JWT tokens
- **Archive Handling**: rarfile, py7zr
- **Deployment**: Docker

## 📁 Project Structure

```
backend/
├── app/
│   ├── main.py              # FastAPI application entry point
│   ├── api/                 # API route handlers
│   │   ├── auth.py          # Authentication endpoints
│   │   ├── analysis.py      # Image/PDF analysis endpoints
│   │   └── history.py       # Analysis history endpoints
│   ├── models/              # Pydantic data models
│   │   ├── user.py          # User models
│   │   └── analysis.py      # Analysis result models
│   ├── services/            # Business logic services
│   │   ├── auth.py          # Authentication service
│   │   ├── image_analysis.py # Image analysis service
│   │   ├── pdf_analysis.py  # PDF analysis service
│   │   └── archive_extractor.py # Archive extraction service
│   ├── utils/               # Utility functions
│   │   └── file_handler.py  # File handling utilities
│   └── core/                # Core configuration
│       ├── config.py        # Application settings
│       └── database.py      # Database connection
├── ml/                      # Machine learning components
│   ├── model.py             # CNN model definition
│   └── train.py             # Training script
├── tests/                   # Test files
├── Dockerfile               # Docker configuration
├── requirements.txt         # Python dependencies
├── .env.example            # Environment variables template
└── README.md               # This file
```

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- MongoDB
- Docker (optional)

### Local Development Setup

1. **Clone and navigate to backend directory**
```bash
git clone <repository>
cd backend
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. **Start MongoDB**
```bash
# Using Docker
docker run -d -p 27017:27017 --name mongodb mongo:latest

# Or install MongoDB locally
```

6. **Run the application**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

### Docker Deployment

1. **Build Docker image**
```bash
docker build -t ai-verification-backend .
```

2. **Run with Docker Compose** (create docker-compose.yml)
```yaml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - MONGODB_URL=mongodb://mongodb:27017
      - SECRET_KEY=your-secret-key
    depends_on:
      - mongodb
  
  mongodb:
    image: mongo:latest
    ports:
      - "27017:27017"
    volumes:
      - mongodb_data:/data/db

volumes:
  mongodb_data:
```

```bash
docker-compose up -d
```

## 📚 API Documentation

Once running, visit:
- **Interactive API Docs**: `http://localhost:8000/docs`
- **ReDoc Documentation**: `http://localhost:8000/redoc`

### Key Endpoints

#### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login and get tokens
- `POST /auth/refresh` - Refresh access token
- `GET /auth/me` - Get current user info

#### Analysis
- `POST /analyze/image` - Analyze image for AI detection
- `POST /analyze/pdf` - Analyze PDF for AI-generated content
- `POST /analyze/dataset/upload` - Upload training dataset archive
- `GET /analyze/datasets` - List available datasets

#### History
- `GET /history` - Get analysis history with pagination
- `GET /history/image/{id}` - Get detailed image analysis
- `GET /history/pdf/{id}` - Get detailed PDF analysis
- `DELETE /history/image/{id}` - Delete image analysis
- `DELETE /history/pdf/{id}` - Delete PDF analysis

## 🤖 Training Custom Models

### Prepare Training Data

1. **Organize your dataset** in this structure:
```
dataset/
├── authentic/
│   ├── image1.jpg
│   ├── image2.png
│   └── ...
├── ai_generated/
│   ├── ai_image1.jpg
│   ├── ai_image2.png
│   └── ...
└── manipulated/
    ├── edited1.jpg
    ├── edited2.png
    └── ...
```

2. **Create archive** (ZIP, RAR, 7Z, or TAR)
```bash
zip -r my_dataset.zip dataset/
```

3. **Upload via API** (Pro users only)
```bash
curl -X POST "http://localhost:8000/analyze/dataset/upload" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "file=@my_dataset.zip" \
  -F "name=my_custom_dataset" \
  -F "description=Custom dataset for AI detection"
```

### Train Model

```bash
cd ml
python train.py --dataset my_custom_dataset --epochs 50 --batch_size 32
```

Or extract from archive directly:
```bash
python train.py --archive /path/to/dataset.zip --dataset my_dataset --epochs 50
```

### Training Features
- **Automatic data splitting** (80% train, 10% val, 10% test)
- **Data augmentation** (rotation, flip, color jitter)
- **Transfer learning** with ResNet50
- **Early stopping** and learning rate scheduling
- **Comprehensive evaluation** with confusion matrix
- **Training visualization** plots

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DEBUG` | Enable debug mode | `False` |
| `SECRET_KEY` | JWT secret key | Required |
| `MONGODB_URL` | MongoDB connection string | `mongodb://localhost:27017` |
| `DATABASE_NAME` | Database name | `ai_verification_db` |
| `MAX_FILE_SIZE` | Max upload size (bytes) | `52428800` (50MB) |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiry | `30` |

### Model Configuration

- **Image Size**: 224x224 pixels
- **Batch Size**: 32 (configurable)
- **Architecture**: ResNet50 + custom classifier
- **Classes**: authentic, ai_generated, manipulated

## 🚀 Deployment

### Railway Deployment

1. **Connect GitHub repository** to Railway
2. **Set environment variables**:
```
SECRET_KEY=your-generated-secret-key
MONGODB_URL=mongodb+srv://user:pass@cluster.mongodb.net/dbname
DEBUG=False
```
3. **Deploy automatically** on push

### Render Deployment

1. **Create new Web Service** from GitHub
2. **Build Command**: `pip install -r requirements.txt`
3. **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. **Set environment variables** in dashboard

### AWS/GCP Deployment

Use the provided Dockerfile with your preferred container service:
- AWS ECS/Fargate
- Google Cloud Run
- Azure Container Instances

## 🧪 Testing

```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run tests
pytest tests/

# Run with coverage
pytest --cov=app tests/
```

## 📊 Monitoring and Logging

The application includes:
- **Structured logging** with timestamps
- **API usage tracking** in database
- **Health check endpoints** (`/health`)
- **Error handling** with proper HTTP status codes
- **Request/response logging**

## 🔒 Security Features

- **JWT Authentication** with access/refresh tokens
- **Password hashing** with bcrypt
- **File type validation** and size limits
- **CORS configuration**
- **Input validation** with Pydantic
- **SQL injection prevention** (NoSQL)
- **No hardcoded secrets**

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Check the API documentation at `/docs`
- Review the logs for error details

## 🔄 Version History

- **v1.0.0** - Initial release with core functionality
  - Image AI detection
  - PDF content analysis
  - User authentication
  - Training pipeline
  - Archive extraction
  - Docker deployment