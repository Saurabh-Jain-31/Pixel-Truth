# 🎯 Pixel-Truth GDG - AI Image Authenticity Verification Platform

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18+-blue.svg)](https://reactjs.org)
[![MongoDB](https://img.shields.io/badge/MongoDB-6.0+-green.svg)](https://mongodb.com)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.0+-red.svg)](https://pytorch.org)

A comprehensive AI-powered platform for detecting AI-generated and manipulated images using advanced machine learning models and OSINT (Open Source Intelligence) analysis.

## 🌟 Features

### 🤖 AI Detection
- **Advanced CNN Model**: ResNet50-based architecture with custom classification head
- **3-Class Classification**: Authentic, AI-Generated, Manipulated
- **Real-time Analysis**: Fast inference with confidence scores
- **Model Versioning**: Tracked model versions and performance metrics

### 🔍 OSINT Analysis
- **EXIF Metadata Extraction**: Complete metadata analysis
- **Anomaly Detection**: Suspicious patterns and missing information
- **Quality Metrics**: Sharpness, noise, contrast, edge density analysis
- **Authenticity Scoring**: Quantified authenticity assessment

### 🗄️ Database Integration
- **MongoDB**: Persistent storage for all analyses
- **User Management**: Account system with usage tracking
- **Analysis History**: Complete audit trail of all detections
- **Statistics Dashboard**: Real-time analytics and insights

### 🌐 Modern Web Interface
- **React Frontend**: Responsive, modern UI/UX
- **Real-time Updates**: Live analysis progress and results
- **Interactive Dashboard**: Comprehensive analytics and history
- **Mobile Responsive**: Works on all devices

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+
- MongoDB 6.0+
- Git

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/Saurabh-Jain-31/Pixel-Truth-GDG.git
cd Pixel-Truth-GDG
```

2. **Backend Setup**
```bash
cd backend
pip install -r requirements.txt
```

3. **Frontend Setup**
```bash
# Frontend is integrated in backend directory
npm install
```

4. **Database Setup**
```bash
# Install and start MongoDB
# Windows: Download from https://www.mongodb.com/try/download/community
# Linux: sudo apt-get install mongodb
# macOS: brew install mongodb-community

# Start MongoDB service
mongod
```

5. **Environment Configuration**
```bash
cp backend/.env.example backend/.env
# Edit .env file with your configuration
```

### 🏃‍♂️ Running the Application

#### Development Mode
```bash
# Start both frontend and backend
cd backend
python production_server.py

# In another terminal
npm run dev
```

#### Production Mode
```bash
cd backend
python production_server.py
```

The application will be available at:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5000
- **API Documentation**: http://localhost:5000/docs

## 📁 Project Structure

```
Pixel-Truth-GDG/
├── backend/                    # Backend application
│   ├── app/                   # FastAPI application
│   │   ├── api/              # API endpoints
│   │   ├── core/             # Core configuration
│   │   ├── models/           # Data models
│   │   └── services/         # Business logic
│   ├── ml/                   # Machine learning models
│   │   ├── models/           # Trained model files
│   │   ├── model.py          # Model architecture
│   │   └── train.py          # Training scripts
│   ├── src/                  # Frontend React code
│   │   ├── components/       # React components
│   │   ├── pages/           # Page components
│   │   └── contexts/        # React contexts
│   ├── uploads/             # Uploaded files
│   ├── datasets/            # Training datasets
│   └── tests/               # Test files
├── docs/                    # Documentation
└── scripts/                 # Utility scripts
```

## 🔧 API Endpoints

### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `GET /api/auth/me` - Get current user

### Image Analysis
- `POST /api/upload` - Upload image for analysis
- `POST /api/analysis/analyze` - Analyze uploaded image
- `GET /api/analysis/{id}` - Get specific analysis
- `GET /api/analysis/history` - Get analysis history

### Statistics
- `GET /api/user/stats` - User statistics
- `GET /api/history` - Analysis history

## 🧠 AI Model Details

### Architecture
- **Base Model**: ResNet50 (ImageNet pretrained)
- **Custom Head**: 3-layer classification head with dropout
- **Input Size**: 224x224 RGB images
- **Output Classes**: 3 (authentic, ai_generated, manipulated)

### Training
- **Dataset**: Custom dataset with authentic, AI-generated, and manipulated images
- **Augmentation**: Random crops, flips, rotations, color jittering
- **Optimization**: Adam optimizer with learning rate scheduling
- **Validation**: Stratified train/validation/test split

### Performance
- **Accuracy**: Varies by dataset and class
- **Inference Time**: ~0.1-0.2 seconds per image
- **Confidence Scoring**: Softmax probabilities with metadata adjustment

## 🔍 OSINT Analysis Features

### Metadata Analysis
- **EXIF Data**: Camera info, timestamps, GPS coordinates
- **Anomaly Detection**: Missing or suspicious metadata patterns
- **Software Signatures**: Detection of editing software traces

### Quality Metrics
- **Sharpness**: Laplacian variance analysis
- **Noise Analysis**: Statistical noise distribution
- **Compression**: JPEG compression artifact analysis
- **Edge Density**: Edge detection and analysis

### Authenticity Indicators
- **Metadata Consistency**: Cross-validation of metadata fields
- **Quality Patterns**: Analysis of quality metrics vs. expected ranges
- **Suspicion Scoring**: Quantified authenticity assessment

## 🗄️ Database Schema

### Collections
- **users**: User accounts and preferences
- **image_analyses**: Analysis results and metadata
- **api_logs**: API usage and performance logs

### Indexes
- User email and username (unique)
- Analysis timestamps and user associations
- Performance-optimized queries

## 🧪 Testing

### Backend Tests
```bash
cd backend
python -m pytest tests/
```

### Integration Tests
```bash
python test_production_ai.py
python test_complete_system.py
```

### Frontend Tests
```bash
npm test
```

## 📊 Monitoring and Analytics

### Built-in Analytics
- **Usage Statistics**: Analysis counts and trends
- **Performance Metrics**: Response times and success rates
- **User Analytics**: User behavior and preferences

### Health Monitoring
- **Health Endpoints**: System status and diagnostics
- **Database Monitoring**: Connection status and performance
- **Model Performance**: Inference times and accuracy tracking

## 🔒 Security Features

### Authentication
- **JWT Tokens**: Secure authentication with refresh tokens
- **Password Hashing**: bcrypt password security
- **Rate Limiting**: API rate limiting and abuse prevention

### Data Protection
- **Input Validation**: Comprehensive input sanitization
- **File Security**: Safe file upload and processing
- **Database Security**: Parameterized queries and validation

## 🚀 Deployment

### Docker Deployment
```bash
docker-compose up -d
```

### Cloud Deployment
- **Backend**: Deploy to Render, Railway, or AWS
- **Database**: MongoDB Atlas or self-hosted
- **Frontend**: Vercel, Netlify, or integrated with backend

### Environment Variables
```env
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=pixel_truth_gdg
SECRET_KEY=your-secret-key
DEBUG=false
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 for Python code
- Use ESLint for JavaScript/React code
- Write tests for new features
- Update documentation for API changes

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **GDG Community**: For inspiration and support
- **PyTorch Team**: For the excellent deep learning framework
- **FastAPI**: For the modern, fast web framework
- **React Team**: For the powerful frontend library
- **MongoDB**: For the flexible database solution

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/Saurabh-Jain-31/Pixel-Truth-GDG/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Saurabh-Jain-31/Pixel-Truth-GDG/discussions)
- **Email**: [Contact](mailto:your-email@example.com)

## 🔄 Changelog

### v2.0.0 (Latest)
- ✅ Real AI model integration with ResNet50
- ✅ MongoDB database integration
- ✅ Complete OSINT analysis functions
- ✅ Production-ready backend with comprehensive API
- ✅ Modern React frontend with responsive design
- ✅ Real-time statistics and analytics
- ✅ Comprehensive testing suite

### v1.0.0
- ✅ Basic AI detection functionality
- ✅ Simple web interface
- ✅ Mock data and basic API

---

**Built with ❤️ for the GDG Community**

*Empowering digital authenticity through AI and OSINT analysis*