# SkillBridge AI - Tech Stack Reference

## 🏗️ Architecture Overview

```
                        USER INTERFACE
                      ┌────────────────┐
                      │  React 18 App  │
                      │   + Vite       │
                      │ TypeScript     │
                      │ Tailwind CSS   │
                      └────────┬────────┘
                               │
                        HTTP/REST API
                               │
                      ┌────────▼────────┐
                      │    FastAPI      │
                      │   Python 3.11   │
                      └────────┬────────┘
                               │
        ┌──────────────────────┼──────────────────────┐
        │                      │                      │
        ▼                      ▼                      ▼
   ┌─────────┐         ┌──────────────┐      ┌──────────────┐
   │ MongoDB │         │   Ollama     │      │ FAISS Store  │
   │(Persist)│         │(Local LLM)   │      │(Vector DB)   │
   └─────────┘         └──────────────┘      └──────────────┘
```

## 🎯 Component Breakdown

### Frontend (React 18 + Vite)
| Component | Purpose |
|-----------|----------|
| React Router | Client-side routing |
| React Components | Reusable UI elements |
| TypeScript | Type-safe development |
| Tailwind CSS | Utility-first styling |
| Vite | Ultra-fast build tool & dev server |

### Backend (FastAPI)
| Component | Purpose |
|-----------|---------|
| FastAPI Framework | Modern async web framework |
| Pydantic | Data validation & serialization |
| Motor | Async MongoDB driver |
| Python 3.11 | Latest stable Python features |
| CORS | Cross-Origin Resource Sharing |

### AI/ML Layer
| Component | Purpose |
|-----------|---------|
| Sentence Transformers | Convert text to embeddings |
| FAISS | Efficient similarity search |
| Ollama + Mistral | Local LLM for text generation |
| PyPDF2 | PDF text extraction |
| Scikit-learn | ML algorithms & preprocessing |

### Data Layer
| Component | Purpose |
|-----------|---------|
| MongoDB | NoSQL database (flexible schema) |
| FAISS Index | Vector search index |
| Ollama Models | Local LLM weights |

## 📊 Data Flow Example

### Resume Analysis Request
```
User Input
  ├─ Resume PDF
  └─ Job Description Text
         ↓
    Frontend (Next.js)
    ├─ Form validation
    └─ API call
         ↓
    Backend (FastAPI)
    ├─ Receive files
    ├─ Validate input
    └─ Route to analysis
         ↓
    ML Pipeline
    ├─ Extract resume text (PyPDF2)
    ├─ Extract job description
    ├─ Generate embeddings (Sentence Transformers)
    ├─ Search FAISS index
    ├─ Query Ollama for text generation
    └─ Score & rank
         ↓
    Database (MongoDB)
    ├─ Store analysis result
    └─ Store user data
         ↓
    Response to Frontend
    ├─ Match score
    ├─ Missing skills
    ├─ Recommendations
    └─ Learning roadmap
         ↓
    Frontend Display
    └─ Show results in dashboard
```

## 🔑 Key Technologies & Why

| Tech | Why Chosen | Benefit |
|------|-----------|---------|
| **React 18 + Vite** | Modern lightweight stack | Fast dev server, optimal bundling, SPA flexibility |
| **FastAPI** | Modern Python framework | Async, automatic validation, great docs |
| **Sentence Transformers** | Specialized embeddings | Quality text representations |
| **FAISS** | Meta's vector search | Extremely fast similarity search |
| **Ollama** | Local LLM | No API costs, privacy, control |
| **MongoDB** | NoSQL flexibility | Easy schema changes, scalable |
| **Docker** | Containerization | Reproducible, portable environments |

## 📦 Dependency Highlights

### Backend (Python)
```
fastapi (0.104.1)           # Web framework
sentence-transformers       # Embeddings model
faiss-cpu (1.7.4)          # Vector search
pymongo / motor            # MongoDB drivers
torch (2.1.1)              # ML framework
scikit-learn (1.3.2)       # ML utilities
PyPDF2 (3.0.1)             # PDF parsing
ollama client              # LLM integration
```

### Frontend (Node.js)
```
vite (5+)                  # Build tool & dev server
react (18+)                # UI library
react-router-dom (6+)      # Client-side routing
typescript                 # Type safety
tailwindcss                # Styling
axios                      # HTTP client
```

## 🚀 Performance Considerations

| Layer | Optimization |
|-------|--------------|
| **Frontend** | Code splitting, image optimization, caching |
| **Backend** | Async operations, connection pooling, caching |
| **AI/ML** | FAISS indexing, batch processing, model caching |
| **Database** | Proper indexing, query optimization |
| **Network** | Compression, CDN for static files |

## 🔒 Security Stack

- **Authentication**: JWT tokens
- **Password Hashing**: Bcrypt via PassLib
- **Input Validation**: Pydantic models
- **File Upload**: Size limits + type checking
- **CORS**: Strict origin configuration
- **HTTPS**: Required in production
- **Environment Variables**: Secret management

## 🐳 Containerization

### Docker Setup
```
├── Backend Container
│   ├── Python 3.11 slim image
│   ├── FastAPI application
│   └── All Python dependencies
├── MongoDB Container
│   └── Data persistence volume
└── Ollama Container
    └── Local LLM model
```

### Docker Compose
- Easy local development
- Service orchestration
- Volume management
- Environment isolation

## 🚢 Deployment Architecture

### Frontend (Vercel)
- Automatic deployments from Git
- Built-in analytics
- Automatic HTTPS
- Global CDN

### Backend (Render/Railway)
- Docker-based deployment
- Environment variables management
- Database connection pooling
- Auto-scaling (Railway)

## 📈 Scalability Path

1. **Phase 1-2 (MVP)**: Local setup with Docker
2. **Phase 3-4**: Deploy backend on Render
3. **Phase 5-6**: Deploy frontend on Vercel
4. **Future**: 
   - Add Redis for caching
   - Use MongoDB Atlas
   - Implement rate limiting
   - Add API versioning

## 🧪 Testing Strategy

- **Backend**: FastAPI TestClient
- **Frontend**: Jest + React Testing Library
- **Integration**: End-to-end tests with Playwright
- **Performance**: Load testing with Locust

---

**This tech stack is chosen for:**
- ✅ Modern development practices
- ✅ Production-ready quality
- ✅ Strong resume appeal
- ✅ Good documentation
- ✅ Active community support
- ✅ Scalability
