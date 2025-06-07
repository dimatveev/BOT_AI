from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from ..fsm.states import CVForm
from ..keyboards.main_menu import get_form_keyboard, get_confirmation_keyboard
from ..models.user_data import UserCV, Education, Experience
from ..storage.db import Database

router = Router()
db = Database()

# Dictionary with questions for each state
QUESTIONS = {
    CVForm.full_name: "Enter your full name:",
    CVForm.email: "Enter your email address:",
    CVForm.phone: "Enter your phone number:",
    CVForm.location: "Enter your current location (city, country):",
    CVForm.professional_summary: "Write a brief professional summary (2-3 sentences):",
    CVForm.education_degree: "Enter your degree/qualification:",
    CVForm.education_institution: "Enter your educational institution:",
    CVForm.education_year: "Enter your graduation year:",
    CVForm.education_location: "Enter the location of your education (city, country):",
    CVForm.experience_company: "Enter company name:",
    CVForm.experience_position: "Enter your position:",
    CVForm.experience_period: "Enter work period (e.g.: 2020-2023):",
    CVForm.experience_location: "Enter the location of your work (city, country):",
    CVForm.experience_description: "Describe your main responsibilities and achievements:",
    CVForm.skills: "List your technical skills (comma-separated):",
    CVForm.languages: "List languages you know with proficiency levels (e.g.: English - B2, Spanish - C1):",
    CVForm.additional_info: "Add additional information (achievements, certifications, etc.):"
}

# Dictionary for state navigation
NEXT_STATE = {
    CVForm.full_name: CVForm.email,
    CVForm.email: CVForm.phone,
    CVForm.phone: CVForm.location,
    CVForm.location: CVForm.professional_summary,
    CVForm.professional_summary: CVForm.education_degree,
    CVForm.education_degree: CVForm.education_institution,
    CVForm.education_institution: CVForm.education_year,
    CVForm.education_year: CVForm.education_location,
    CVForm.education_location: CVForm.experience_company,
    CVForm.experience_company: CVForm.experience_position,
    CVForm.experience_position: CVForm.experience_period,
    CVForm.experience_period: CVForm.experience_location,
    CVForm.experience_location: CVForm.experience_description,
    CVForm.experience_description: CVForm.skills,
    CVForm.skills: CVForm.languages,
    CVForm.languages: CVForm.additional_info,
    CVForm.additional_info: None  # End of form
}

PREV_STATE = {v: k for k, v in NEXT_STATE.items() if v is not None}

# Helper function to get state name
def get_state_name(state):
    """Convert FSM state to database field name."""
    if isinstance(state, str):
        state_name = state
    else:
        state_name = state.state
    
    # Convert state name to database field name
    field_name = state_name.lower()
    if field_name.startswith('cvform:'):
        field_name = field_name[7:]  # Remove 'cvform:' prefix
    elif field_name.startswith('cvform_'):
        field_name = field_name[7:]  # Remove 'cvform_' prefix
    elif field_name.startswith('cvform.'):
        field_name = field_name[7:]  # Remove 'cvform.' prefix
    
    # Map state names to database fields
    field_mapping = {
        'full_name': 'full_name',
        'email': 'email',
        'phone': 'phone',
        'location': 'location',
        'professional_summary': 'professional_summary',
        'education_degree': 'education_degree',
        'education_institution': 'education_institution',
        'education_year': 'education_year',
        'education_location': 'education_location',
        'experience_company': 'experience_company',
        'experience_position': 'experience_position',
        'experience_period': 'experience_period',
        'experience_location': 'experience_location',
        'experience_description': 'experience_description',
        'skills': 'skills',
        'languages': 'languages',
        'additional_info': 'additional_info'
    }
    
    return field_mapping.get(field_name, field_name)

@router.message(F.text == "📝 Start Filling")
async def start_form(message: types.Message, state: FSMContext):
    # Clear old user data
    db.clear_user_data(message.from_user.id)
    await state.clear()
    
    await state.set_state(CVForm.full_name)
    await message.answer(
        QUESTIONS[CVForm.full_name],
        reply_markup=get_form_keyboard()
    )

