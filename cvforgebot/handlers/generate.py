from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from ..latex.compiler import LaTeXCompiler
from ..models.user_data import UserCV, Education, Experience
from ..storage.db import Database

router = Router()
latex_compiler = LaTeXCompiler()
db = Database()

@router.callback_query(F.data == "confirm_cv")
async def generate_cv(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    
    # Get form data from database
    data = db.get_user_data(callback.from_user.id)
    
    if not data:
        await callback.message.answer(
            "❌ Form data not found. Please fill out the form again.",
            reply_markup=types.ReplyKeyboardRemove()
        )
        return
    
    try:
        # Generate PDF
        await callback.message.answer("⏳ Generating PDF resume...")
        pdf_path = await latex_compiler.generate_pdf(data, callback.from_user.id)
        
        # Send PDF
        with open(pdf_path, 'rb') as pdf_file:
            await callback.message.answer_document(
                types.FSInputFile(pdf_path, filename=f"resume_{callback.from_user.id}.pdf"),
                caption="✅ Your resume is ready!"
            )
        
        # Cleanup
        latex_compiler.cleanup(callback.from_user.id)
        # Clear form data after successful generation
        db.clear_user_data(callback.from_user.id)
        await state.clear()
        
    except Exception as e:
        await callback.message.answer(
            f"❌ An error occurred while generating PDF: {str(e)}\n"
            "Please try again or contact administrator."
        )
        
@router.callback_query(F.data == "restart_cv")
async def restart_cv(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    # Clear form data
    db.clear_user_data(callback.from_user.id)
    await state.clear()
    await callback.message.answer(
        "🔄 Let's start over.\n"
        "Use the /start command to begin."
    ) 