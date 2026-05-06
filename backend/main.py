from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from pydantic import BaseModel
from typing import List, Dict, Any
import json
import sys
import os

# Add ml_models to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Import ML models
from ml_models.resume_parser import ResumeParser
from ml_models.skill_matcher import SkillMatcher
from ml_models.experience_extractor import ExperienceExtractor

# Ollama local LLM integration
from ollama_client import OllamaClient

# Import routes (will create these)
# from routes import auth, resumes, jobs, analyses

from config import get_settings

settings = get_settings()

# Initialize ML modules
resume_parser = ResumeParser()
skill_matcher = SkillMatcher()
experience_extractor = ExperienceExtractor()
ollama_client = OllamaClient()

# Pydantic models for API
class SkillsRequest(BaseModel):
    skills: str

class JobMatchRequest(BaseModel):
    job_title: str

class JobCreateRequest(BaseModel):
    title: str
    description: str
    required_skills: List[str] = []
    salary_range: str = "Not specified"

class SkillsResponse(BaseModel):
    skills: List[str]
    analysis: Dict[str, Any]

class JobMatchResponse(BaseModel):
    job_title: str
    matches: List[Dict[str, Any]]
    recommendations: List[str]

class ResumeUploadResponse(BaseModel):
    resume_id: str
    filename: str
    message: str

class JobCreateResponse(BaseModel):
    job_id: str
    title: str
    message: str

class OllamaRequest(BaseModel):
    prompt: str
    max_tokens: int = 250
    temperature: float = 0.7

class OllamaResponse(BaseModel):
    output: str

# In-memory storage for demo (replace with MongoDB in production)
resumes_db: Dict[str, Dict[str, Any]] = {}
jobs_db: Dict[str, Dict[str, Any]] = {}
resume_counter = 0
job_counter = 0

# Lifespan context manager for startup/shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("SkillBridge AI Backend Starting...")
    print(f"Debug mode: {settings.DEBUG}")
    
    yield
    
    # Shutdown
    print("SkillBridge AI Backend Shutting Down...")

