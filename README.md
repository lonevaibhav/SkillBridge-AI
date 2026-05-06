# SkillBridge AI - AI Career & Placement Assistant

An intelligent career guidance platform that analyzes resumes against job descriptions and generates personalized skill-gap reports, project recommendations, and interview preparation plans.

## 🎯 Project Overview

**Problem**: Students apply for jobs/internships without knowing:
- If their resume matches the role
- Which skills they're missing
- What projects they should build
- How to prepare for interviews
- How to improve their resume

**Solution**: SkillBridge AI analyzes resume + job description to provide:
- 📊 Resume match score
- 🎯 Missing skills identification
- 📚 Project recommendations
- 📅 Personalized learning roadmap
- 💡 AI-generated interview questions
- ✨ Resume improvement suggestions

## 🏗️ Project Architecture

```
Frontend (Next.js)
    ↓
Backend (FastAPI)
    ↓
├── Resume Parser
├── Embedding Model
├── Vector Database (FAISS)
├── RAG Engine
└── Analysis Engine
    ├── Skill Gap Analysis
    ├── Project Recommender
    ├── Interview Question Generator
    └── Resume Improver
    ↓
Database (MongoDB)
```

## 🛠️ Tech Stack

| Layer | Technologies |
|-------|--------------|
| **Frontend** | React 18, Vite, TypeScript, Tailwind CSS |
| **Backend** | FastAPI, Python, Pydantic |
| **AI/ML** | Sentence Transformers, FAISS, Ollama (Local LLM) |
| **Database** | MongoDB |
| **Deployment** | Docker, Vercel (Frontend), Render/Railway (Backend) |

## 📦 Project Structure

```
SkillBridge-AI/
├── frontend/              # Next.js application
├── backend/               # FastAPI application
├── ml_models/             # Model files & preprocessing
├── docs/                  # Documentation
└── docker-compose.yml     # Local development setup
```

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+
- MongoDB (or MongoDB Atlas)
- Ollama installed locally

### Installation

1. Clone and navigate:
```bash
cd SkillBridge-AI
```

2. Set up backend:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Set up frontend:
```bash
cd ../frontend
npm install
npm run dev
```

4. Start Ollama:
```bash
ollama pull mistral
ollama serve
```

## 🎓 Core Features

| Feature | Description |
|---------|------------|
| **Resume Upload** | PDF resume parsing with text extraction |
| **Job Description Input** | Parse job requirements from text |
| **Match Scoring** | Calculate resume-job match percentage |
| **Skill Gap Analysis** | Identify missing technical skills |
| **Project Recommendations** | AI-suggested projects based on skill gaps |
| **Learning Roadmap** | Week-by-week preparation plan |
| **Interview Questions** | Generated HR & technical questions |
| **Resume Suggestions** | AI-powered resume bullet points |

## 📋 Development Roadmap

### Phase 1: Backend Foundation (Week 1-2)
- [ ] FastAPI project setup
- [ ] MongoDB connection & schemas
- [ ] Resume parsing (PyPDF2)
- [ ] Basic job description parser

### Phase 2: AI/ML Pipeline (Week 2-3)
- [ ] Embedding model integration (Sentence Transformers)
- [ ] FAISS vector store setup
- [ ] Skill extraction & matching
- [ ] Ollama integration for LLM

### Phase 3: Core Analysis Engine (Week 3-4)
- [ ] Resume match scorer
- [ ] Missing skills identifier
- [ ] Project recommender
- [ ] Interview question generator
- [ ] Resume improver

### Phase 4: Frontend (Week 4-5)
- [ ] Next.js project setup
- [ ] UI components (Tailwind CSS)
- [ ] Resume upload interface
- [ ] Dashboard & results display
- [ ] Responsive design

### Phase 5: Integration & Polish (Week 5-6)
- [ ] API integration
- [ ] Error handling & validation
- [ ] Performance optimization
- [ ] Testing

### Phase 6: Deployment (Week 6)
- [ ] Docker setup
- [ ] Vercel deployment (Frontend)
- [ ] Render/Railway deployment (Backend)
- [ ] Documentation

## 📚 Sample Workflow

**Input:**
- Resume: Student with Python, ML, Pandas skills
- Job: AI/ML Intern (Python, FastAPI, NLP, SQL, Deployment)

**Output:**
```
Resume Match Score: 68%
Strong Skills: Python, ML, Pandas
Missing Skills: FastAPI, NLP, SQL, Deployment
Top Projects to Build:
  1. Resume Parser with NLP
  2. Job Recommendation System
  3. ML Model Deployment API
Learning Timeline: 4-week focused track
Interview Questions: 15 generated questions
```

## 🎖️ Resume Impact

**Strong wording for your resume:**

> "Built an AI-powered placement assistant using Retrieval-Augmented Generation (RAG), sentence embeddings, FastAPI, Next.js, and vector search (FAISS) to analyze student resumes against job descriptions and generate personalized skill-gap reports, project recommendations, and interview preparation plans."

## 📖 Documentation

See [docs/](docs/) for:
- API Documentation
- Database Schema
- AI Model Architecture
- Deployment Guide

## 🤝 Contributing

This is an active learning project. Future enhancements:
- LinkedIn profile analysis
- GitHub activity integration
- Real-time job market trends
- Batch resume analysis
- Industry-specific roadmaps

## 📄 License

MIT

---

**Built by**: Vaibhav Singh 
**Last Updated**: May 2026
