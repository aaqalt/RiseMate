from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton

def language_keyboard():
    builder = InlineKeyboardBuilder()

    builder.button(text="En 🇬🇧", callback_data="lang_en")
    builder.button(text="Uz 🇺🇿", callback_data="lang_uz")
    builder.button(text="Ru 🇷🇺", callback_data="lang_ru")

    builder.adjust(3)
    return builder.as_markup()
