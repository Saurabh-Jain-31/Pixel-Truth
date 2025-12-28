# 🏗️ Full-Stack Project Structure Guide

## Recommended Folder Structure

```
pixel-truth/                    # Root project directory
├── frontend/                   # React.js frontend
│   ├── public/
│   │   ├── index.html
│   │   └── favicon.ico
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/          # API calls
│   │   ├── utils/
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   ├── vite.config.js
│   └── dist/                  # Built frontend files
├── backend/                   # FastAPI backend
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── models/
│   │   ├── services/
│   │   └── main.py
│   ├── ml/
│   ├── requirements.txt
│   └── static/               # Serve frontend from here
├── docs/                     # Documentation
├── docker-compose.yml        # Full-stack deployment
├── .gitignore               # Combined gitignore
├── .gitattributes          # Git LFS configuration
└── README.md               # Project documentation
```

## Benefits of This Structure:
- ✅ Clear separation of concerns
- ✅ Easy development and deployment
- ✅ Backend can serve frontend static files
- ✅ Shared configuration files
- ✅ Docker support for full-stack deployment