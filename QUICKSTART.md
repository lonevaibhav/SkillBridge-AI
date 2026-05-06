# SkillBridge AI - Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Prerequisites
- Python 3.10+ 
- Node.js 18+
- Docker & Docker Compose (optional, for easy local setup)
- Git

### Option 1: Quick Start with Docker (Recommended)

```bash
# Clone/navigate to project
cd SkillBridge-AI

# Start all services
docker-compose up

# In another terminal, pull Ollama model
docker exec skillbridge_ollama ollama pull mistral

# Access:
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# Swagger Docs: http://localhost:8000/docs
```

### Option 2: Manual Setup

#### 1. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Update .env with your configuration
# For local development, you can keep defaults

# Start MongoDB (separate terminal)
# If you have MongoDB installed locally:
mongod

# Start Ollama (separate terminal)
ollama serve

# In yet another terminal, pull Mistral model
ollama pull mistral

# Run backend (in backend directory with venv activated)
uvicorn main:app --reload

# Backend is now at http://localhost:8000
# API Docs at http://localhost:8000/docs
```

#### 2. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Create .env.local
cp .env.example .env.local

# Start development server
npm run dev

# Frontend is now at http://localhost:5173
```

---

## 📋 Project Structure Overview

```
SkillBridge-AI/
├── backend/                 # FastAPI application
│   ├── main.py             # Entry point
│   ├── config.py           # Configuration
│   ├── requirements.txt     # Dependencies
│   ├── Dockerfile          # Docker setup
│   ├── models/             # Pydantic models
│   ├── routes/             # API routes
│   ├── services/           # Business logic
│   ├── ml/                 # ML/AI components
│   └── data/               # Data files
│
├── frontend/               # Next.js application
│   ├── app/               # App router
│   ├── components/        # React components
│   ├── lib/               # Utilities
│   ├── public/            # Static files
│   └── package.json       # Dependencies
│
├── ml_models/             # Pre-trained models
├── docs/                  # Documentation
├── docker-compose.yml     # Docker Compose config
├── README.md              # Project overview
└── BUILDPLAN.md          # Detailed build plan
```

---

## 🎯 First Tasks

### 1. Set up Backend ✅
```bash
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

**Test:** Open http://localhost:8000/health (after running with uvicorn)

### 2. Start MongoDB
```bash
# Option A: Using Docker
docker run -d -p 27017:27017 -e MONGO_INITDB_ROOT_USERNAME=admin -e MONGO_INITDB_ROOT_PASSWORD=password mongo:7.0

# Option B: Using system MongoDB
mongod
```

### 3. Start Ollama
```bash
# Download and run Ollama from https://ollama.ai
ollama serve

# In another terminal:
ollama pull mistral
```

### 4. Set up Frontend
```bash
cd frontend
npm install
npm run dev
```

---

## 🧪 Test the Setup

### Access Your Application
```bash
# Frontend: http://localhost:5173
# Backend API: http://localhost:8000
# API Swagger Docs: http://localhost:8000/docs
```

### Quick Backend Test (with Python)
```python
import requests

# Test API
response = requests.get("http://localhost:8000/health")
print(response.json())
```

---

## 📚 Next Steps

1. **Read BUILDPLAN.md** - Detailed phase-by-phase implementation guide
2. **Review API Design** - Check backend/routes structure
3. **Check UI Mockups** - See planned components in frontend/
4. **Start Phase 1** - Backend foundation

---

## 🆘 Troubleshooting

### Port Already in Use
```bash
# Find what's using port
# Linux/Mac:
lsof -i :8000

# Windows:
netstat -ano | findstr :8000

# Kill the process or use different port
```

### Ollama Connection Error
```bash
# Make sure Ollama is running
ollama serve

# Test Ollama
curl http://localhost:11434/api/tags
```

### MongoDB Connection Error
```bash
# Check MongoDB is running
# If using Docker:
docker ps | grep mongo

# If using local MongoDB:
mongosh  # Should connect successfully
```

### Dependencies Not Installing
```bash
# Try upgrading pip
pip install --upgrade pip

# If still issues, use specific Python version
# Python 3.10 or 3.11 recommended
python --version
```

---

## 📖 Development Commands

```bash
# Backend
cd backend
uvicorn main:app --reload          # Start with auto-reload
uvicorn main:app --host 0.0.0.0   # Accessible from other machines

# Frontend
cd frontend
npm run dev                         # Development server (port 5173)
npm run build                       # Production build
npm run preview                     # Preview production build

# Docker
docker-compose up                   # Start all services
docker-compose down                 # Stop all services
docker-compose logs -f backend     # View backend logs
docker exec skillbridge_ollama ollama pull <model>  # Pull different LLM
```

---

## 🚀 Ready to Code?

1. Start with **Phase 1** in BUILDPLAN.md
2. Create the database models first
3. Build the resume parser
4. Then connect everything

**Good luck! 🎉**