@router.message(F.text == "❌ Cancel")
async def cancel_form(message: types.Message, state: FSMContext):
    # Delete user data from DB
    db.clear_user_data(message.from_user.id)
    await state.clear()
    await message.answer(
        "Form filling cancelled. To start over, use the /start command",
        reply_markup=types.ReplyKeyboardRemove()
    )

@router.message(F.text == "⬅️ Back")
async def previous_step(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state in PREV_STATE:
        prev_state = PREV_STATE[current_state]
        await state.set_state(prev_state)
        await message.answer(QUESTIONS[prev_state], reply_markup=get_form_keyboard())
    else:
        await message.answer("You are at the first step of the form.")

@router.message(F.text == "➡️ Skip")
async def skip_step(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state == CVForm.additional_info:
        db.update_user_data(message.from_user.id, get_state_name(current_state), "")
        data = db.get_user_data(message.from_user.id)
        await show_summary(message, data)
    elif current_state in NEXT_STATE:
        next_state = NEXT_STATE[current_state]
        if next_state:
            db.update_user_data(message.from_user.id, get_state_name(current_state), "Not specified")
            await state.set_state(next_state)
            await message.answer(QUESTIONS[next_state], reply_markup=get_form_keyboard())
        else:
            data = db.get_user_data(message.from_user.id)
            await show_summary(message, data)

async def process_form_step(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    # Save user's answer to DB
    db.update_user_data(message.from_user.id, get_state_name(current_state), message.text)
    
    if current_state in NEXT_STATE:
        next_state = NEXT_STATE[current_state]
        if next_state:
            await state.set_state(next_state)
            await message.answer(QUESTIONS[next_state], reply_markup=get_form_keyboard())
        else:
            # Form completed
            data = db.get_user_data(message.from_user.id)
            await show_summary(message, data)

async def show_summary(message: types.Message, data: dict):
    summary = "📋 Please review your data:\n\n"
    summary += f"👤 Full Name: {data.get('full_name')}\n"
    summary += f"📧 Email: {data.get('email')}\n"
    summary += f"📱 Phone: {data.get('phone')}\n"
    summary += f"📍 Location: {data.get('location')}\n"
    summary += f"\n💼 Professional Summary:\n{data.get('professional_summary')}\n"
    summary += f"\n📚 Education:\n"
    summary += f"- Degree: {data.get('education_degree')}\n"
    summary += f"- Institution: {data.get('education_institution')}\n"
    summary += f"- Year: {data.get('education_year')}\n"
    summary += f"- Location: {data.get('education_location')}\n"
    summary += f"\n💡 Work Experience:\n"
    summary += f"- Company: {data.get('experience_company')}\n"
    summary += f"- Position: {data.get('experience_position')}\n"
    summary += f"- Period: {data.get('experience_period')}\n"
    summary += f"- Location: {data.get('experience_location')}\n"
    summary += f"- Description: {data.get('experience_description')}\n"
    summary += f"\n🛠 Skills: {data.get('skills')}\n"
    summary += f"🌐 Languages: {data.get('languages')}\n"
    
    if data.get('additional_info'):
        summary += f"\nℹ️ Additional Information:\n{data.get('additional_info')}\n"
    
    await message.answer(
        summary,
        reply_markup=get_confirmation_keyboard()
    )

# Handlers for each state
@router.message(CVForm.full_name)
@router.message(CVForm.email)
@router.message(CVForm.phone)
@router.message(CVForm.location)
@router.message(CVForm.professional_summary)
@router.message(CVForm.education_degree)
@router.message(CVForm.education_institution)
@router.message(CVForm.education_year)
@router.message(CVForm.education_location)
@router.message(CVForm.experience_company)
@router.message(CVForm.experience_position)
@router.message(CVForm.experience_period)
@router.message(CVForm.experience_location)
@router.message(CVForm.experience_description)
@router.message(CVForm.skills)
@router.message(CVForm.languages)
@router.message(CVForm.additional_info)
async def process_any_state(message: types.Message, state: FSMContext):
    await process_form_step(message, state) 