# Initialize FastAPI app
app = FastAPI(
    title="SkillBridge AI API",
    description="AI-powered Career & Placement Assistant",
    version="0.1.0",
    lifespan=lifespan
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
# app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
# app.include_router(resumes.router, prefix="/api/resumes", tags=["Resumes"])
# app.include_router(jobs.router, prefix="/api/jobs", tags=["Jobs"])
# app.include_router(analyses.router, prefix="/api/analyses", tags=["Analysis"])

@app.get("/", tags=["Root"])
async def root():
    """Welcome endpoint"""
    return {
        "message": "Welcome to SkillBridge AI",
        "version": "0.1.0",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "SkillBridge AI Backend",
        "version": "0.1.0"
    }

@app.post("/api/analyze-skills", response_model=SkillsResponse, tags=["Analysis"])
async def analyze_skills(request: SkillsRequest):
    """Analyze user skills and provide insights"""
    try:
        # Parse skills from input
        skills_list = [skill.strip() for skill in request.skills.split(',') if skill.strip()]
        
        # Basic analysis (placeholder for ML processing)
        # Generate an enhanced skills analysis with Ollama
        prompt = (
            "You are an expert career coach. "
            "Analyze the following skills list and provide: categories, key strengths, gaps, and recommendations. "
            f"Skills: {', '.join(skills_list)}\n"
            "Return the result as a concise JSON object with keys categories, strengths, gaps, and recommendations."
        )

        try:
            raw_output = ollama_client.generate_completion(
                prompt=prompt,
                max_tokens=250,
                temperature=0.7
            )
            analysis = {
                "skills_count": len(skills_list),
                "raw_analysis": raw_output
            }
        except Exception:
            analysis = {
                "total_skills": len(skills_list),
                "categories": ["Technical", "Soft Skills", "Domain Knowledge"],
                "strengths": ["Problem Solving", "Communication"],
                "gaps": ["Advanced ML", "Cloud Architecture"],
                "note": "Ollama integration unavailable, returned fallback analysis."
            }

        return SkillsResponse(skills=skills_list, analysis=analysis)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.post("/api/match-job", response_model=JobMatchResponse, tags=["Jobs"])
async def match_job(request: JobMatchRequest):
    """Find job matches based on desired job title"""
    try:
        # Mock job matching results with match scores
        matches = [
            {
                "title": f"Senior {request.job_title}",
                "company": "Tech Corp",
                "match_score": 85,
                "required_skills": ["Python", "React", "AWS"],
                "salary_range": "$120k - $150k"
            },
            {
                "title": f"{request.job_title} Developer",
                "company": "Startup Inc",
                "match_score": 78,
                "required_skills": ["JavaScript", "Node.js", "MongoDB"],
                "salary_range": "$90k - $120k"
            },
            {
                "title": f"Mid-level {request.job_title}",
                "company": "Innovation Labs",
                "match_score": 72,
                "required_skills": ["Java", "Spring Boot", "Docker"],
                "salary_range": "$100k - $130k"
            }
        ]
        
        recommendations = [
            "Consider learning advanced cloud technologies",
            "Build a portfolio showcasing relevant projects",
            "Network with professionals in this field"
        ]
        
        return JobMatchResponse(
            job_title=request.job_title,
            matches=matches,
            recommendations=recommendations
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Job matching failed: {str(e)}")

@app.post("/api/resumes/upload", response_model=ResumeUploadResponse, tags=["Resumes"])
async def upload_resume(file: UploadFile = File(...)):
    """Upload and parse a resume"""
    try:
        global resume_counter
        resume_counter += 1
        resume_id = f"resume_{resume_counter}"
        
        content = await file.read()
        
        # Parse resume using ML model
        try:
            parsed_resume = resume_parser.parse_resume(content, file.filename)
        except Exception as parse_error:
            # If parsing fails, still store basic info
            parsed_resume = {
                "text": "",
                "skills": [],
                "experience_level": "entry",
                "email": "",
                "phone": "",
                "total_skills": 0,
                "parse_error": str(parse_error)
            }
        
        # Extract experience information
        try:
            experience_info = experience_extractor.analyze_experience(
                parsed_resume.get("text", ""),
                parsed_resume.get("skills", [])
            )
        except Exception:
            experience_info = {
                "years_of_experience": 0,
                "job_titles": [],
                "companies": [],
                "experience_level": "entry",
                "skills_count": len(parsed_resume.get("skills", [])),
                "is_relevant_experience": False
            }
        
        # Store resume data in memory (in production, save to MongoDB or cloud storage)
        resumes_db[resume_id] = {
            "filename": file.filename,
            "size": len(content),
            "content_type": file.content_type,
            "skills": parsed_resume.get("skills", []),
            "experience_level": experience_info.get("experience_level", "entry"),
            "years_of_experience": experience_info.get("years_of_experience", 0),
            "job_titles": experience_info.get("job_titles", []),
            "email": parsed_resume.get("email", ""),
            "total_skills": len(parsed_resume.get("skills", []))
        }
        
        return ResumeUploadResponse(
            resume_id=resume_id,
            filename=file.filename,
            message=f"Resume uploaded and parsed successfully. Found {resumes_db[resume_id]['total_skills']} skills."
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Resume upload failed: {str(e)}")

@app.post("/api/jobs/create", response_model=JobCreateResponse, tags=["Jobs"])
async def create_job(request: JobCreateRequest):
    """Create a new job posting"""
    try:
        global job_counter
        job_counter += 1
        job_id = f"job_{job_counter}"
        
        # Store job in memory (in production, save to MongoDB)
        jobs_db[job_id] = {
            "title": request.title,
            "description": request.description,
            "required_skills": request.required_skills,
            "salary_range": request.salary_range
        }
        
        return JobCreateResponse(
            job_id=job_id,
            title=request.title,
            message=f"Job created successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Job creation failed: {str(e)}")

@app.post("/api/ollama/generate", response_model=OllamaResponse, tags=["Ollama"])
async def ollama_generate(request: OllamaRequest):
    """Generate text with Ollama from a custom prompt."""
    try:
        output = ollama_client.generate_completion(
            prompt=request.prompt,
            max_tokens=request.max_tokens,
            temperature=request.temperature,
        )
        return OllamaResponse(output=output)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ollama generation failed: {str(e)}")

@app.post("/api/analyze", tags=["Analysis"])
async def analyze_resume(resume_id: str, job_id: str):
    """Analyze resume against a job and calculate match score"""
    try:
        if resume_id not in resumes_db:
            raise HTTPException(status_code=404, detail="Resume not found")
        if job_id not in jobs_db:
            raise HTTPException(status_code=404, detail="Job not found")
        
        resume = resumes_db[resume_id]
        job = jobs_db[job_id]
        
        # Get skills from both resume and job
        resume_skills = resume.get("skills", [])
        job_skills = job.get("required_skills", [])
        
        # Calculate match score using ML model
        match_score, match_details = skill_matcher.calculate_match_score(
            resume_skills, 
            job_skills
        )
        
        # Generate recommendations
        recommendations = skill_matcher.generate_recommendations(
            match_details.get("missing_skills", []),
            resume.get("experience_level", "entry")
        )
        
        # Prepare feedback
        feedback = [
            f"Match score: {match_score}% based on skill overlap",
        ]
        
        if match_details.get("matched_count", 0) > 0:
            feedback.append(
                f"Great! You have {match_details['matched_count']} of {match_details['required_count']} required skills"
            )
        else:
            feedback.append(
                f"You're missing key skills for this role. Consider learning the required skills."
            )
        
        if resume.get("years_of_experience", 0) > 0:
            feedback.append(
                f"Your {resume['years_of_experience']} years of experience is valuable for this role"
            )
        
        return {
            "resume_id": resume_id,
            "job_id": job_id,
            "job_title": job["title"],
            "match_score": match_score,
            "feedback": feedback,
            "matched_skills": match_details.get("matched_skills", []),
            "missing_skills": match_details.get("missing_skills", []),
            "recommendations": recommendations,
            "candidate_skills": resume_skills,
            "experience_level": resume.get("experience_level", "entry"),
            "years_of_experience": resume.get("years_of_experience", 0)
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG
    )
