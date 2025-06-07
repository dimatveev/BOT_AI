from pydantic import BaseModel, EmailStr
from typing import List, Optional

class Education(BaseModel):
    degree: str
    institution: str
    year: str

class Experience(BaseModel):
    company: str
    position: str
    period: str
    description: str

class UserCV(BaseModel):
    # Personal Information
    full_name: str
    email: EmailStr
    phone: str
    location: str
    
    # Professional Summary
    professional_summary: str
    
    # Education
    education: Education
    
    # Work Experience
    experience: Experience
    
    # Skills and Languages
    skills: List[str]
    languages: List[str]
    
    # Additional Information
    additional_info: Optional[str] = None 