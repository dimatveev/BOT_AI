from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from ..fsm.states import CVForm
from ..keyboards.main_menu import get_main_keyboard

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    await state.clear()
    
    welcome_text = (
        "👋 Welcome to the Resume Generator Bot!\n\n"
        "I will help you create a professional resume in PDF format.\n"
        "Click the button below to start filling out the form."
    )
    
    await message.answer(
        welcome_text,
        reply_markup=get_main_keyboard()
    ) 