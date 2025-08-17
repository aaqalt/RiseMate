from aiogram import Router, F, types
from aiogram.filters import Command
from keyboards.inline import language_keyboard
from utils.database import SessionLocal, User

lang_router = Router()

@lang_router.message(Command("lang"))
async def choose_language(message: types.Message):
    keyboard = language_keyboard()
    await message.answer(
        "Please choose your language / Iltimos tilni tanlang:",
        reply_markup=keyboard
    )

@lang_router.callback_query(F.data.startswith("lang_"))
async def set_language_callback(callback: types.CallbackQuery):
    lang_code = callback.data.split("_")[1]
    chat_id = callback.from_user.id

    session = SessionLocal()
    try:
        user = session.query(User).filter(User.chat_id == chat_id).first()
        if user:
            user.language = lang_code
            session.commit()
            await callback.message.edit_text(f"✅ Language set to {lang_code.upper()}")
        else:
            await callback.message.edit_text("⚠️ User not found in database.")
    finally:
        session.close()

    await callback.answer()
