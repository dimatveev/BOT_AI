from aiogram.fsm.state import State, StatesGroup

class CVForm(StatesGroup):
    # Personal Information
    full_name = State()
    email = State()
    phone = State()
    location = State()
    
    # Professional Summary
    professional_summary = State()
    
    # Education
    education_degree = State()
    education_institution = State()
    education_year = State()
    education_location = State()
    
    # Work Experience
    experience_company = State()
    experience_position = State()
    experience_period = State()
    experience_location = State()
    experience_description = State()
    
    # Skills
    skills = State()
    
    # Languages
    languages = State()
    
    # Additional Information
    additional_info = State() 