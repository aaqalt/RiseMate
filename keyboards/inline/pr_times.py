from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

def time_keyboard():
    builder = InlineKeyboardBuilder()

    for hour in range(3,12): 
        builder.button(text=f"{hour}:00", callback_data=f"settime_{hour}")

    builder.adjust(3)
    return builder.as_markup()
