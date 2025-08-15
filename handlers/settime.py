import datetime
from aiogram import Router,html
from aiogram.filters import Command
from aiogram.types import Message,CallbackQuery
from aiogram.fsm.context import FSMContext
from keyboards.inline.pr_times import time_keyboard
from utils.database import User,session

settime_router = Router()


@settime_router.message(Command("settime"))
async def set_time_handler(message: Message, state: FSMContext):
    await message.answer(
        "Choose your daily notification time:",
        reply_markup=time_keyboard()
    )

@settime_router.callback_query(lambda c: c.data.startswith("settime_"))
async def set_time_callback(callback: CallbackQuery):
    await callback.answer()
    selected_hour = callback.data.split("_")[1]
    pr_time_value = datetime.time(int(selected_hour), 0)
    chat_id = callback.from_user.id
    User.update(session,chat_id,pr_time=pr_time_value)
    await callback.message.edit_text(
        f"✅ Your preferred time has been set to {pr_time_value.strftime('%H:%M')}."
    )