"""
Resume Parser Module
Extracts text and information from resume files (PDF, DOC, DOCX, TXT)
"""

import re
from typing import Dict, List, Any


class ResumeParser:
    """Parse resume files and extract structured information"""
    
    def __init__(self):
        # Common skills to look for in resumes
        self.common_skills = [
            # Programming Languages
            "python", "javascript", "java", "c++", "c#", "ruby", "php", "go", "rust",
            "kotlin", "swift", "typescript", "r", "matlab", "scala", "groovy",
            
            # Web Technologies
            "html", "css", "react", "vue", "angular", "node.js", "express", "django",
            "flask", "spring", "asp.net", "jquery", "bootstrap", "webpack", "gulp",
            
            # Databases
            "sql", "mysql", "postgresql", "mongodb", "redis", "elasticsearch", "dynamodb",
            "cassandra", "oracle", "firebase", "faiss",
            
            # Cloud & DevOps
            "aws", "azure", "gcp", "docker", "kubernetes", "jenkins", "circleci",
            "gitlab", "github", "terraform", "ansible", "heroku",
            
            # Data & ML
            "machine learning", "deep learning", "tensorflow", "pytorch", "keras",
            "scikit-learn", "pandas", "numpy", "spark", "hadoop", "airflow",
            "data analysis", "data science", "nlp", "computer vision",
            
            # Soft Skills
            "communication", "leadership", "problem solving", "teamwork", "project management",
            "agile", "scrum", "collaboration", "critical thinking", "time management",
        ]
        
        # Common keywords for experience levels
        self.experience_patterns = {
            "senior": r"\b(senior|sr|lead|principal|architect)\b",
            "mid": r"\b(mid|middle|intermediate|mid-level)\b",
            "junior": r"\b(junior|jr|entry|junior developer)\b",
            "intern": r"\b(intern|internship)\b"
        }
    
    def extract_text_from_txt(self, content: bytes) -> str:
        """Extract text from plain text file"""
        try:
            return content.decode('utf-8')
        except UnicodeDecodeError:
            return content.decode('latin-1', errors='ignore')
    
    def extract_text_from_pdf(self, content: bytes) -> str:
        """
        Extract text from PDF file
        Note: Full PDF parsing requires PyPDF2, simplified version below
        """
        try:
            # Basic PDF text extraction - returns placeholder
            # In production, use PyPDF2: PyPDF2.PdfReader(BytesIO(content))
            text = content.decode('latin-1', errors='ignore')
            # Remove binary data and keep readable text
            text = re.sub(r'[^\x20-\x7E\n]', '', text)
            return text
        except Exception:
            return ""
    
    def extract_text_from_docx(self, content: bytes) -> str:
        """
        Extract text from DOCX file
        Note: Full DOCX parsing requires python-docx, simplified version below
        """
        try:
            # Basic DOCX text extraction - returns placeholder
            # In production, use python-docx: Document(BytesIO(content))
            text = content.decode('latin-1', errors='ignore')
            # Remove binary data and keep readable text
            text = re.sub(r'[^\x20-\x7E\n]', '', text)
            return text
        except Exception:
            return ""
    
    def extract_skills(self, text: str) -> List[str]:
        """Extract skills from resume text"""
        text_lower = text.lower()
        found_skills = []
        
        for skill in self.common_skills:
            if re.search(r'\b' + re.escape(skill) + r'\b', text_lower):
                found_skills.append(skill.title())
        
        # Remove duplicates and sort
        return sorted(list(set(found_skills)))
    
    def extract_experience_level(self, text: str) -> str:
        """Determine experience level from resume text"""
        text_lower = text.lower()
        
        for level, pattern in self.experience_patterns.items():
            if re.search(pattern, text_lower):
                return level
        
        return "entry"  # Default to entry level
    
    def extract_email(self, text: str) -> str:
        """Extract email address from resume"""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        matches = re.findall(email_pattern, text)
        return matches[0] if matches else ""
    
    def extract_phone(self, text: str) -> str:
        """Extract phone number from resume"""
        phone_patterns = [
            r'(\+1)?[\s.-]?\(?[0-9]{3}\)?[\s.-]?[0-9]{3}[\s.-]?[0-9]{4}',
            r'\b[0-9]{3}[.-]?[0-9]{3}[.-]?[0-9]{4}\b'
        ]
        
        for pattern in phone_patterns:
            matches = re.findall(pattern, text)
            if matches:
                return matches[0] if isinstance(matches[0], str) else ''.join(matches[0])
        
        return ""
    
    def parse_resume(self, content: bytes, filename: str) -> Dict[str, Any]:
        """
        Parse resume file and extract structured information
        
        Args:
            content: File content as bytes
            filename: Original filename
            
        Returns:
            Dictionary with extracted resume information
        """
        # Extract text based on file type
        file_ext = filename.lower().split('.')[-1]
        
        if file_ext == 'pdf':
            text = self.extract_text_from_pdf(content)
        elif file_ext == 'docx':
            text = self.extract_text_from_docx(content)
        else:  # txt, doc, or other
            text = self.extract_text_from_txt(content)
        
        if not text:
            text = content.decode('latin-1', errors='ignore')
        
        # Extract information
        skills = self.extract_skills(text)
        experience_level = self.extract_experience_level(text)
        email = self.extract_email(text)
        phone = self.extract_phone(text)
        
        return {
            "text": text[:500],  # Store first 500 chars as preview
            "skills": skills,
            "experience_level": experience_level,
            "email": email,
            "phone": phone,
            "total_skills": len(skills)
        }
