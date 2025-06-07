from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

def get_main_keyboard() -> ReplyKeyboardMarkup:
    kb = [
        [KeyboardButton(text="📝 Start Filling")]
    ]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

def get_form_keyboard() -> ReplyKeyboardMarkup:
    kb = [
        [
            KeyboardButton(text="⬅️ Back"),
            KeyboardButton(text="➡️ Skip"),
        ],
        [KeyboardButton(text="❌ Cancel")]
    ]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

def get_confirmation_keyboard() -> InlineKeyboardMarkup:
    kb = [
        [
            InlineKeyboardButton(text="✅ Generate PDF", callback_data="confirm_cv"),
            InlineKeyboardButton(text="🔄 Start Over", callback_data="restart_cv")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb) 