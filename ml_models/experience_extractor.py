"""
Experience Extractor Module
Extracts and analyzes work experience from resume text
"""

import re
from typing import Dict, List, Any
from datetime import datetime


class ExperienceExtractor:
    """Extract and analyze work experience from resume text"""
    
    def __init__(self):
        self.job_titles = [
            "developer", "engineer", "analyst", "manager", "architect",
            "designer", "scientist", "consultant", "director", "specialist",
            "coordinator", "associate", "senior", "lead", "principal"
        ]
        
        self.years_pattern = r'\b(\d{1,2})\s*(?:years?|yrs?)\b'
        self.month_pattern = r'\b(\d{1,2})\s*(?:months?|mos?)\b'
        self.date_pattern = r'\b(\d{1,2})[/-](\d{1,2})[/-](\d{2,4})\b'
    
    def extract_years_of_experience(self, text: str) -> int:
        """
        Extract total years of experience from text
        
        Args:
            text: Resume text
            
        Returns:
            Estimated years of experience
        """
        # Look for explicit years mentioned
        years_matches = re.findall(self.years_pattern, text, re.IGNORECASE)
        
        if years_matches:
            try:
                # Get the maximum year mentioned (usually total experience)
                return max(int(y) for y in years_matches)
            except (ValueError, AttributeError):
                pass
        
        # Look for employment dates
        dates = re.findall(self.date_pattern, text)
        if len(dates) >= 2:
            try:
                # Estimate from date ranges
                earliest_year = min(int(d[2]) if len(d[2]) == 4 else 2000 + int(d[2]) for d in dates)
                current_year = datetime.now().year
                return max(0, current_year - earliest_year)
            except (ValueError, IndexError):
                pass
        
        # Default estimation based on experience keywords
        if re.search(r'\b(senior|sr|lead|principal)\b', text, re.IGNORECASE):
            return 8
        elif re.search(r'\b(mid|middle|intermediate)\b', text, re.IGNORECASE):
            return 5
        elif re.search(r'\b(junior|jr|entry)\b', text, re.IGNORECASE):
            return 2
        
        return 1  # Default
    
    def extract_job_titles(self, text: str) -> List[str]:
        """
        Extract job titles from resume text
        
        Args:
            text: Resume text
            
        Returns:
            List of found job titles
        """
        found_titles = []
        text_lower = text.lower()
        
        for title in self.job_titles:
            pattern = r'\b' + re.escape(title) + r'\b'
            if re.search(pattern, text_lower):
                found_titles.append(title.title())
        
        return list(set(found_titles))  # Remove duplicates
    
    def extract_companies(self, text: str) -> List[str]:
        """
        Extract likely company names from resume text
        
        Args:
            text: Resume text
            
        Returns:
            List of potential company names
        """
        # Look for company-like patterns (e.g., "Company Name, Inc.")
        # This is a simplified extraction
        companies = []
        
        # Patterns for company mentions
        patterns = [
            r'(?:at|@|worked at|company|employer|organization)[\s:]*([A-Z][A-Za-z\s&.,]*(?:Inc|LLC|Ltd|Corp|Company)?)',
            r'^([A-Z][A-Za-z\s&.,]*(?:Inc|LLC|Ltd|Corp|Company)?)$'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text, re.MULTILINE)
            companies.extend(matches)
        
        # Clean and filter
        companies = [c.strip() for c in companies if len(c.strip()) > 2]
        return list(set(companies))[:5]  # Return unique, top 5
    
    def calculate_experience_level(self, years: int, skills_count: int) -> str:
        """
        Calculate experience level based on years and skills
        
        Args:
            years: Years of experience
            skills_count: Number of skills listed
            
        Returns:
            Experience level: 'entry', 'junior', 'mid', 'senior'
        """
        if years < 1:
            return "entry"
        elif years < 3:
            if skills_count < 3:
                return "junior"
            return "entry"
        elif years < 6:
            return "mid"
        else:
            return "senior"
    
    def analyze_experience(self, resume_text: str, skills: List[str]) -> Dict[str, Any]:
        """
        Analyze and extract comprehensive experience information
        
        Args:
            resume_text: Full resume text
            skills: List of extracted skills
            
        Returns:
            Dictionary with experience analysis
        """
        years = self.extract_years_of_experience(resume_text)
        job_titles = self.extract_job_titles(resume_text)
        companies = self.extract_companies(resume_text)
        exp_level = self.calculate_experience_level(years, len(skills))
        
        return {
            "years_of_experience": years,
            "job_titles": job_titles,
            "companies": companies,
            "experience_level": exp_level,
            "skills_count": len(skills),
            "is_relevant_experience": any(title.lower() in ["developer", "engineer", "analyst"] 
                                         for title in job_titles)
        }
