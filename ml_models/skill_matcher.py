"""
Skill Matcher Module
Compares resume skills against job requirements and calculates match scores
"""

from typing import List, Dict, Tuple
import re


class SkillMatcher:
    """Match candidate skills with job requirements"""
    
    def __init__(self):
        # Skill categories for better matching
        self.skill_categories = {
            "programming_languages": [
                "python", "javascript", "java", "c++", "c#", "ruby", "php", "go",
                "rust", "kotlin", "swift", "typescript", "r", "matlab", "scala"
            ],
            "web_frameworks": [
                "react", "vue", "angular", "node.js", "express", "django", "flask",
                "spring", "asp.net", "jquery", "bootstrap"
            ],
            "databases": [
                "sql", "mysql", "postgresql", "mongodb", "redis", "elasticsearch",
                "dynamodb", "cassandra", "oracle", "firebase"
            ],
            "cloud_devops": [
                "aws", "azure", "gcp", "docker", "kubernetes", "jenkins",
                "gitlab", "github", "terraform", "ansible"
            ],
            "data_ml": [
                "machine learning", "deep learning", "tensorflow", "pytorch",
                "scikit-learn", "pandas", "numpy", "spark", "hadoop"
            ]
        }
    
    def normalize_skill(self, skill: str) -> str:
        """Normalize skill name for comparison"""
        return skill.lower().strip()
    
    def calculate_similarity(self, skill1: str, skill2: str) -> float:
        """
        Calculate similarity between two skills (0.0 to 1.0)
        Uses multiple matching strategies
        """
        s1 = self.normalize_skill(skill1)
        s2 = self.normalize_skill(skill2)
        
        # Exact match
        if s1 == s2:
            return 1.0
        
        # Partial match
        if s1 in s2 or s2 in s1:
            return 0.8
        
        # Levenshtein-like simple distance
        longer = max(len(s1), len(s2))
        if longer == 0:
            return 0.0
        
        # Count matching characters
        matches = sum(c1 == c2 for c1, c2 in zip(s1, s2))
        return matches / longer
    
    def find_matching_skills(self, resume_skills: List[str], 
                            job_skills: List[str], 
                            threshold: float = 0.7) -> Dict[str, List[str]]:
        """
        Find matching skills between resume and job
        
        Args:
            resume_skills: List of skills from resume
            job_skills: List of required skills for job
            threshold: Minimum similarity score (0.0-1.0)
            
        Returns:
            Dictionary with matched and missing skills
        """
        matched = []
        missing = []
        
        resume_skills_norm = [self.normalize_skill(s) for s in resume_skills]
        
        for job_skill in job_skills:
            job_skill_norm = self.normalize_skill(job_skill)
            best_match = False
            
            for resume_skill in resume_skills_norm:
                similarity = self.calculate_similarity(resume_skill, job_skill_norm)
                if similarity >= threshold:
                    matched.append(job_skill)
                    best_match = True
                    break
            
            if not best_match:
                missing.append(job_skill)
        
        return {
            "matched": list(set(matched)),
            "missing": list(set(missing))
        }
    
    def calculate_match_score(self, resume_skills: List[str], 
                             job_skills: List[str]) -> Tuple[int, Dict[str, any]]:
        """
        Calculate overall match score between resume and job
        
        Args:
            resume_skills: List of skills from resume
            job_skills: List of required skills for job
            
        Returns:
            Tuple of (score: 0-100, details: dict)
        """
        if not job_skills:
            return (100, {"matched": resume_skills, "missing": []})
        
        match_info = self.find_matching_skills(resume_skills, job_skills)
        matched_count = len(match_info["matched"])
        required_count = len(job_skills)
        
        # Calculate base score
        if required_count == 0:
            base_score = 100
        else:
            base_score = int((matched_count / required_count) * 100)
        
        # Bonus for additional skills
        extra_skills = len(resume_skills) - matched_count
        bonus = min(extra_skills * 2, 10)  # Max 10% bonus
        
        final_score = min(base_score + bonus, 100)
        
        return (final_score, {
            "matched_count": matched_count,
            "required_count": required_count,
            "matched_skills": match_info["matched"],
            "missing_skills": match_info["missing"],
            "extra_skills": extra_skills
        })
    
    def generate_recommendations(self, missing_skills: List[str], 
                                experience_level: str) -> List[str]:
        """
        Generate recommendations based on missing skills and experience level
        
        Args:
            missing_skills: List of skills not in resume
            experience_level: Current experience level
            
        Returns:
            List of recommendation strings
        """
        recommendations = []
        
        # Prioritize missing skills
        if missing_skills:
            top_missing = missing_skills[:3]  # Top 3 missing skills
            recommendations.append(
                f"Learn these key skills: {', '.join(top_missing)}"
            )
        
        # Experience-based recommendations
        if experience_level == "junior" or experience_level == "entry":
            recommendations.append(
                "Build real-world projects to gain practical experience"
            )
            recommendations.append(
                "Consider internships or junior developer positions"
            )
        elif experience_level == "mid":
            recommendations.append(
                "Lead projects or mentor junior developers to advance"
            )
            recommendations.append(
                "Develop expertise in specialized areas"
            )
        else:  # senior
            recommendations.append(
                "Consider architect or leadership roles"
            )
            recommendations.append(
                "Mentor team members and improve soft skills"
            )
        
        # General recommendations
        recommendations.extend([
            "Build a portfolio showcasing your best work",
            "Network with professionals in target industry",
            "Keep learning and stay updated with trends"
        ])
        
        return recommendations[:5]  # Return top 5 recommendations
